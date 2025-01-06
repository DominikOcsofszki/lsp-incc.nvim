from lsprotocol import types
from pygls.lsp.server import LanguageServer

from incc_lsp.extracts_from_interpreter import LEXER_TOKS
from incc_lsp.extracts_from_interpreter.interpreter_class_info import (
    InccInterpreterImported,
)

__inccInterpreterImported = InccInterpreterImported()
lexer_reserved_words_dict = {
    item: "keyword" for item in __inccInterpreterImported.LEXER_reserved_words
}
lexer_reserved_words_dict.update(
    {
        item: "keyword"
        for item in __inccInterpreterImported.LEXER_reserved_keywords_from_import
    }
)

__operators_binop: list[str] = [
    "DIVIDE",
    "EQS",
    "GE",
    "GT",
    "LE",
    "LPAREN",
    "LT",
    "MINUS",
    "NEQS",
    "PLUS",
    "TIMES",
    "ASSIGN",
    "RIGHT_ARROW",
    "BACKSLASH",
]
operators_op_dict = {item: "operator" for item in __operators_binop}

literal_tokens: list[str] = [
    "RBRACE",
    "RBRACKET",
    "RPAREN",
    "LBRACE",
    "LBRACKET",
    "COMMA",
    "DOT",
    "SEMICOLON",
]
literal_tokens_dict = {item: "operator" for item in literal_tokens}


class InCCLanguageServer(LanguageServer):
    CONFIGURATION_SECTION: str = "pygls.incc-server"
    token_modifiers: list[str] = [
        "declaration",
        "definition",
        "deprecated",
    ]
    token_types: list[str] = [
        "namespace",
        "operator",
        "comment",
        "string",
        "number",
        "struct",
        "parameter",
        "variable",
        "property",
        "keyword",
        "method",
    ]

    token_types_dict: dict[str, str] = {
        "NUMBER": "number",
        "STRING": "string",
        "CHAR": "string",
        # "COMMENT": "comment",
        "COMMENT": "namespace",
        "STRUCT": "struct",
        "IDENT": "variable",
    }
    extra_keywords = ["import", "dict", "["]
    lexer_reserved_words_dict.update({item: "keyword" for item in extra_keywords})

    lexer_reserved_words_dict = lexer_reserved_words_dict
    token_types_dict.update(lexer_reserved_words_dict)
    token_types_dict.update(operators_op_dict)
    token_types_dict.update(literal_tokens_dict)
    ic(lexer_reserved_words_dict)
    # ic(lexer_reserved_words_dict)

    def __init__(self, *args):
        super().__init__(*args)

    def parseHighlightTokens(
        self, params: types.SemanticTokensParams
    ) -> list[LEXER_TOKS.InccSemanticToken]:
        document = self.workspace.get_text_document(params.text_document.uri)
        tokens = LEXER_TOKS.getTokensLexerSemanticTokens(document.source)
        return tokens


if __name__ == "__main__":
    iii = InCCLanguageServer()
    # "keyword",
    # "parameter",
    # "property",
    # "operator",
    # "namespace",
    # "method",

    # token_types_all: list[str] = [
    #     "namespace",
    #     "operator",
    #     "comment",
    #     "string",
    #     "number",
    #     "struct",
    #     "parameter",
    #     "variable",
    #     "property",
    #     "keyword",
    #     "method",
    #     "enumMember",
    #     "event",
    #     "function",
    #     "macro",
    #     "modifier",
    #     "regexp",
    #     "decorator",
    #     "type",
    #     "class",
    #     "enum",
    #     "interface",
    #     "typeParameter",
    # ]
