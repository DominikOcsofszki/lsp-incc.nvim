# lsp-incc.nvim



<h1 align='center'>lsp-incc</h1>

<h4 align='center'>Language Server for incc</h4>


## Introduction


## Requirements

- Neovim (>= 0.9)

## Install

- With [lazy.nvim](https://github.com/folke/lazy.nvim)
- Change path to current LSP-SERVER

```lua
return {
	{
		"DominikOcsofszki/lsp-incc.nvim",
		opts = {
			-- path = { "incc_lsp" } -- DEFAULT
		},
		dependencies = { 
        "hrsh7th/cmp-nvim-lsp", 
        "neovim/nvim-lspconfig" 
        }
	}
}
```

### per (pipx)[https://github.com/pypa/pipx]:

- options:
```sh
brew install pipx
sudo apt install pipx
sudo dnf install pipx
sudo pacman -S python-pipx
python3 -m pip install --user pipx
```
```sh
sh install_lsp_pipx.sh
```


