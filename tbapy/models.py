class _base_model_class(dict):
    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            raise KeyError(item)

def _create_model_class(class_name, *json_keys):
    def init(self, json):
        self.json = json
        self.update(json)
        for key in json_keys:
            setattr(self, key, json[key])
    return type(class_name, (_base_model_class,), {'__init__': init})

Team = _create_model_class('Team', 'address', 'city', 'country', 'gmaps_place_id', 'gmaps_url', 'home_championship', 'key', 'lat', 'lng',
                           'location_name', 'motto', 'name', 'nickname', 'postal_code', 'rookie_year', 'state_prov', 'team_number', 'website')

Event = _create_model_class('Event', 'address', 'city', 'country', 'district', 'division_keys', 'end_date', 'event_code', 'event_type',
                            'event_type_string', 'first_event_id', 'gmaps_place_id', 'gmaps_url', 'key', 'lat', 'lng', 'location_name', 'name',
                            'parent_event_key', 'playoff_type', 'playoff_type_string', 'postal_code', 'short_name', 'start_date', 'state_prov',
                            'timezone', 'webcasts', 'website', 'week', 'year')

Match = _create_model_class('Match', 'actual_time', 'alliances', 'comp_level', 'event_key', 'key', 'match_number', 'post_result_time',
                            'predicted_time', 'score_breakdown', 'set_number', 'time', 'videos', 'winning_alliance')

Award = _create_model_class('Award', 'award_type', 'event_key', 'name', 'recipient_list', 'year')

District = _create_model_class('District', 'abbreviation', 'display_name', 'key', 'year')

Media = _create_model_class('Media', 'details', 'foreign_key', 'preferred', 'type')

Robot = _create_model_class('Robot', 'key', 'robot_name', 'team_key', 'year')

Profile = _create_model_class('Profile', 'details', 'preferred', 'type')

Alliance = _create_model_class('Alliance', 'backup', 'declines', 'name', 'picks', 'status')

DistrictPoints = _create_model_class('DistrictPoints', 'extra_stats_info', 'rankings', 'sort_order_info')

Insights = _create_model_class('Insights', 'playoff', 'qual')

OPRs = _create_model_class('OPRs', 'ccwms', 'dprs', 'oprs')

Prediction = _create_model_class('Prediction', 'match_prediction_stats', 'match_predictions', 'ranking_prediction_stats',
                                 'ranking_predictions', 'stat_mean_vars')
Rankings = _create_model_class('Rankings', 'extra_stats_info', 'rankings', 'sort_order_info')

DistrictRanking = _create_model_class('DistrictRanking', 'event_points', 'point_total', 'rank', 'rookie_bonus', 'team_key')
