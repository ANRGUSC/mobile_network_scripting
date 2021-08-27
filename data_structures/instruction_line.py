import re

class InstructionLine:
    def __init__(self, line):
        line = line.strip().replace(" ", "")
        split = re.split(r'=|\(|\)', line)[:-1]
        if len(split) == 3:
            self.initialized_variable = split[0]
        else:
            self.initialized_variable = None
        self.function_name = split[-2]

        parameters = split[-1]
        self.param_list = parameters.split(",") if parameters else []


