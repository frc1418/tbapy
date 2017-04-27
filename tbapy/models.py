class _base_model_class(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def __init__(self, json):
        self.json = json
        self.update(json)
    def __repr__(self):
        contents = {k: self[k] for k in self if k != 'json'} # Exclude :json: from the string
        return '%s(%s)' % (self.__class__.__name__, dict.__repr__(contents))

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
