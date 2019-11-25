class TBAErrorList(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__('\n'.join([f'Error type ({error[0]}): {error[1]}' for error in errors]))


class LastModifiedDate:
    def __init__(self, date_string):
        self.date_string = date_string

    def __bool__(self):
        return False


class NotModifiedException(Exception):
    def __init__(self, last_modified):
        self.last_modified = LastModifiedDate(last_modified)