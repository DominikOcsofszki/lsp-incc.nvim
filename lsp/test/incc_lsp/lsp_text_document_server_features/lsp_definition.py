from lsprotocol import types

# from incc_interpreter_ue08.LSP.LSP_ENV import lsp_ref, lsp_def
from incc_lsp.extracts_from_interpreter import LEXER_TOKS
from incc_lsp.extracts_from_interpreter.PARSER_LSP import parse_for_def_ref
from incc_lsp.lsp_server.lsp_pre_server import InCCLanguageServer
from incc_lsp.lsp_server.lsp_server_logging import LOGGING

# from incc_lsp.lsp_text_document_server_features.import_lsp_text_document import (
#     InCCLanguageServer,
#     types,
# )


def find_column(input, lexpos):
    line_start = input.rfind("\n", 0, lexpos) + 1
    return lexpos - line_start


def helper_create_range_items(tok):
    # end = character - (match.span()[1] - match.span()[0])
    # char_pos: int = tok.pos
    char_pos: int = 0
    # line_nr: int = tok.lineno - 2
    line_nr: int = tok.lineno - 1
    range_ = types.Range(
        start=types.Position(line=line_nr, character=char_pos),
        end=types.Position(line=line_nr, character=char_pos),
    )
    return range_


def empty_diagnostic_msg(ls, document):
    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=document.uri,
            version=1,
            diagnostics=[],
        )
    )


def diagnostic_msg(ls, document, line, character, msg):
    diagnostics = types.Diagnostic(
        message=msg,
        severity=types.DiagnosticSeverity.Error,
        range=types.Range(
            start=types.Position(line=line, character=character),
            end=types.Position(line=line, character=character),
        ),
    )
    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=document.uri,
            version=1,
            diagnostics=[diagnostics],
        )
    )


def get_lsp_def(document, tok_under_courser):
    lsp_defs, lsp_refs = parse_for_def_ref(document.source)

    defined_at = lsp_defs.entries.get(tok_under_courser)
    LOGGING.info(tok_under_courser)
    if defined_at:
        column = find_column(document.source, defined_at[-1].lexpos)
        LOGGING.info(defined_at[-1])
        return [
            types.Location(
                uri=document.uri,
                range=types.Range(
                    start=types.Position(line=defined_at[-1].lineno, character=column),
                    end=types.Position(line=defined_at[-1].lineno, character=column),
                ),
            )
        ]

    else:
        return


def EXTRACT_INFO(message):
    import re

    pattern = r"LexToken\((\w+),'(.*?)',(\d+),(\d+)\)"
    match = re.search(pattern, message)

    if match:
        token_type = match.group(1)
        token_value = match.group(2)
        line_number = int(match.group(3))
        column_number = int(match.group(4))
        return line_number, column_number
    return line_number, column_number


def create(SERVER: InCCLanguageServer):

    @SERVER.feature(types.TEXT_DOCUMENT_DEFINITION)
    def goto_definition(ls: InCCLanguageServer, params: types.DefinitionParams):
        document = SERVER.workspace.get_text_document(params.text_document.uri)
        current_line = document.lines[params.position.line]
        tok_under_courser = LEXER_TOKS.from_line_match_get_id(
            current_line, params.position.character
        )
        LOGGING.info(tok_under_courser)
        # return get_lsp_def(document, tok_under_courser)
        try:
            items = get_lsp_def(document, tok_under_courser)
            empty_diagnostic_msg(ls, document)

            return items
        except SyntaxError as err:
            error_msg = err.msg
            if error_msg:
                linenr, column = EXTRACT_INFO(err.msg)
                diagnostic_msg(
                    # ls, document, linenr, params.position.character, error_msg
                    ls,
                    document,
                    linenr,
                    column,
                    error_msg,
                )
                return


def create_old(SERVER: InCCLanguageServer):

    @SERVER.feature(types.TEXT_DOCUMENT_DEFINITION)
    def goto_definition(ls: InCCLanguageServer, params: types.DefinitionParams):
        LOGGING.info("=============================================================")
        LOGGING.info("===========types.TEXT_DOCUMENT_DEFINITION====================")

        doc = ls.workspace.get_text_document(params.text_document.uri)
        document = SERVER.workspace.get_text_document(params.text_document.uri)
        current_line = document.lines[params.position.line]
        lines_up_to = document.lines[0 : params.position.line]
        tok_under_courser = LEXER_TOKS.from_line_match_get_id(
            current_line, params.position.character
        )
        # all_tokens = LEXER_TOKS.getTokens_Definition(document.source)
        # LOGGING.info("================all_tokens:" + str(all_tokens))
        lsp_defs, lsp_refs = parse_for_def_ref(document.source)
        # lsp_defs, lsp_refs = parse_for_def_ref("".join(lines_up_to))
        # lsp_defs, lsp_refs = parse_for_def_ref("")

        LOGGING.info(lsp_defs)
        defined_at = lsp_defs.entries.get(tok_under_courser)
        LOGGING.info(defined_at)
        if defined_at:
            LOGGING.info(defined_at[-1])
            return [
                types.Location(
                    uri=doc.uri,
                    range=types.Range(
                        start=types.Position(
                            line=defined_at[-1].lineno, character=defined_at[-1].lexpos
                        ),
                        end=types.Position(
                            line=defined_at[-1].lineno, character=defined_at[-1].lexpos
                        ),
                    ),
                )
            ]
        else:
            return
        LOGGING.info("lsp_defs:" + str(lsp_defs))
        # exit()
        filtered_results = [tok for tok in all_tokens if tok.value == tok_under_courser]
        LOGGING.info("================filtered_results:" + str(filtered_results))

        if not tok_under_courser:
            return

        # x = document.source.find(tok_under_courser)
        # finditer  Return an iterator yielding a Match object for each match.

        # results = re.finditer("c", document.source)
        for x in filtered_results:
            LOGGING.info(">>>>>>>>>>>>>" + str(x))

        ranges_ = [helper_create_range_items(tok) for tok in filtered_results]

        LOGGING.info("=============================================================")

        return [types.Location(uri=doc.uri, range=range_) for range_ in ranges_]
        # return [
        #     types.Location(uri=doc.uri, range=range_),
        #     # types.Location(uri=doc.uri, range=range_2),
        # ]


# TODO:
# - check if id or other item


# TODO:
# - RESET lineno after first run!!!!
