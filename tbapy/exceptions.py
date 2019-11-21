class TBAErrorList(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__('\n'.join([f'Error type ({error[0]}): {error[1]}' for error in errors]))
