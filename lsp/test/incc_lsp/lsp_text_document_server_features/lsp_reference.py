from lsprotocol import types

from incc_lsp.extracts_from_interpreter import LEXER_TOKS
from incc_lsp.extracts_from_interpreter.PARSER_LSP import parse_for_def_ref
from incc_lsp.lsp_server.lsp_pre_server import InCCLanguageServer
from incc_lsp.lsp_server.lsp_server_logging import LOGGING


def find_column(input: str, lexpos: int):
    line_start = input.rfind("\n", 0, lexpos) + 1
    return lexpos - line_start


def get_lsp_def(document, tok_under_courser):
    lsp_defs, lsp_refs = parse_for_def_ref(document.source)

    # defined_at = lsp_defs.entries.get(tok_under_courser)
    entries = lsp_refs.entries.get(tok_under_courser)
    arr = []
    if entries:
        for entry in entries:
            column = find_column(document.source, entry.lexpos)
            LOGGING.info(entry)
            arr.append(
                types.Location(
                    uri=document.uri,
                    range=types.Range(
                        start=types.Position(line=entry.lineno, character=column),
                        end=types.Position(line=entry.lineno, character=column),
                    ),
                )
            )
        return arr
    else:
        return


def create(SERVER: InCCLanguageServer):

    @SERVER.feature(types.TEXT_DOCUMENT_REFERENCES)
    def goto_reference(ls: InCCLanguageServer, params: types.DefinitionParams):
        document = SERVER.workspace.get_text_document(params.text_document.uri)
        current_line = document.lines[params.position.line]
        tok_under_courser = LEXER_TOKS.from_line_match_get_id(
            current_line, params.position.character
        )
        return get_lsp_def(document, tok_under_courser)


# TODO:
# - check if id or other item


# TODO:
# - RESET lineno after first run!!!!
