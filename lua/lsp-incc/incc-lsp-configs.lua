local M = {}


M.CAPABILITIES = require('cmp_nvim_lsp').default_capabilities(vim.lsp.protocol.make_client_capabilities())
M.ON_ATTACH = function(_, bufnr)
	local nmap = function(keys, func, desc)
		if desc then
			desc = 'LSP: ' .. desc
		end

		vim.keymap.set('n', keys, func, { buffer = bufnr, desc = desc })
	end
	vim.api.nvim_buf_create_user_command(bufnr, 'F', function(_)
		vim.lsp.buf.format()
	end, { desc = 'Format current buffer with LSP' })

	nmap('<leader>ga', vim.lsp.buf.code_action, '[C]ode [A]ction')
	nmap('ga', vim.lsp.buf.code_action, '[C]ode [A]ction')
	nmap("<leader>]", function() vim.diagnostic.goto_next() end, '[G]oto [D]iagnostics')
	nmap("]d", function() vim.diagnostic.goto_next() end, '[G]oto [D]iagnostics')
	nmap("<leader>[", function() vim.diagnostic.goto_prev() end, '[G]oto [D]iagnostics')
	nmap("[d", function() vim.diagnostic.goto_prev() end, '[G]oto [D]iagnostics')
	nmap('<leader>gr', vim.lsp.buf.rename, '[R]e[n]ame')
	nmap('<leader>gd', vim.lsp.buf.definition, '[G]oto [D]efinition')
	nmap('gd', vim.lsp.buf.definition, '[G]oto [D]efinition')
	nmap('<leader>gR', require('telescope.builtin').lsp_references, '[G]oto [R]eferences')
	nmap('<leader>gI', vim.lsp.buf.implementation, '[G]oto [I]mplementation')
	nmap('<leader>gD', vim.lsp.buf.type_definition, 'Type [D]efinition')
	nmap('<leader>gs', require('telescope.builtin').lsp_document_symbols, '[D]ocument [S]ymbols')
	nmap('<leader>gh', vim.lsp.buf.hover, 'Hover Documentation')
	nmap('gh', vim.lsp.buf.hover, 'Hover Documentation')
	nmap('<leader>g=', vim.lsp.buf.signature_help, 'Signature Documentation')
end


return M
