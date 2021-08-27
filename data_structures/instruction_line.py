import re


def split_list_with_braces(string_to_split):
    trailing_index = 0
    param_list = []
    paren_count = 0
    bracket_count = 0
    for index, char in enumerate(string_to_split):
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        elif char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
        elif char == ',':
            if paren_count == 0 and bracket_count == 0:
                param_list.append(string_to_split[trailing_index:index])
                trailing_index = index + 1
    param_list.append(string_to_split[trailing_index:len(string_to_split)])
    return param_list


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
        # trailing_index = 0
        # param_list = []
        # paren_count = 0
        # bracket_count = 0
        # for index, char in enumerate(parameters):
        #     if char == '(':
        #         paren_count += 1
        #     elif char == ')':
        #         paren_count -= 1
        #     elif char == '[':
        #         bracket_count += 1
        #     elif char == ']':
        #         bracket_count -= 1
        #     elif char == ',':
        #         if paren_count == 0 and bracket_count == 0:
        #             param_list.append(parameters[trailing_index:index])
        #             trailing_index = index + 1
        # param_list.append(parameters[trailing_index:len(parameters)])
        self.param_list = param_list if parameters else []
