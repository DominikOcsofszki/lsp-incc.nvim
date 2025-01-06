import re

from incc_interpreter_ue08.LSP.LSP_ENV import EnvLsp, InfoLsp
from lsprotocol import types

from incc_lsp.extracts_from_interpreter.PARSER_LSP import parse_for_def_ref
from incc_lsp.lsp_server.lsp_pre_server import InCCLanguageServer
from incc_lsp.lsp_server.lsp_server_logging import LOGGING


def find_column(input, lexpos):
    line_start = input.rfind("\n", 0, lexpos) + 1
    return lexpos - line_start


def calc(word, combined, new_name: str, text):
    match: list[InfoLsp] = combined.get(word)

    edits: list[types.TextEdit] = []
    # LOGGING.info("INSIDE >>>>>> CALC :::::")

    for item in match:
        LOGGING.info("INSIDE >>>>>> CALC :::::")
        LOGGING.info(item)

        column = find_column(text, item.lexpos)
        edits.append(
            types.TextEdit(
                new_text=new_name,
                range=types.Range(
                    start=types.Position(line=item.lineno, character=column),
                    end=types.Position(line=item.lineno, character=column + len(word)),
                ),
            )
        )
    return edits


# TODO: This also renames item defined in functions with wrong scope


def create(SERVER: InCCLanguageServer):
    @SERVER.feature(types.TEXT_DOCUMENT_RENAME)
    def rename(ls: InCCLanguageServer, params: types.RenameParams):
        """Rename the symbol at the given position."""
        LOGGING.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>!>!!!!!!!!!>>>")
        LOGGING.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>!>!!!!!!!!!>>>")
        doc = ls.workspace.get_text_document(params.text_document.uri)
        word = doc.word_at_position(params.position)
        lsp_defs, lsp_refs = parse_for_def_ref(doc.source)
        edits: list[types.TextEdit] = []
        combined = {
            key: lsp_defs.entries.get(key, []) + lsp_refs.entries.get(key, [])
            for key in set(lsp_defs.entries) | set(lsp_refs.entries)
        }
        # print(combined)

        # matched = combined.get(word)
        # if matched:
        #     edits = []
        edits = calc(word, combined, params.new_name, doc.source)
        # return
        # for linum, line in enumerate(doc.lines):
        #     for match in re.finditer(f"\\b{word}\\b", line):
        #         edits.append(
        #             types.TextEdit(
        #                 new_text=params.new_name,
        #                 range=types.Range(
        #                     start=types.Position(line=linum, character=match.start()),
        #                     end=types.Position(line=linum, character=match.end()),
        #                 ),
        #             )
        #         )

        return types.WorkspaceEdit(changes={params.text_document.uri: edits})
