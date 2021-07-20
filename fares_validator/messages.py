import enum


class Messages:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def add_warning(self, *args, **kwargs):
        self.warnings.append(Messages.message_to_string(*args, **kwargs))

    def add_error(self, *args, **kwargs):
        self.errors.append(Messages.message_to_string(*args, **kwargs))

    @staticmethod
    def message_to_string(code, line_context='', path='', extra_info=''):
        msg = ''
        if path:
            msg += path + ': '
    
        msg += code
    
        if extra_info:
            msg += '\n' + extra_info
        
        msg += line_context
        return msg

    def to_string(self):
        output = ''
        if len(self.errors):
            output += 'ERRORS:\n'

            for error in self.errors:
                output += '\n' + error + '\n'
        else:
            output += 'No errors detected.\n'

        if len(self.warnings):
            output += '\n\nWARNINGS:\n'

            for warning in self.warnings:
                output += '\n' + warning + '\n'
        else:
            output += '\n\nNo warnings to report.'

        return output

