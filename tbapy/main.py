import functools
import requests
import json
from hashlib import md5
from .models import *
from .exceptions import *
from cachecontrol import CacheControl
from datetime import datetime
import time


class TBA:
    """
    Main library class.

    Contains methods for interacting with The Blue Alliance.
    """

    READ_URL_PRE = 'https://www.thebluealliance.com/api/v3/'
    WRITE_URL_PRE = 'https://www.thebluealliance.com/api/trusted/v1/'
    session = CacheControl(requests.Session())
    auth_secret = ''
    event_key = ''

    def __init__(self, auth_key, auth_id='', auth_secret='', event_key=''):
        """
        Store auth key so we can reuse it as many times as we make a request.

        :param auth_key: Your application authorization key, obtainable at https://www.thebluealliance.com/account.
        :param auth_id: Your event authorization ID, obtainable at https://www.thebluealliance.com/request/apiwrite
        :param auth_secret: Your event authorization secret, obtainable at https://www.thebluealliance.com/request/apiwrite
        :param event_key: The event key that is linked to the ID and secret provided.
        """
        self.auth_secret = auth_secret
        self.event_key = event_key
        self.session.headers.update({'X-TBA-Auth-Key': auth_key, 'X-TBA-Auth-Id': auth_id})
        self._if_modified_since = None
        self._last_modified = False

    def _get(self, url):
        """
        Helper method: GET data from given URL on TBA's API.

        :param url: URL string to get data from.
        :return: Requested data in JSON format.
        """
        extra_headers = {}
        if self._if_modified_since is not None:
            extra_headers['If-Modified-Since'] = self._if_modified_since

        response = self.session.get(self.READ_URL_PRE + url, headers=extra_headers)
        last_modified = response.headers.get('Last-Modified')
        
        if last_modified is not None:
            if response.status_code == 304:
                raise NotModifiedException(response.headers['Last-Modified'])

            if self._last_modified:
                self._last_modified = LastModifiedDate(last_modified)

        raw = response.json()
        self._detect_errors(raw)
        return raw

    def _post(self, url, data):
        """
        Helper method: POST data to a given URL on TBA's API.

        :param url: URL string to post data to and hash.
        :pararm data: JSON data to post and hash.
        :return: Requests Response object.

        """
        raw = self.session.post(
            self.WRITE_URL_PRE + url % self.event_key, 
            data=data, 
            headers={
                'X-TBA-Auth-Sig': md5((self.auth_secret + '/api/trusted/v1/' + url % self.event_key + data).encode('utf-8')).hexdigest()
            }
        )

        self._detect_errors(raw)
        return raw

    def _detect_errors(self, json):
        if not isinstance(json, dict):
            return

        errors = json.get('Errors')
        if errors is not None:
            raise TBAErrorList([error.popitem() for error in errors])

    def _check_modified(func):
        @functools.wraps(func)
        def wrapper(self, *args, last_modified=False, if_modified_since=None, silent=True, **kwargs):
            self._if_modified_since = if_modified_since and datetime.strftime(if_modified_since, '%a, %d %b %Y %H:%M:%S GMT')
            self._last_modified = last_modified

            if last_modified or if_modified_since:
                self.cache = False

            try:
                output = func(self, *args, **kwargs)
                if last_modified:
                    return output, self._last_modified
                return output
            except NotModifiedException as e:
                if not silent:
                    raise e from None
                return e.last_modified
            finally:
                self.cache = True

        return wrapper

    @property
    def cache(self):
        for adapter in self.session.adapters.values():
            if 'GET' in adapter.cacheable_methods:
                return True

        return False

    @cache.setter
    def cache(self, on):
        for adapter in self.session.adapters.values():
            if on:
                adapter.cacheable_methods = ('GET',)
            else:
                adapter.cacheable_methods = ()

    @staticmethod
    def team_key(identifier):
        """
        Take raw team number or string key and return string key.

        Used by all team-related methods to support either an integer team number or team key being passed.

        (We recommend passing an integer, just because it's cleaner. But whatever works.)

        :param identifier: int team number or str 'frc####'
        :return: string team key in format 'frc####'
        """
        return identifier if type(identifier) == str else 'frc%s' % identifier

    @_check_modified
    def status(self):
        """
        Get TBA API status information.

        :return: Data on current status of the TBA API as APIStatus object.
        """
        return APIStatus(self._get('status'))

    @_check_modified
    def teams(self, page=None, year=None, simple=False, keys=False):
        """
        Get list of teams.

        :param page: Page of teams to view. Each page contains 500 teams.
        :param year: View teams from a specific year.
        :param simple: Get only vital data.
        :param keys: Set to true if you only want the teams' keys rather than full data on them.
        :return: List of Team objects or string keys.
        """
        # If the user has requested a specific page, get that page.
        if page is not None:
            if year:
                if keys:
                    return self._get('teams/%s/%s/keys' % (year, page))
                else:
                    return [Team(raw) for raw in self._get('teams/%s/%s%s' % (year, page, '/simple' if simple else ''))]
            else:
                if keys:
                    return self._get('teams/%s/keys' % page)
                else:
                    return [Team(raw) for raw in self._get('teams/%s%s' % (page, '/simple' if simple else ''))]
        # If no page was specified, get all of them and combine.
        else:
            teams = []
            target = 0
            while True:
                page_teams = self.teams(page=target, year=year, simple=simple, keys=keys)
                if page_teams:
                    teams.extend(page_teams)
                else:
                    break
                target += 1
            return teams

    @_check_modified
    def team(self, team, simple=False):
        """
        Get data on a single specified team.

        :param team: Team to get data for.
        :param simple: Get only vital data.
        :return: Team object with data on specified team.
        """
        return Team(self._get('team/%s%s' % (self.team_key(team), '/simple' if simple else '')))

    @_check_modified
    def team_events(self, team, year=None, simple=False, keys=False):
        """
        Get team events a team has participated in.

        :param team: Team to get events for.
        :param year: Year to get events from.
        :param simple: Get only vital data.
        :param keys: Get just the keys of the events. Set to True if you only need the keys of each event and not their full data.
        :return: List of strings or Teams
        """
        if year:
            if keys:
                return self._get('team/%s/events/%s/keys' % (self.team_key(team), year))
            else:
                return [Event(raw) for raw in self._get('team/%s/events/%s%s' % (self.team_key(team), year, '/simple' if simple else ''))]
        else:
            if keys:
                return self._get('team/%s/events/keys' % self.team_key(team))
            else:
                return [Event(raw) for raw in self._get('team/%s/events%s' % (self.team_key(team), '/simple' if simple else ''))]

    @_check_modified
    def team_awards(self, team, year=None, event=None):
        """
        Get list of awards team has recieved.

        :param team: Team to get awards of.
        :param year: Year to get awards from.
        :param event: Event to get awards from.
        :return: List of Award objects
        """
        if event:
            return [Award(raw) for raw in self._get('team/%s/event/%s/awards' % (self.team_key(team), event))]
        else:
            if year:
                return [Award(raw) for raw in self._get('team/%s/awards/%s' % (self.team_key(team), year))]
            else:
                return [Award(raw) for raw in self._get('team/%s/awards' % self.team_key(team))]

    @_check_modified
    def team_matches(self, team, event=None, year=None, simple=False, keys=False):
        """
        Get list of matches team has participated in.

        :param team: Team to get matches of.
        :param year: Year to get matches from.
        :param event: Event to get matches from.
        :param simple: Get only vital data.
        :param keys: Only get match keys rather than their full data.
        :return: List of string keys or Match objects.
        """
        if event:
            if keys:
                return self._get('team/%s/event/%s/matches/keys' % (self.team_key(team), event))
            else:
                return [Match(raw) for raw in self._get('team/%s/event/%s/matches%s' % (self.team_key(team), event, '/simple' if simple else ''))]
        elif year:
            if keys:
                return self._get('team/%s/matches/%s/keys' % (self.team_key(team), year))
            else:
                return [Match(raw) for raw in self._get('team/%s/matches/%s%s' % (self.team_key(team), year, '/simple' if simple else ''))]

    @_check_modified
    def team_years(self, team):
        """
        Get years during which a team participated in FRC.

        :param team: Key for team to get data about.
        :return: List of integer years in which team participated.
        """
        return self._get('team/%s/years_participated' % self.team_key(team))

    @_check_modified
    def team_media(self, team, year=None, tag=None):
        """
        Get media for a given team.

        :param team: Team to get media of.
        :param year: Year to get media from.
        :param tag: Get only media with a given tag.
        :return: List of Media objects.
        """
        return [Media(raw) for raw in self._get('team/%s/media%s%s' % (self.team_key(team), ('/tag/%s' % tag) if tag else '', ('/%s' % year) if year else ''))]

    @_check_modified
    def team_robots(self, team):
        """
        Get data about a team's robots.

        :param team: Key for team whose robots you want data on.
        :return: List of Robot objects
        """
        return [Robot(raw) for raw in self._get('team/%s/robots' % self.team_key(team))]

    @_check_modified
    def team_districts(self, team):
        """
        Get districts a team has competed in.

        :param team: Team to get data on.
        :return: List of District objects.
        """
        return [District(raw) for raw in self._get('team/%s/districts' % self.team_key(team))]

    @_check_modified
    def team_profiles(self, team):
        """
        Get team's social media profiles linked on their TBA page.

        :param team: Team to get data on.
        :return: List of Profile objects.
        """
        return [Profile(raw) for raw in self._get('team/%s/social_media' % self.team_key(team))]

    @_check_modified
    def team_status(self, team, event):
        """
        Get status of a team at an event.

        :param team: Team whose status to get.
        :param event: Event team is at.
        :return: Status object.
        """
        return Status(self._get('team/%s/event/%s/status' % (self.team_key(team), event)))

    @_check_modified
    def events(self, year, simple=False, keys=False):
        """
        Get a list of events in a given year.

        :param year: Year to get events from.
        :param keys: Get only keys of the events rather than full data.
        :param simple: Get only vital data.
        :return: List of string event keys or Event objects.
        """
        if keys:
            return self._get('events/%s/keys' % year)
        else:
            return [Event(raw) for raw in self._get('events/%s%s' % (year, '/simple' if simple else ''))]

    @_check_modified
    def event(self, event, simple=False):
        """
        Get basic information about an event.

        More specific data (typically obtained with the detail_type URL parameter) can be obtained with event_alliances(), event_district_points(), event_insights(), event_oprs(), event_predictions(), and event_rankings().

        :param event: Key of event for which you desire data.
        :param simple: Get only vital data.
        :return: A single Event object.
        """
        return Event(self._get('event/%s%s' % (event, '/simple' if simple else '')))

    @_check_modified
    def event_alliances(self, event):
        """
        Get information about alliances at event.

        :param event: Key of event to get data on.
        :return: List of Alliance objects.
        """
        return [Alliance(raw) for raw in self._get('event/%s/alliances' % event)]

    @_check_modified
    def event_district_points(self, event):
        """
        Get district point information about an event.

        :param event: Key of event to get data on.
        :return: Single DistrictPoints object.
        """
        return DistrictPoints(self._get('event/%s/district_points' % event))

    @_check_modified
    def event_insights(self, event):
        """
        Get insights about an event.

        :param event: Key of event to get data on.
        :return: Single Insights object.
        """
        return Insights(self._get('event/%s/insights' % event))

    @_check_modified
    def event_oprs(self, event):
        """
        Get OPRs from an event.

        :param event: Key of event to get data on.
        :return: Single OPRs object.
        """
        return OPRs(self._get('event/%s/oprs' % event))

    @_check_modified
    def event_predictions(self, event):
        """
        Get predictions for matches during an event.

        :param event: Key of event to get data on.
        :return: Single Predictions object.
        """
        return Predictions(self._get('event/%s/predictions' % event))

    @_check_modified
    def event_rankings(self, event):
        """
        Get rankings from an event.

        :param event: Key of event to get data on.
        :return: Single Rankings object.
        """
        return Rankings(self._get('event/%s/rankings' % event))

    @_check_modified
    def event_teams(self, event, simple=False, keys=False):
        """
        Get list of teams at an event.

        :param event: Event key to get data on.
        :param simple: Get only vital data.
        :param keys: Return list of team keys only rather than full data on every team.
        :return: List of string keys or Team objects.
        """
        if keys:
            return self._get('event/%s/teams/keys' % event)
        else:
            return [Team(raw) for raw in self._get('event/%s/teams%s' % (event, '/simple' if simple else ''))]

    @_check_modified
    def event_awards(self, event):
        """
        Get list of awards presented at an event.

        :param event: Event key to get data on.
        :return: List of Award objects.
        """
        return [Award(raw) for raw in self._get('event/%s/awards' % event)]

    @_check_modified
    def event_matches(self, event, simple=False, keys=False):
        """
        Get list of matches played at an event.

        :param event: Event key to get data on.
        :param keys: Return list of match keys only rather than full data on every match.
        :param simple: Get only vital data.
        :return: List of string keys or Match objects.
        """
        if keys:
            return self._get('event/%s/matches/keys' % event)
        else:
            return [Match(raw) for raw in self._get('event/%s/matches%s' % (event, '/simple' if simple else ''))]

    @_check_modified
    def match(self, key=None, year=None, event=None, type='qm', number=None, round=None, simple=False):
        """
        Get data on a match.

        You may either pass the match's key directly, or pass `year`, `event`, `type`, `match` (the match number), and `round` if applicable (playoffs only). The event year may be specified as part of the event key or specified in the `year` parameter.

        :param key: Key of match to get data on. First option for specifying a match (see above).
        :param year: Year in which match took place. Optional; if excluded then must be included in event key.
        :param event: Key of event in which match took place. Including year is optional; if excluded then must be specified in `year` parameter.
        :param type: One of 'qm' (qualifier match), 'qf' (quarterfinal), 'sf' (semifinal), 'f' (final). If unspecified, 'qm' will be assumed.
        :param number: Match number. For example, for qualifier 32, you'd pass 32. For Semifinal 2 round 3, you'd pass 2.
        :param round: For playoff matches, you will need to specify a round.
        :param simple: Get only vital data.
        :return: A single Match object.
        """
        if key:
            return Match(self._get('match/%s%s' % (key, '/simple' if simple else '')))
        else:
            return Match(self._get('match/{year}{event}_{type}{number}{round}{simple}'.format(year=year if not event[0].isdigit() else '',
                                                                                              event=event,
                                                                                              type=type,
                                                                                              number=number,
                                                                                              round=('m%s' % round) if not type == 'qm' else '',
                                                                                              simple='/simple' if simple else '')))

    @_check_modified
    def districts(self, year):
        """
        Return a list of districts active.

        :param year: Year from which you want to get active districts.
        :return: A list of District objects.
        """
        return [District(raw) for raw in self._get('districts/%s' % year)]

    @_check_modified
    def district_events(self, district, simple=False, keys=False):
        """
        Return list of events in a given district.

        :param district: Key of district whose events you want.
        :param simple: Get only vital data.
        :param keys: Return list of event keys only rather than full data on every event.
        :return: List of string keys or Event objects.
        """
        if keys:
            return self._get('district/%s/events/keys' % district)
        else:
            return [Event(raw) for raw in self._get('district/%s/events%s' % (district, '/simple' if simple else ''))]

    @_check_modified
    def district_rankings(self, district):
        """
        Return data about rankings in a given district.

        :param district: Key of district to get rankings of.
        :return: List of DistrictRanking objects.
        """
        return [DistrictRanking(raw) for raw in self._get('district/%s/rankings' % district)]

    @_check_modified
    def district_teams(self, district, simple=False, keys=False):
        """
        Get list of teams in the given district.

        :param district: Key for the district to get teams in.
        :param simple: Get only vital data.
        :param keys: Return list of team keys only rather than full data on every team.
        :return: List of string keys or Team objects.
        """
        if keys:
            return self._get('district/%s/teams/keys' % district)
        else:
            return [Team(raw) for raw in self._get('district/%s/teams' % district)]

    def update_trusted(self, auth_id, auth_secret, event_key):
        """
        Set Trusted API ID and Secret and the event key they are assigned to.

        :param auth_id: Your event authorization ID, obtainable at https://www.thebluealliance.com/request/apiwrite
        :param auth_secret: Your event authorization secret, obtainable at https://www.thebluealliance.com/request/apiwrite
        :param event_key: The event key that is linked to the ID and secret provided.
        """
        self.session.headers.update({'X-TBA-Auth-Id': auth_id})
        self.auth_secret = auth_secret
        self.event_key = event_key

    def update_event_info(self, data):
        """
        Update an event's info on The Blue Alliance.

        :param data: Dictionary of data to update the event with.
        """
        return self._post('event/%s/info/update', json.dumps(data))

    def update_event_alliances(self, data):
        """
        Update an event's alliances on The Blue Alliance.

        :param data: List of lists of alliances in frc#### string format.
        """
        return self._post('event/%s/alliance_selections/update', json.dumps(data))

    def update_event_awards(self, data):
        """
        Update an event's awards on The Blue Alliance.

        :param data: List of Dictionaries of award winners. Each dictionary should have a name_str for the award name, team_key in frc#### string format, and the awardee for any awards given to individuals. The last two can be null
        """
        return self._post('event/%s/awards/update', json.dumps(data))

    def update_event_matches(self, data):
        """
        Update an event's matches on The Blue Alliance.

        :param data: List of Dictionaries. More info about the match data can be found in the API docs.
        """
        return self._post('event/%s/matches/update', json.dumps(data))

    def delete_event_matches(self, data=None):
        """
        Delete an event's matches on The Blue Alliance.

        :param data: List of match keys to delete, can be ommited if you would like to delete all matches.
        """
        return self._post('event/%s/matches/delete_all' if data is None else 'event/%s/matches/delete', json.dumps(self.event_key) if data is None else json.dumps(data))

    def update_event_rankings(self, data):
        """
        Update an event's rankings on The Blue Alliance.

        :param data: Dictionary of breakdowns and rankings. Rankings are a list of dictionaries.
        """
        return self._post('event/%s/rankings/update', json.dumps(data))

    def update_event_team_list(self, data):
        """
        Update an event's team list on The Blue Alliance.

        :param data: a list of team keys in frc#### string format.
        """
        return self._post('event/%s/team_list/update', json.dumps(data))

    def add_match_videos(self, data):
        """
        Add match videos to the respective match pages of an event on The Blue Alliance.

        :param data: Dictionary of partial match keys to youtube video ids.
        """
        return self._post('event/%s/match_videos/add', json.dumps(data))

    def add_event_videos(self, data):
        """
        Add videos to an event's media tab on The Blue Alliance.

        :param data: List of youtube video ids.
        """
        return self._post('event/%s/media/add', json.dumps(data))
