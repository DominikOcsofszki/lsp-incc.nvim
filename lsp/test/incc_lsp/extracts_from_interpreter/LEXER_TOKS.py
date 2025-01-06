import re
from dataclasses import dataclass

from ply.lex import Lexer, LexToken

from incc_lsp.lsp_server.lsp_server_logging import LOGGING
from incc_lsp.lsp_text_document_server_features.helper_lsp_completions import III


@dataclass
class InccSemanticToken:
    line_offset: int
    pos_offset: int
    text: str
    tok_type: str


from incc_interpreter_ue08.lexer.lexer import lexer, lsp_lexer

# III_lexer = III.LEXER_import_modul.lexer
III_lexer = lexer
# III_lexer = lsp_lexer


@dataclass
class LexTokenInfo(LexToken):
    value: str
    lineno: int
    lexpos: int
    lexer: Lexer
    type: str


def get_sem_tok(
    tok: LexTokenInfo, prev_line: int, prev_pos: int
) -> tuple[InccSemanticToken, int, int]:
    line_offset = tok.lineno - prev_line
    pos_offset = tok.lexpos - prev_pos
    text = tok.value
    tok_type = tok.type
    _sem_tok = InccSemanticToken(
        line_offset=line_offset,
        pos_offset=pos_offset,
        text=text,
        tok_type=tok_type,
    )
    _prev_line, _prev_pos = tok.lineno, tok.lexpos
    return _sem_tok, _prev_line, _prev_pos


# line_start_pos


def get_sem_tok_new(
    tok: LexTokenInfo, prev_line: int, prev_pos: int
) -> tuple[InccSemanticToken, int, int]:
    line_offset = tok.lineno - prev_line
    if line_offset > 0:
        if hasattr(tok, "lexer"):
            pos_offset = tok.lexpos - tok.lexer.line_start_pos
            LOGGING.info(tok.__dict__.get("line_start_pos"))
        else:
            pos_offset = 0
            LOGGING.info(tok.__dict__.get("line_start_pos"))
            LOGGING.info(tok.__dict__)
            if tok.__dict__.get("line_start_pos"):
                LOGGING.info(tok.line_start_pos)
                pos_offset = tok.lexpos - tok.line_start_pos

            # line_start_pos
        # pos_offset = tok.lexpos - tok.line_start_pos
    else:
        pos_offset = tok.lexpos - prev_pos
    text = tok.value
    tok_type = tok.type
    # LOGGING.info(tok_type)
    _sem_tok = InccSemanticToken(
        line_offset=line_offset,
        pos_offset=pos_offset,
        text=text,
        tok_type=tok_type,
    )
    _prev_line, _prev_pos = tok.lineno, tok.lexpos
    return _sem_tok, _prev_line, _prev_pos


def getTokensLexerSemanticTokens(data: str) -> list[InccSemanticToken]:
    # lexer = III_lexer
    lexer = lsp_lexer
    lexer.input(data)
    lexer.lineno = 1
    all_tok: list[InccSemanticToken] = []
    prev_line: int = 1
    prev_pos: int = 0

    while True:
        tok: LexTokenInfo | None = lexer.token()
        if tok:
            # if tok.__dict__.get("lexer"):
            # _sem_tok, _prev_line, _prev_pos = get_sem_tok(tok, prev_line, prev_pos)
            _sem_tok, _prev_line, _prev_pos = get_sem_tok_new(tok, prev_line, prev_pos)
            sem_tok, prev_line, prev_pos = _sem_tok, _prev_line, _prev_pos
            all_tok.append(sem_tok)
        if not tok:
            break
    return all_tok


def filter_for_items(toks: list[str], pos_nr: int) -> str | None:
    # REGEX starts at pos 1 and lsp  at 0
    pos_nr = pos_nr + 1
    for x in toks:
        if pos_nr >= x.start() and pos_nr <= x.end():
            # print("yey")
            return x.group()


def getAllTokens(data: str) -> list[re.Match]:
    lexer = III_lexer
    lexer = lsp_lexer

    lexer.input(data)
    all_tok: list[any] = []

    while True:
        tok = lexer.token()
        if tok:
            if tok.__dict__.get("lexer"):
                lexmatch = tok.__dict__.get("lexer").__dict__.get("lexmatch")
                all_tok.append(lexmatch)
        if not tok:
            break
    return all_tok


def from_line_match_get_id(line: str, char_pos: int) -> str:
    res = getAllTokens(line)
    item_under_cursor = filter_for_items(res, char_pos)
    return item_under_cursor


def getTokens_Definition(data: str) -> list[any]:
    lexer = III_lexer
    lexer.lineno = 1
    lexer.input(data)
    all_tok: list[any] = []

    while True:
        tok = lexer.token()
        if tok:
            if tok.__dict__.get("lexer"):
                all_tok.append(tok)
        if not tok:
            break
    return all_tok


def getTokenFromDataDepth(data: str) -> list[LexTokenInfo]:
    lexer = III_lexer
    lexer.input(data)
    all_ids: list[LexTokenInfo] = []

    while True:
        tok = lexer.token()
        if tok:
            if tok.type == "IDENT":
                info = LexTokenInfo(
                    tok.value, tok.lineno, tok.lexpos, tok.lexer, tok.type
                )
                # info = LexTokenInfo(tok.value, tok.lexpos, depth)
                all_ids.append(info)

        if not tok:
            break
    return all_ids


if __name__ == "__main__":
    data = """{b =123; ca = 1 + c;
               x+a; x= s.x}
    """
    res = getTokensLexerSemanticTokens(data)
    print(res)
