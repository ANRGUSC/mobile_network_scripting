import re
from util.util import split_list_with_braces

class InstructionLine:
    def __init__(self, line):
        line = line.strip().replace(" ", "")
        split = re.split(r'=', line)
        if len(split) == 2:
            self.initialized_variable = split[0]
        else:
            self.initialized_variable = None

        first_open_paren = split[-1].find('(')
        last_end_paren = split[-1].rfind(')')
        self.function_name = split[-1][0:first_open_paren]

        parameters = split[-1][first_open_paren + 1:last_end_paren]
        param_list = split_list_with_braces(parameters)
        self.param_list = param_list if parameters else []
