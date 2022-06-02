def format(code, line_context='', path='', extra_info=''):
    msg = ''
    if path:
        msg += path + ': '

    msg += code

    if extra_info:
        msg += '\n' + extra_info

    msg += line_context
    return msg


class Diagnostics:

    def __init__(self):
        self.errors = []
        self.warnings = []

    def add_warning(self, message):
        self.warnings.append(message)

    def add_error(self, message):
        self.errors.append(message)

    def to_string(self):
        output = ''
        if len(self.errors):
            output += 'ERRORS:\n'

            for error in self.errors:
                output += f'\n{error}\n'
        else:
            output += 'No errors detected.\n'

        if len(self.warnings):
            output += '\n\nWARNINGS:\n'

            for warning in self.warnings:
                output += f'\n{warning}\n'
        else:
            output += '\n\nNo warnings to report.'

        return output
