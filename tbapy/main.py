from requests import get


class TBA:
    """
    Main library class.

    Contains methods for interacting with The Blue Alliance.
    """

    URL_PRE = 'https://www.thebluealliance.com/api/v3/'
    auth_key = ''

    def __init__(self, auth_key):
        """
        Store auth key so we can reuse it as many times as we make a request.

        :param auth_key: Your application authorization key, obtainable at https://www.thebluealliance.com/account.
        """
        self.auth_key = auth_key

    def fetch(self, url):
        """
        Helper method: fetch data from given URL on TBA's API.

        :param url: URL string to get data from.
        """
        return get(self.URL_PRE + url, headers={'X-TBA-Auth-Key': self.auth_key}).json()

    def team_key(self, identifier):
        """
        Take raw team number or string key and return string key.

        We recommend passing an integer, just because it's cleaner.
        But either way works.

        :param identifier: int team number or str 'frc####'
        """
        return (identifier if type(identifier) == str else 'frc%s' % identifier)

    def status(self):
        """
        Return TBA API status information.
        """
        return self.fetch('status')

    # TODO: Allow automatic fetching of entire team list.
    def teams(self, page, year=None, keys=False):
        """
        Get list of teams.

        :param page: Page of teams to view. Each page contains 500 teams.
        :param year: Pass this parameter to view teams from a specific year.
        :param keys: Set to true if you only want the teams' keys rather than full data on them.
        """
        if year:
            if keys:
                return self.fetch('teams/%s/%s/keys' % (year, page))
            else:
                return self.fetch('teams/%s/%s' % (year, page))
        else:
            if keys:
                return self.fetch('teams/%s/keys' % page)
            else:
                return self.fetch('teams/%s' % page)

    def team(self, team, simple=False):
        """
        Get data on a single specified team.

        :param simple: Fetch simpler data. Use if you only need basic data about the team.
        """
        if simple:
            return self.fetch('team/%s/simple' % self.team_key(team))
        else:
            return self.fetch('team/%s' % self.team_key(team))

    def team_events(self, team, year=None, keys=False):
        """
        Get team events a team has participated in.

        :param team: Team to get events for.
        :param year: Year to get events from.
        :param keys: Get just the keys of the events. Set to True if you only need the keys of each event and not their full data.
        """
        if year:
            if keys:
                return self.fetch('team/%s/%s/events/keys' % (self.team_key(team), year))
            else:
                return self.fetch('team/%s/%s/events' % (self.team_key(team), year))
        else:
            if keys:
                return self.fetch('team/%s/events/keys' % self.team_key(team))
            else:
                return self.fetch('team/%s/events' % self.team_key(team))

    def team_awards(self, team, year=None, event=None):
        """
        Get list of awards team has recieved.

        :param team: Team to get awards of.
        :param year: Year to get awards from.
        :param event: Event to get awards from.
        """
        if event:
            return self.fetch('team/%s/event/%s/awards' % (self.team_key(team), event))
        else:
            if year:
                return self.fetch('team/%s/awards/%s' % (self.team_key(team), year))
            else:
                return self.fetch('team/%s/awards' % self.team_key(team))

    def team_matches(self, team, event=None, year=None, keys=False):
        """
        Get list of matches team has participated in.

        :param team: Team to get matches of.
        :param year: Year to get matches from.
        :param event: Event to get matches from.
        :param keys: Only fetch match keys rather than their full data.
        """
        if event:
            if keys:
                return self.fetch('team/%s/event/%s/matches/keys' % (self.team_key(team), event))
            else:
                return self.fetch('team/%s/event/%s/matches' % (self.team_key(team), event))
        elif year:
            if keys:
                return self.fetch('team/%s/matches/%s/keys' % (self.team_key(team), year))
            else:
                return self.fetch('team/%s/matches/%s' % (self.team_key(team), year))

    def team_years(self, team):
        """
        Get years during which a team participated in FRC.

        :param team: Key for team to get data about.
        """
        return self.fetch('team/%s/years_participated' % self.team_key(team))

    def team_media(self, team, year):
        """
        Get media for a given team.

        :param team: Team to get media of.
        :param year: Year to get media from.
        """
        return self.fetch('team/%s/media/%s' % (self.team_key(team), year))

    def team_robots(self, team):
        """
        Get data about a team's robots.

        :param team: Key for team whose robots you want data on.
        """
        return self.fetch('team/%s/robots' % self.team_key(team))

    def team_districts(self, team):
        """
        Get districts a team has competed in.

        :param team: Team to get data on.
        """
        return self.fetch('team/%s/districts' % self.team_key(team))

    def team_social_media(self, team):
        """
        Get team's social media profiles linked on their TBA page.

        :param team: Team to get data on.
        """
        return self.fetch('team/%s/social_media')

    def events(self, year, keys=False):
        """
        Get a list of events in a given year.

        :param year: Year to get events from.
        :param keys: Get only keys of the events rather than full data.
        """
        if keys:
            return self.fetch('events/%s/keys' % year)
        else:
            return self.fetch('events/%s' % year)

    def event(self, event, simple=False):
        """
        Get basic information about an event.

        More specific data (typically obtained with the detail_type URL parameter) can be obtained with event_alliances(), event_district_points(), event_insights(), event_oprs(), event_predictions(), and event_rankings().

        :param event: Key of event for which you desire data.
        :param simple: Fetch simpler data about event. Use this if you don't need the extra information provided by a standard request.
        """
        if simple:
            return self.fetch('event/%s/simple' % event)
        else:
            return self.fetch('event/%s' % event)

    def event_alliances(self, event):
        """
        Get information about alliances at event.

        :param event: Key of event to get data on.
        """
        return self.fetch('event/%s/alliances' % event)

    def event_district_points(self, event):
        """
        Get district point information about an event.

        :param event: Key of event to get data on.
        """
        return self.fetch('event/%s/district_points' % event)

    def event_insights(self, event):
        """
        Get insights about an event.

        :param event: Key of event to get data on.
        """
        return self.fetch('event/%s/insights' % event)

    def event_oprs(self, event):
        """
        Get OPRs from an event.

        :param event: Key of event to get data on.
        """
        return self.fetch('event/%s/oprs' % event)

    def event_predictions(self, event):
        """
        Get predictions for matches during an event.

        :param event: Key of event to get data on.
        """
        return self.fetch('event/%s/predictions' % event)

    def event_rankings(self, event):
        """
        Get rankings from an event.

        :param event: Key of event to get data on.
        """
        return self.fetch('event/%s/rankings' % event)

    def event_teams(self, event, keys=False):
        """
        Get list of teams at an event.

        :param event: Event key to get data on.
        :param keys: Return list of team keys only rather than full data on every team.
        """
        if keys:
            return self.fetch('event/%s/teams/keys' % event)
        else:
            return self.fetch('event/%s/teams' % event)

    def event_awards(self, event):
        """
        Get list of awards presented at an event.

        :param event: Event key to get data on.
        """
        return self.fetch('event/%s/awards' % event)

    def event_matches(self, event, keys=False):
        """
        Get list of matches played at an event.

        :param event: Event key to get data on.
        :param keys: Return list of match keys only rather than full data on every match.
        """
        if keys:
            return self.fetch('event/%s/matches/keys' % event)
        else:
            return self.fetch('event/%s/matches' % event)

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
        :param simple: Set to True to get simpler match data. Recommended unless you need the data given in the full request.
        """
        if key:
            return self.fetch('match/%s' % key)
        else:
            return self.fetch('match/%s%s_%s%s%s' % (year if not event[0].isdigit() else '', event, type, number, ('m%s' % round) if not type == 'qm' else ''))

    def districts(self, year):
        """
        Return a list of districts active.

        :param year: Year from which you want to get active districts.
        """
        return self.fetch('districts/%s' % year)

    def district_events(self, district, keys=False):
        """
        Return list of events in a given district.

        :param district: Key of district whose events you want.
        :param keys: Return list of event keys only rather than full data on every event.
        """
        if keys:
            return self.fetch('district/%s/events/keys' % district)
        else:
            return self.fetch('district/%s/events' % district)

    def district_rankings(self, district):
        """
        Return data about rankings in a given district.

        :param district: Key of district to get rankings of.
        """
        return self.fetch('district/%s/rankings' % district)

    def district_teams(self, district, year, keys=False):
        """
        Get list of teams in the given district in a certain year.

        :param district: Key for the district to get teams in.
        :param year: Year from which to get teams.
        :param keys: Return list of team keys only rather than full data on every team.
        """
        if keys:
            return self.fetch('district/%s/%s/teams/keys' % (district, year))
        else:
            return self.fetch('district/%s/%s/teams' % (district, year))

    # TODO: Suggest media request.
    # TODO: Use .format() instead of % notation.
    # TODO: Return data in object form rather than as JSON.
