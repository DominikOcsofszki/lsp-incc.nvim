from incc_lsp.lsp_server.lsp_pre_server import InCCLanguageServer
from incc_lsp.lsp_text_document_server_features import (
    lsp_completion,
    lsp_definition,
    lsp_diagnostic,
    lsp_hover,
    lsp_reference,
    lsp_rename,
    lsp_semantic_tokens_full,
)

# from incc_lsp.lsp_text_document_server_features.import_lsp_text_document import (
#     InCCLanguageServer,
# )

# from lsprotocol import types
EXPERIMENTAL = False


def run():
    INCC_SERVER = InCCLanguageServer("incc-server", "v0.1")
    lsp_completion.create(INCC_SERVER)
    lsp_definition.create(INCC_SERVER)
    lsp_diagnostic.create(INCC_SERVER)
    lsp_diagnostic.create_on_open(INCC_SERVER)
    lsp_reference.create(INCC_SERVER)
    lsp_hover.create(INCC_SERVER)
    lsp_semantic_tokens_full.create(INCC_SERVER)
    if EXPERIMENTAL:
        lsp_rename.create(INCC_SERVER)
    INCC_SERVER.start_io()


#
# def run_vs_code():
#     INCC_SERVER = InCCLanguageServer("incc-server", "v0.1")
#     create_lsp_text_document_completion(SERVER=INCC_SERVER)
#     create_lsp_text_document_hover(SERVER=INCC_SERVER)
#     create_go_to_def(SERVER=INCC_SERVER)
#     # Change to Websocket?
#     INCC_SERVER.start_io()


# run()
# run_vs_code()
