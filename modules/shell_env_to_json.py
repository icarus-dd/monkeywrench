import io
import json
import re


class ShellEnvToJSON:

    def __init__(self):
        self.__json_dict: dict = {}
        self.comment_strings: list[str] = ['#']
        self.line_separators: list[str] = [';', '&&']
        self.exports_only = True

    def __len__(self):
        return len(self.__json_dict)

    def __str__(self):
        return json.dumps(self.__json_dict)

    def scan_file(self, file: str | io.TextIOBase) -> dict:
        __json_dict = dict()
        __f = None
        if isinstance(file, io.TextIOBase):
            __f = file
        else:
            __f = open(file, 'r')

        __lines = __f.readlines()
        __f.close()
        __regex = '|'.join(self.line_separators)
        for __line in __lines:
            for __exp in re.split(__regex, __line):
                __exp = __exp.strip()

                # Strip comments
                for __c in self.comment_strings:
                    __exp = __exp.split(__c)[0]

                if len(__exp) == 0:
                    continue

                if self.exports_only and __exp.split(' ')[0].strip() != 'export':
                    continue
                else:
                    __exp = __exp.split(' ', 1)[-1].strip()
                    __match = re.match('^\w+=.*', __exp)

                    if __match:
                        (__var, __value) = __exp.split('=', 1)
                        self.__json_dict[__var] = __value

        return self.__json_dict
