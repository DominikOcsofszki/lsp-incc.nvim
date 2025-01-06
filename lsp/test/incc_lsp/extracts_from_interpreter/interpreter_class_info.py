from incc_interpreter_ue08 import interpreter
from incc_interpreter_ue08.lexer import lexer
from lsprotocol import types as types


class InccInterpreterImported:
    def __init__(self):
        _all_import_keys = [x for x in interpreter.set_up_env().vars.keys()]
        self.LEXER_reserved_keywords_from_import = [
            x for x in _all_import_keys if not str.isupper(x)
        ]
        # self.LEXER_reserved_keywords_from_import = [
        #     x.upper() for x in self.LEXER_reserved_keywords_from_import
        # ]
        self.LEXER_import_modul = lexer
        self.LEXER_reserved_words = lexer.reserved_words
        self.LEXER_tokens = lexer.tokens

    def print_all_infos(self, print_f=print):
        for key in self.__dict__:
            print_f(key, self.__dict__[key])
            print_f()
            # interpreter_tokens.lexer_dict.get(key)

    # self.reserved_help = {}
    # self.import_toks_to_translate = [x for x in _all_import_keys if str.isupper(x)]

    #     self.COMPLETION_ITEMS_reserved_words_with_help_info = (
    #         self.add_info_to_reserved_words(self.reserved_help)
    #     )
    #
    # def printm(self, print_f=print):
    #     print_f(self.LEXER_reserved_words)
    #     print_f(self.LEXER_tokens)

    #

    #
    # def check_for_reserved_words(self, x):
    #     return x in self.LEXER_reserved_words
    #
    # def check_for_tokens(self, x):
    #     return x in self.LEXER_tokens
    #
    # def add_info_to_reserved_words(self, reserved):
    #     return [
    #         types.CompletionItem(label=x, kind=14, detail=self.reserved_help.get(x))
    #         for x in self.LEXER_reserved_words
    #     ]


if __name__ == "__main__":
    III = InccInterpreterImported()
    III.print_all_infos()
