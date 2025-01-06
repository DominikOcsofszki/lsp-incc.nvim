from lsprotocol import types

from incc_lsp.extracts_from_interpreter.LEXER_TOKS import InccSemanticToken
from incc_lsp.lsp_server.lsp_pre_server import InCCLanguageServer
from incc_lsp.lsp_server.lsp_server_logging import LOGGING

# TODO: Compare speed inside func or outside
lexer_reserved_words_dict = InCCLanguageServer.lexer_reserved_words_dict.keys()


def get_TokenTypes(token, SERVER: InCCLanguageServer):
    if token.tok_type == "IDENT" and token.text in lexer_reserved_words_dict:
        highlight_type = "keyword"
    else:
        highlight_type = SERVER.token_types_dict.get(token.tok_type, "namespace")
    ret_index = SERVER.token_types.index(highlight_type)
    return ret_index


def create(SERVER: InCCLanguageServer):
    @SERVER.feature(
        types.TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
        types.SemanticTokensLegend(
            token_types=InCCLanguageServer.token_types,
            token_modifiers=InCCLanguageServer.token_modifiers,
        ),
    )
    def semantic_tokens_full(
        incc_server: InCCLanguageServer, params: types.SemanticTokensParams
    ):
        """Return the semantic tokens for the entire document"""
        tokens: list[InccSemanticToken] = incc_server.parseHighlightTokens(params)
        data = [
            item
            for token in tokens
            for item in [
                token.line_offset,
                token.pos_offset,
                len(token.text),
                get_TokenTypes(token, SERVER),
                0,
            ]
        ]

        semanticTokens = types.SemanticTokens(data=data)
        # LOGGING.info(msg=semanticTokens.data)
        return semanticTokens


# TODO: usw dict-for improvement? TODO: Compare later
# def get_TokenTypes(token, SERVER: InCCLanguageServer):
#     match token.tok_type:
#         case "IDENT":
#             token_type = "variable"
#         case tok if tok in III.LEXER_reserved_words:
#             token_type = "keyword"
#         case "CHAR":
#             token_type = "string"
#         case "STRING":
#             token_type = "string"
#         case "NUMBER":
#             token_type = "number"
#         case "COMMENT":
#             token_type = "namespace"
#         # case tok if tok in III.LEXER_tokens:
#         #     token_type = "namespace"
#         case _:
#             # token_type = None
#             token_type = "namespace"
#             token_type = "number"
#
#     ret_index = SERVER.token_types.index(token_type)
#     return ret_index

# TODO: COMPARE!!!!
# for token in tokens:
#     data.extend(
#         [
#             token.line_offset,
#             token.pos_offset,
#             len(token.text),
#             get_TokenTypes(token, SERVER),
#             0,
#             # reduce(operator.or_, token.tok_modifiers, 0),
#         ]
#     )
