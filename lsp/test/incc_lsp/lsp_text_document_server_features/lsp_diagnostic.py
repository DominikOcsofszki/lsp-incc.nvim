# from incc_interpreter_ue08.LSP.LSP_ENV import get_lsp_def
from lsprotocol import types

from incc_lsp.extracts_from_interpreter import PARSER_LSP
from incc_lsp.lsp_server.lsp_pre_server import InCCLanguageServer
from incc_lsp.lsp_server.lsp_server_logging import LOGGING


def find_column(input, lexpos):
    line_start = input.rfind("\n", 0, lexpos) + 1
    return lexpos - line_start


def empty_diagnostic_msg(ls, document):
    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=document.uri,
            version=1,
            diagnostics=[],
        )
    )


def publish_all_diagnostics(ls, document, diagnostics):
    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(
            uri=document.uri,
            version=1,
            diagnostics=diagnostics,
            # diagnostics=[diagnostics],
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
    return diagnostics
    # publish_all_diagnostics(ls, document, diagnostics)


def EXTRACT_INFO(message):
    import re

    pattern = r"LexToken\((\w+),'(.*?)',(\d+),(\d+)\)"
    match = re.search(pattern, message)
    line_number, column_number = None, None
    if match:
        token_type = match.group(1)
        token_value = match.group(2)
        line_number = int(match.group(3))
        column_number = int(match.group(4))
        return line_number, column_number
    return line_number, column_number


def get_error_messages(error_msg: str):
    arr = error_msg.split("\n\r")
    return arr


def parse_and_check_for_errors(ls, document):
    try:
        PARSER_LSP.parse_for_def_ref(document.source)
        empty_diagnostic_msg(ls, document)
    except SyntaxError as err:
        diagnostics: list[types.Diagnostic] = []
        error_msg = err.msg
        arr_err_msgs = get_error_messages(err.msg)
        LOGGING.info("=======================================")
        LOGGING.info("=======================================")
        LOGGING.info(arr_err_msgs)
        LOGGING.info("=======================================")
        LOGGING.info("=======================================")

        for error_msg in arr_err_msgs:
            LOGGING.info(error_msg)
            if error_msg:
                linenr, column = EXTRACT_INFO(error_msg)
                LOGGING.info("=======================================")
                LOGGING.info(linenr, column)
                if linenr and column:
                    diagnostics.append(
                        diagnostic_msg(
                            # ls, document, linenr, params.position.character, error_msg
                            ls,
                            document,
                            linenr,
                            column,
                            error_msg,
                        )
                    )
        publish_all_diagnostics(ls, document, diagnostics)
        return


def create_on_open(SERVER: InCCLanguageServer):
    @SERVER.feature(types.TEXT_DOCUMENT_DID_OPEN)
    def did_open(ls: InCCLanguageServer, params: types.DidOpenTextDocumentParams):
        """Parse each document when it is changed"""
        document = SERVER.workspace.get_text_document(params.text_document.uri)
        parse_and_check_for_errors(ls, document)


def create(SERVER: InCCLanguageServer):
    @SERVER.feature(types.TEXT_DOCUMENT_DID_CHANGE)
    def did_change(ls: InCCLanguageServer, params: types.DidOpenTextDocumentParams):
        """Parse each document when it is changed"""
        document = SERVER.workspace.get_text_document(params.text_document.uri)
        parse_and_check_for_errors(ls, document)
