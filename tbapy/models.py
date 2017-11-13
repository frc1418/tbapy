class _base_model_class(dict):
    def __init__(self, json={}):
        self.update(json)
        self.update(self.__dict__)
        self.__dict__ = self

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.json())

    def json(self):
        return dict.__repr__(self)


def _model_class(class_name):
    return type(class_name, (_base_model_class,), {})


Team = _model_class('Team')
Event = _model_class('Event')
Match = _model_class('Match')
Award = _model_class('Award')
District = _model_class('District')
Media = _model_class('Media')
Robot = _model_class('Robot')
Profile = _model_class('Profile')
Alliance = _model_class('Alliance')
DistrictPoints = _model_class('DistrictPoints')
Insights = _model_class('Insights')
OPRs = _model_class('OPRs')
Prediction = _model_class('Prediction')
Rankings = _model_class('Rankings')
DistrictRanking = _model_class('DistrictRanking')
Status = _model_class('Status')
