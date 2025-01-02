-- local LSP_IMPORTS  = require("lsp-incc-nvim.lsp-all-import")

local M            = {}
local CMD_INCC24   = "/Users/dominik/HOME/BA/DEV/MAIN/src/incc_lsp/SERVER.sh"
local DEFAULT_OPTS = {
	path = CMD_INCC24,
	CAPABILITIES = require('cmp_nvim_lsp').default_capabilities(vim.lsp.protocol.make_client_capabilities()),
	ON_ATTACH = M.ON_ATTACH,
	SETTINGS = {}
}

local function merge_options(conf)
	return vim.tbl_deep_extend("force", DEFAULT_OPTS, conf or {})
end
local create_autocmd_ft_incc   = function()
	vim.filetype.add({
		extension = {
			incc = 'incc',
			incc24 = 'incc',
		},
	})
end

local create_incc24_lsp_config = function(conf)
	local merged_config = merge_options(conf)
	if not require 'lspconfig.configs'.incc24_lsp then
		require 'lspconfig.configs'.incc24_lsp = {
			default_config = {
				cmd = { merged_config.path },
				filetypes = { 'tx', 'incc', 'incc24' },
				root_dir = function(fname)
					return require 'lspconfig'.util.find_git_ancestor(fname)
				end,
				settings = merged_config.SETTINGS,
				on_attach = merged_config.ON_ATTACH,
				capabilities = merged_config.CAPABILITIES,
			},
		}
	end
	require("lspconfig").incc24_lsp.setup {}
end

M.setup                        = function(conf)
	create_autocmd_ft_incc()
	create_incc24_lsp_config(conf)
end
return M
