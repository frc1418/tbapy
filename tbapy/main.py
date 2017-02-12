import requests


class TBA:

    URL_PRE = 'https://www.thebluealliance.com/api/v2/'
    app_id = ''

    def __init__(self, app_id):
        self.app_id = app_id

    def fetch(self, url):
        return requests.get(self.URL_PRE + url, headers={'X-TBA-App-Id': self.app_id}).json()

    def team_key(self, identifier):
        """
        Take raw team number or string key and return string key.

        We recommend passing an integer, just because it's cleaner.
        But either way works.

        :param identifier: int team number or str 'frc####'
        """
        return (identifier if type(identifier) == str else 'frc%s' % identifier)

    def teams(self, index):
        return self.fetch('teams/%s' % index)

    def team(self, team):
        return self.fetch('team/%s' % self.team_key(team))

    def team_events(self, team, year):
        return self.fetch('team/%s/%s' % (self.team_key(team), year))

    def team_awards(self, team, event=None):
        if event:
            return self.fetch('team/%s/event/%s/awards' % (self.team_key(team), event))
        else:
            return self.fetch('team/%s' % self.team_key(team))

    def team_matches(self, team, event):
        return self.fetch('team/%s/event/%s/matches' % (self.team_key(team), event))

    def team_years(self, team):
        return self.fetch('team/%s/years_participated' % self.team_key(team))

    def team_media(self, team, year=None):
        if year:
            return self.fetch('team/%s/%s/media' % (self.team_key(team), year))
        else:
            return self.fetch('team/%s/media' % self.team_key(team))

    def team_history_events(self, team):
        return self.fetch('team/%s/history/events' % self.team_key(team))

    def team_history_awards(self, team):
        return self.fetch('team/%s/history/awards' % self.team_key(team))

    def team_history_robots(self, team):
        return self.fetch('team/%s/history/robots' % self.team_key(team))

    def team_history_districts(self, team):
        return self.fetch('team/%s/history/districts' % self.team_key(team))

    def event_list(self, year=None):
        if year:
            return self.fetch('events/%s' % year)
        else:
            return self.fetch('events/')

    def event(self, event):
        return self.fetch('event/%s' % event)

    def event_teams(self, event):
        return self.fetch('event/%s/teams' % event)

    def event_stats(self, event):
        return self.fetch('event/%s/stats' % event)

    def event_rankings(self, event):
        return self.fetch('event/%s/rankings' % event)

    def event_awards(self, event):
        return self.fetch('event/%s/awards' % event)

    def event_matches(self, event):
        return self.fetch('event/%s/matches' % event)

    def district_points(self, event):
        return self.fetch('event/%s/district_points' % event)

    # TODO: Make this a bit more accessible. Add automatic key generation, etc.
    def match(self, match):
        return self.fetch('match/%s' % match)

    def districts(self, year):
        return self.fetch('districts/%s' % year)

    def district_events(self, district, year):
        return self.fetch('district/%s/%s/events' % (district, year))

    def district_rankings(self, district, year):
        return self.fetch('district/%s/%s/rankings' % (district, year))

    def district_teams(self, district, year):
        return self.fetch('district/%s/%s/teams' % (district, year))
