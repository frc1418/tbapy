class Team:
    def __init__(self, json):
        self.json = json
        self.address = json['address']
        self.city = json['city']
        self.country = json['country']
        self.gmaps_place_id = json['gmaps_place_id']
        self.gmaps_url = json['gmaps_url']
        self.home_championship = json['home_championship']
        self.key = json['key']
        self.lat = json['lat']
        self.lng = json['lng']
        self.location_name = json['location_name']
        self.motto = json['motto']
        self.name = json['name']
        self.nickname = json['nickname']
        self.postal_code = json['postal_code']
        self.rookie_year = json['rookie_year']
        self.state_prov = json['state_prov']
        self.team_number = json['team_number']
        self.website = json['website']


class Event:
    def __init__(self, json):
        self.json = json
        self.address = json['address']
        self.city = json['city']
        self.country = json['country']
        self.district = json['district']
        self.division_keys = json['division_keys']
        self.end_date = json['end_date']
        self.event_code = json['event_code']
        self.event_type = json['event_type']
        self.event_type_string = json['event_type_string']
        self.first_event_id = json['first_event_id']
        self.gmaps_place_id = json['gmaps_place_id']
        self.gmaps_url = json['gmaps_url']
        self.key = json['key']
        self.lat = json['lat']
        self.lng = json['lng']
        self.location_name = json['location_name']
        self.name = json['name']
        self.parent_event_key = json['parent_event_key']
        self.playoff_type = json['playoff_type']
        self.playoff_type_string = json['playoff_type_string']
        self.postal_code = json['postal_code']
        self.short_name = json['short_name']
        self.start_date = json['start_date']
        self.state_prov = json['state_prov']
        self.timezone = json['timezone']
        self.webcasts = json['webcasts']
        self.website = json['website']
        self.week = json['week']
        self.year = json['year']


class Match:
    def __init__(self, json):
        self.json = json
        self.actual_time = json['actual_time']
        self.alliances = json['alliances']
        self.comp_level = json['comp_level']
        self.event_key = json['event_key']
        self.key = json['key']
        self.match_number = json['match_number']
        self.post_result_time = json['post_result_time']
        self.predicted_time = json['predicted_time']
        self.score_breakdown = json['score_breakdown']
        self.set_number = json['set_number']
        self.time = json['time']
        self.videos = json['videos']
        self.winning_alliance = json['winning_alliance']


class Award:
    def __init__(self, json):
        self.json = json
        self.award_type = json['award_type']
        self.event_key = json['event_key']
        self.name = json['name']
        self.recipient_list = json['recipient_list']
        self.year = json['year']


class District:
    def __init__(self, json):
        self.json = json
        self.abbreviation = json['abbreviation']
        self.display_name = json['display_name']
        self.key = json['key']
        self.year = json['year']


class Media:
    def __init__(self, json):
        self.json = json
        self.details = json['details']
        self.foreign_key = json['foreign_key']
        self.preferred = json['preferred']
        self.type = json['type']

class Robot:
    def __init__(self, json):
        self.json = json
        self.key = json['key']
        self.robot_name = json['robot_name']
        self.team_key = json['team_key']
        self.year = json['year']


class Profile:
    def __init__(self, json):
        self.json = json
        self.details = json['details']
        self.preferred = json['preferred']
        self.type = json['type']


class Alliance:
    def __init__(self, json):
        self.json = json
        self.backup = json['backup']
        self.declines = json['declines']
        self.name = json['name']
        self.picks = json['picks']
        self.status = json['status']


class DistrictPoints:
    def __init__(self, json):
        self.json = json
        self.extra_stats_info = json['extra_stats_info']
        self.rankings = json['rankings']
        self.sort_order_info = json['sort_order_info']


class Insights:
    def __init__(self, json):
        self.json = json
        self.playoff = json['playoff']
        self.qual = json['qual']


class OPRs:
    def __init__(self, json):
        self.json = json
        self.ccwms = json['ccwms']
        self.dprs = json['dprs']
        self.oprs = json['oprs']


class Prediction:
    def __init__(self, json):
        self.json = json
        self.match_prediction_stats = json['match_prediction_stats']
        self.match_predictions = json['match_predictions']
        self.ranking_prediction_stats = json['ranking_prediction_stats']
        self.ranking_predictions = json['ranking_predictions']
        self.stat_mean_vars = json['stat_mean_vars']


class Rankings:
    def __init__(self, json):
        self.json = json
        self.extra_stats_info = json['extra_stats_info']
        self.rankings = json['rankings']
        self.sort_order_info = json['sort_order_info']


class DistrictRanking:
    def __init__(self, json):
        self.json = json
        self.event_points = json['event_points']  # TODO: Expand this.
        self.point_total = json['point_total']
        self.rank = json['rank']
        self.rookie_bonus = json['rookie_bonus']
        self.team_key = json['team_key']
