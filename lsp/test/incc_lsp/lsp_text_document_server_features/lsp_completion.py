from lsprotocol import types

from incc_lsp.extracts_from_interpreter import LEXER_TOKS
from incc_lsp.extracts_from_interpreter.PARSER_LSP import get_struct_infos
from incc_lsp.lsp_server.lsp_pre_server import InCCLanguageServer
from incc_lsp.lsp_server.lsp_server_logging import LOGGING
from incc_lsp.lsp_text_document_server_features.helper_lsp_completions import III


def add_helper_reserved_word():
    return ["h." + str.lower(x) for x in III.LEXER_reserved_words]


def get_helper_CompletionItem() -> list[types.CompletionItem]:
    auto_completion = add_helper_reserved_word()
    return [
        types.CompletionItem(label=x, kind=18, detail="TEST") for x in auto_completion
    ]


def get_CompletionItem():
    auto_completion = [str.lower(x) for x in III.LEXER_reserved_words]
    return [types.CompletionItem(label=x, kind=14) for x in auto_completion]


def get_IDs_from_data(data: str):
    arr = LEXER_TOKS.getTokenFromDataDepth(data)
    arr = [x.value for x in arr]
    arr = list(set(arr))
    return [types.CompletionItem(label=x, kind=18) for x in arr]


def filter_comp_items(all_comp_items: list[types.CompletionItem]):
    all_comp_items.sort(key=lambda x: x.label[0])
    return all_comp_items


def get_struct_context(data):
    arr = LEXER_TOKS.getTokenFromDataDepth(data)
    arr = [x.value for x in arr]
    arr = list(set(arr))
    return [types.CompletionItem(label=x, kind=18) for x in arr]


def create(SERVER: InCCLanguageServer):
    @SERVER.feature(
        types.TEXT_DOCUMENT_COMPLETION,
        types.CompletionOptions(trigger_characters=["."]),
    )
    def completions(params: types.CompletionParams):

        document = SERVER.workspace.get_text_document(params.text_document.uri)
        lines_up_to_cursor = document.lines[0 : params.position.line]
        file_concated = "".join(lines_up_to_cursor)
        LOGGING.info("===========================================xxx============")
        if params.context:
            if params.context.trigger_character == ".":
                # res = parse_for_struct(file_concated)
                res = [x for x in get_struct_infos("").get_keys()]
                return [types.CompletionItem(label=x, kind=18) for x in res]

                LOGGING.info(
                    "===========>>>>>>================================xxx============"
                )
                LOGGING.info(res)
                return res
                # return get_struct_context(file_concated)

        comp_items = get_IDs_from_data(file_concated)
        all_comp_items = get_CompletionItem() + comp_items
        all_comp_items_sorted = filter_comp_items(all_comp_items)

        return all_comp_items_sorted
