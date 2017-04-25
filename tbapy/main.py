from requests import get


class TBA:
    """
    Main library class.
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
    def teams(self, page, year=None, model_type=None):
        """
        Get list of teams.

        :param page: Page of teams to view. Each page contains 500 teams.
        :param year: Pass this parameter to view teams from a specific year.
        :param model_type: Type of data to view. `simple` option will return every team's full data, where `keys` option will just return a list of keys.
        """
        if year:
            if model_type:
                return self.fetch('teams/%s/%s/%s' % (year, page, model_type))
            else:
                return self.fetch('teams/%s/%s' % (year, page))
        else:
            if model_type:
                return self.fetch('teams/%s/%s' % (page, model_type))
            else:
                return self.fetch('teams/%s' % (page))

    def team(self, team, model_type=None):
        """
        Get data on a single specified team.

        :param model_type: Type of data to view. `simple` option will return simpler data on a team, where `keys` option will just return a list of keys.
        """
        if model_type:
            return self.fetch('team/%s/%s' % (self.team_key(team), model_type))
        else:
            return self.fetch('team/%s' % self.team_key(team))

    def team_events(self, team, year=None, model_type=None):
        """
        Get team events a team has participated in.

        :param team: Team to get events for.
        :param year: Year to get events from.
        :param model_type: Type of data to get. `simple` option will return event data as normal, where `keys` option will just return a list of event keys.
        """
        if year:
            if model_type:
                return self.fetch('team/%s/%s/events/%s' % (self.team_key(team), year, model_type))
            else:
                return self.fetch('team/%s/%s/events' % (self.team_key(team), year))
        else:
            if model_type:
                return self.fetch('team/%s/events/%s' % (self.team_key(team), model_type))
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

    def team_matches(self, team, event=None, year=None, model_type=None):
        """
        Get list of matches team has participated in.

        :param team: Team to get matches of.
        :param year: Year to get matches from.
        :param event: Event to get matches from.
        """
        if event:
            if model_type:
                return self.fetch('team/%s/event/%s/matches/%s' % (self.team_key(team), event, model_type))
            else:
                return self.fetch('team/%s/event/%s/matches' % (self.team_key(team), event))
        elif year:
            if model_type:
                return self.fetch('team/%s/matches/%s/%s' % (self.team_key(team), year, model_type))
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

    def events(self, year, model_type=None):
        """
        Get a list of events in a given year.

        :param year: Year to get events from.
        :param model_type: Type of data to view. `simple` option will return simpler data on a team, where `keys` option will just return a list of keys.
        """
        if model_type:
            return self.fetch('events/%s/%s' % (year, model_type))
        else:
            return self.fetch('events/%s' % year)

    def event(self, event, model_type=None):
        """
        Get basic information about an event.

        Further, more specific data (typically obtained with the detail_type URL parameter) can be obtained with event_alliances(), event_district_points(), event_insights(), event_oprs(), event_predictions(), and event_rankings().

        :param event: Key of event for which you desire data.
        :param model_type: Data model type. (`simple` is the only option here, and will return simplified data.)
        """
        if model_type:
            return self.fetch('event/%s/%s' % (event, model_type))
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

    def event_teams(self, event, model_type=None):
        """
        Get list of teams at an event.

        :param event: Event key to get data on.
        :param model_type: Type of data to view. `simple` option will return team data as normal, where `keys` option will just return a list of team keys.
        """
        if model_type:
            return self.fetch('event/%s/teams/%s' % (event, model_type))
        else:
            return self.fetch('event/%s/teams' % event)

    def event_awards(self, event):
        """
        Get list of awards presented at an event.

        :param event: Event key to get data on.
        """
        return self.fetch('event/%s/awards' % event)

    def event_matches(self, event, model_type=None):
        """
        Get list of matches played at an event.

        :param event: Event key to get data on.
        :param model_type: Type of data to view. `simple` option will return simpler data on matches, where `keys` option will just return a list of their keys.
        """
        if model_type:
            return self.fetch('event/%s/matches/%s' % (event, model_type))
        else:
            return self.fetch('event/%s/matches' % event)

    def match(self, key=None, year=None, event=None, type='qm', match=None, round=None, model_type=None):
        """
        Get data on a match.

        :param match: Key of match to get data on.
        """
        if key:
            return self.fetch('match/%s' % key)
        else:
            return self.fetch('match/%s%s_%s%s%s' % (year if not event[0].isdigit() else '', event, type, match, ('m%s' % round) if not type == 'qm' else ''))

    def districts(self, year):
        """
        Return a list of districts active.

        :param year: Year from which you want to get active districts.
        """
        return self.fetch('districts/%s' % year)

    def district_events(self, district, model_type=None):
        """
        Return list of events in a given district.

        :param district: Key of district whose events you want.
        :param model_type: Type of data to view. `simple` option will return simpler data on events, where `keys` option will just return a list of their keys.
        """
        if model_type:
            return self.fetch('district/%s/events/%s' % (district, model_type))
        else:
            return self.fetch('district/%s/events' % district)

    def district_rankings(self, district):
        """
        Return data about rankings in a given district.

        :param district: Key of district to get rankings of.
        """
        return self.fetch('district/%s/rankings' % district)

    def district_teams(self, district, year, model_type=None):
        """
        Get list of teams in the given district in a certain year.

        :param district: Key for the district to get teams in.
        :param year: Year from which to get teams.
        :param model_type: Type of data to view. `simple` option will return simpler data on events, where `keys` option will just return a list of their keys.
        """
        if model_type:
            return self.fetch('district/%s/%s/teams/%s' % (district, year, model_type))
        else:
            return self.fetch('district/%s/%s/teams' % (district, year))

    # TODO: Suggest media request.
    # TODO: Use .format() instead of % notation.
    # TODO: Return data in object form rather than as JSON.
