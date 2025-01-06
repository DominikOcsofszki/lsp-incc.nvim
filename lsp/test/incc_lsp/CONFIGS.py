from incc_lsp.lsp_text_import_hover import load_from_github

UPDATE_JSON_FROM_GITHUB = True
# UPDATE_JSON_FROM_GITHUB = False

if __name__ == "__main__":
    load_from_github.update_all_hover(UPDATE_JSON_FROM_GITHUB)
