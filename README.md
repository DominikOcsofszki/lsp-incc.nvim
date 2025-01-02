# lsp-incc.nvim



<h1 align='center'>lsp-incc</h1>

<h4 align='center'>Language Server for incc</h4>


## Introduction


## Requirements

- Neovim (>= 0.9)

## Install

- With [lazy.nvim](https://github.com/folke/lazy.nvim)

```lua
require("lazy").setup({
	{
		"DominikOcsofszki/lsp-incc.nvim",
		opts = {
			path = "/Users/dominik/HOME/BA/DEV/MAIN/src/incc_lsp/SERVER_run.sh"
		}
	}
}
```
- or inside plugins/some_name.lua
```lua
return {
    {
		"DominikOcsofszki/lsp-incc.nvim",
		opts = {
			path = "/Users/dominik/HOME/BA/DEV/MAIN/src/incc_lsp/SERVER_run.sh"
		}
	}
}
```

- Change path to current LSP-SERVER

