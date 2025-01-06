from incc_interpreter_ue08.lexer import lexer
from incc_interpreter_ue08.LSP import LSP_ENV
from incc_interpreter_ue08.LSP.LSP_ENV import get_lsp_def, get_lsp_ref
from incc_interpreter_ue08.parser import parser as PARSER


def get_struct_infos(text):
    # PARSER.parse_expr(text)
    struc_ = LSP_ENV.get_lsp_structs()
    print(struc_)
    return struc_


def parse_for_def_ref(text):
    PARSER.parse_expr(text)
    def_ = get_lsp_def()
    ref_ = get_lsp_ref()
    # struc_ = LSP_ENV.get_lsp_structs()
    print(def_)
    print(ref_)
    return def_, ref_


if __name__ == "__main__":
    text = r""" 
{
x = 123;
s = struct {
	.x = 7;
	.set_x = \A -> .x = A
};
s;
x;
s;
x=123;
x;
x

}
"""
    parse_for_def_ref(text)
    get_struct_infos(text)
