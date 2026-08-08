#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOVA Core — All-in-one interpreter for the KOVA programming language.

This module contains the complete implementation:
  - Token types and lexer
  - AST node definitions
  - Recursive descent parser
  - Tree-walking interpreter
  - Environment (scope chain)
  - Standard library / built-in functions
  - Custom error types
  - Interactive REPL

Author : Nguyen Khoi
Version: 1.0.0
License: MIT
"""

from __future__ import annotations

import copy
import math
import os
import random
import sys
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

KOVA_VERSION = "1.0.0"
KOVA_AUTHOR = "Nguyen Khoi"
RECURSION_LIMIT = 1000
LOOP_LIMIT = 1_000_000
IMPORT_DEPTH_LIMIT = 16

# ANSI colour helpers (used for REPL and error output)
_COLORS_ENABLED = sys.stderr.isatty()

def _clr(code: str, text: str) -> str:
    """Wrap *text* in ANSI colour *code* if colours are enabled."""
    if _COLORS_ENABLED:
        return f"\033[{code}m{text}\033[0m"
    return text

def _red(t: str) -> str:
    return _clr("1;31", t)

def _green(t: str) -> str:
    return _clr("1;32", t)

def _cyan(t: str) -> str:
    return _clr("1;36", t)

def _yellow(t: str) -> str:
    return _clr("1;33", t)

def _bold(t: str) -> str:
    return _clr("1", t)


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — ERROR TYPES
# ═══════════════════════════════════════════════════════════════════════════════

class KovaError(Exception):
    """Base class for all KOVA errors."""

    def __init__(self, message: str, line: int = 0, col: int = 0,
                 source_line: str = "") -> None:
        self.message = message
        self.line = line
        self.col = col
        self.source_line = source_line
        super().__init__(self.format())

    def format(self) -> str:
        header = _red(f"[{type(self).__name__}]")
        loc = ""
        if self.line:
            loc = f" at line {self.line}"
            if self.col:
                loc += f", col {self.col}"
        msg = f"{header}{loc}: {self.message}"
        if self.source_line:
            msg += f"\n  | {self.source_line.rstrip()}"
            if self.col:
                msg += f"\n  | {' ' * max(0, self.col - 1)}^"
        return msg


class KovaSyntaxError(KovaError):
    """Raised when the source code cannot be parsed."""
    pass


class KovaRuntimeError(KovaError):
    """Raised during interpretation."""
    pass


class KovaTypeError(KovaError):
    """Raised on type mismatches."""
    pass


class KovaReturnSignal(Exception):
    """Internal signal used to implement 'yield' (return)."""

    def __init__(self, value: Any) -> None:
        self.value = value
        super().__init__()


class KovaBreakSignal(Exception):
    """Internal signal for 'snap' (break)."""
    pass


class KovaContinueSignal(Exception):
    """Internal signal for 'skip' (continue)."""
    pass


class KovaEjectSignal(Exception):
    """Internal signal for 'eject' (throw)."""

    def __init__(self, value: Any, line: int = 0, col: int = 0) -> None:
        self.value = value
        self.line = line
        self.col = col
        super().__init__(str(value))


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — TOKEN TYPES & LEXER
# ═══════════════════════════════════════════════════════════════════════════════

class TT(Enum):
    """Token types used by the lexer and parser."""

    # Literals
    NUMBER = auto()
    STRING = auto()
    INTERP_STRING = auto()  # string with interpolation parts
    YES = auto()
    NO = auto()
    VOID = auto()

    # Identifiers & keywords
    IDENT = auto()
    GRAB = auto()
    LOCK = auto()
    FORGE = auto()
    YIELD = auto()
    TEST = auto()
    ALSO = auto()
    RIVAL = auto()
    SPIN = auto()
    FROM = auto()
    TO = auto()
    IN = auto()
    ORBIT = auto()
    SNAP = auto()
    SKIP = auto()
    SHAPE = auto()
    EVOLVE = auto()
    SELF = auto()
    PARENT = auto()
    ATTEMPT = auto()
    RESCUE = auto()
    EJECT = auto()
    PULL = auto()
    EXPOSE = auto()
    MORPH = auto()
    DEFER = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    POWER = auto()       # **
    EQ = auto()          # ==
    NEQ = auto()         # !=
    GT = auto()          # >
    LT = auto()          # <
    GTE = auto()         # >=
    LTE = auto()         # <=
    ASSIGN = auto()      # =
    PLUS_EQ = auto()     # +=
    MINUS_EQ = auto()    # -=
    STAR_EQ = auto()     # *=
    SLASH_EQ = auto()    # /=
    PIPE = auto()        # |>
    DOTDOT = auto()      # ..
    ARROW = auto()       # =>
    BAR = auto()         # |
    DOT = auto()         # .

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    NEWLINE = auto()

    # Special
    EOF = auto()


# Map keyword strings to token types
KEYWORDS: Dict[str, TT] = {
    "grab": TT.GRAB,
    "lock": TT.LOCK,
    "forge": TT.FORGE,
    "yield": TT.YIELD,
    "test": TT.TEST,
    "also": TT.ALSO,
    "rival": TT.RIVAL,
    "spin": TT.SPIN,
    "from": TT.FROM,
    "to": TT.TO,
    "in": TT.IN,
    "orbit": TT.ORBIT,
    "snap": TT.SNAP,
    "skip": TT.SKIP,
    "shape": TT.SHAPE,
    "evolve": TT.EVOLVE,
    "self": TT.SELF,
    "parent": TT.PARENT,
    "attempt": TT.ATTEMPT,
    "rescue": TT.RESCUE,
    "eject": TT.EJECT,
    "pull": TT.PULL,
    "expose": TT.EXPOSE,
    "morph": TT.MORPH,
    "defer": TT.DEFER,
    "and": TT.AND,
    "or": TT.OR,
    "not": TT.NOT,
    "yes": TT.YES,
    "no": TT.NO,
    "void": TT.VOID,
}


@dataclass
class Token:
    """A single lexical token."""
    type: TT
    value: Any
    line: int
    col: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:{self.col})"


class Lexer:
    """
    Tokenises KOVA source code.

    Handles:
      - Single-line comments: -- ...
      - Multi-line comments: {-- ... --}
      - String interpolation: "hello {expr}"
      - All operator tokens including ** |> .. =>
      - Number literals (int and float)
      - Unicode identifiers
    """

    def __init__(self, source: str, filename: str = "<stdin>") -> None:
        self.source: str = source
        self.filename: str = filename
        self.pos: int = 0
        self.line: int = 1
        self.col: int = 1
        self.tokens: List[Token] = []
        self._lines = source.split("\n")

    # -- helpers ---------------------------------------------------------------

    def _src_line(self, lineno: int) -> str:
        """Return the source text of a given line (1-based)."""
        if 1 <= lineno <= len(self._lines):
            return self._lines[lineno - 1]
        return ""

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        if idx < len(self.source):
            return self.source[idx]
        return "\0"

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self.pos < len(self.source) and self.source[self.pos] == expected:
            self._advance()
            return True
        return False

    def _error(self, msg: str) -> KovaSyntaxError:
        return KovaSyntaxError(msg, self.line, self.col, self._src_line(self.line))

    # -- public ----------------------------------------------------------------

    def tokenise(self) -> List[Token]:
        """Scan the entire source and return a list of tokens."""
        while self.pos < len(self.source):
            self._skip_whitespace_and_comments()
            if self.pos >= len(self.source):
                break
            ch = self._peek()

            start_line = self.line
            start_col = self.col

            # Newline — we track these so the parser can use them as statement separators
            if ch == "\n":
                self._advance()
                self.tokens.append(Token(TT.NEWLINE, "\\n", start_line, start_col))
                continue

            # Numbers
            if ch.isdigit() or (ch == "." and self._peek(1).isdigit()):
                self._read_number(start_line, start_col)
                continue

            # Strings
            if ch == '"':
                self._read_string(start_line, start_col)
                continue

            # Identifiers / keywords
            if ch.isalpha() or ch == "_" or (ord(ch) > 127):
                self._read_ident(start_line, start_col)
                continue

            # Operators and punctuation
            self._read_operator(start_line, start_col)

        self.tokens.append(Token(TT.EOF, None, self.line, self.col))
        return self.tokens

    # -- scanning methods ------------------------------------------------------

    def _skip_whitespace_and_comments(self) -> None:
        """Skip spaces, tabs, and comments (but NOT newlines)."""
        while self.pos < len(self.source):
            ch = self._peek()
            # Plain whitespace (not newline)
            if ch in (" ", "\t", "\r"):
                self._advance()
                continue
            # Single-line comment: -- ...
            if ch == "-" and self._peek(1) == "-":
                while self.pos < len(self.source) and self._peek() != "\n":
                    self._advance()
                continue
            # Multi-line comment: {-- ... --}
            if ch == "{" and self._peek(1) == "-" and self._peek(2) == "-":
                self._advance()  # {
                self._advance()  # -
                self._advance()  # -
                depth = 1
                while self.pos < len(self.source) and depth > 0:
                    if self._peek() == "-" and self._peek(1) == "-" and self._peek(2) == "}":
                        self._advance()
                        self._advance()
                        self._advance()
                        depth -= 1
                    else:
                        self._advance()
                if depth > 0:
                    raise self._error("Unterminated multi-line comment")
                continue
            break

    def _read_number(self, sl: int, sc: int) -> None:
        """Read an integer or floating-point number literal."""
        start = self.pos
        has_dot = False
        while self.pos < len(self.source):
            ch = self._peek()
            if ch.isdigit():
                self._advance()
            elif ch == "." and not has_dot and self._peek(1) != ".":
                has_dot = True
                self._advance()
            else:
                break
        text = self.source[start:self.pos]
        value: Union[int, float] = float(text) if has_dot else int(text)
        self.tokens.append(Token(TT.NUMBER, value, sl, sc))

    def _read_string(self, sl: int, sc: int) -> None:
        """Read a string literal, handling escape sequences and interpolation."""
        self._advance()  # consume opening "
        parts: List[Any] = []  # list of (str | AST-node) for interpolation
        buf: List[str] = []
        has_interp = False

        while self.pos < len(self.source) and self._peek() != '"':
            ch = self._peek()
            if ch == "\\":
                self._advance()
                esc = self._advance() if self.pos < len(self.source) else ""
                esc_map = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "{": "{", "}": "}"}
                buf.append(esc_map.get(esc, "\\" + esc))
            elif ch == "{":
                # Start of interpolation expression
                has_interp = True
                if buf:
                    parts.append("".join(buf))
                    buf = []
                self._advance()  # consume {
                # Collect tokens until matching }
                expr_start = self.pos
                depth = 1
                while self.pos < len(self.source) and depth > 0:
                    c = self._peek()
                    if c == "{":
                        depth += 1
                    elif c == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    self._advance()
                if depth != 0:
                    raise self._error("Unterminated string interpolation")
                expr_text = self.source[expr_start:self.pos]
                self._advance()  # consume closing }
                parts.append(("expr", expr_text, sl, sc))
            else:
                buf.append(self._advance())

        if self.pos >= len(self.source):
            raise self._error("Unterminated string literal")
        self._advance()  # consume closing "

        if has_interp:
            if buf:
                parts.append("".join(buf))
            self.tokens.append(Token(TT.INTERP_STRING, parts, sl, sc))
        else:
            self.tokens.append(Token(TT.STRING, "".join(buf), sl, sc))

    def _read_ident(self, sl: int, sc: int) -> None:
        """Read an identifier or keyword."""
        start = self.pos
        while self.pos < len(self.source):
            ch = self._peek()
            if ch.isalnum() or ch == "_" or ord(ch) > 127:
                self._advance()
            else:
                break
        text = self.source[start:self.pos]
        tt = KEYWORDS.get(text, TT.IDENT)
        self.tokens.append(Token(tt, text, sl, sc))

    def _read_operator(self, sl: int, sc: int) -> None:
        """Read an operator or punctuation token."""
        ch = self._advance()

        two_char: Dict[str, TT] = {
            "**": TT.POWER,
            "==": TT.EQ,
            "!=": TT.NEQ,
            ">=": TT.GTE,
            "<=": TT.LTE,
            "+=": TT.PLUS_EQ,
            "-=": TT.MINUS_EQ,
            "*=": TT.STAR_EQ,
            "/=": TT.SLASH_EQ,
            "|>": TT.PIPE,
            "..": TT.DOTDOT,
            "=>": TT.ARROW,
        }

        if self.pos < len(self.source):
            pair = ch + self._peek()
            if pair in two_char:
                self._advance()
                self.tokens.append(Token(two_char[pair], pair, sl, sc))
                return

        one_char: Dict[str, TT] = {
            "+": TT.PLUS,
            "-": TT.MINUS,
            "*": TT.STAR,
            "/": TT.SLASH,
            "%": TT.PERCENT,
            "=": TT.ASSIGN,
            ">": TT.GT,
            "<": TT.LT,
            "|": TT.BAR,
            ".": TT.DOT,
            "(": TT.LPAREN,
            ")": TT.RPAREN,
            "{": TT.LBRACE,
            "}": TT.RBRACE,
            "[": TT.LBRACKET,
            "]": TT.RBRACKET,
            ",": TT.COMMA,
            ":": TT.COLON,
            ";": TT.SEMICOLON,
        }

        if ch in one_char:
            self.tokens.append(Token(one_char[ch], ch, sl, sc))
        else:
            raise self._error(f"Unexpected character: '{ch}'")


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — AST NODES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ASTNode:
    """Base for all AST nodes."""
    line: int = 0
    col: int = 0


# -- Literals ------------------------------------------------------------------

@dataclass
class NumberLit(ASTNode):
    value: Union[int, float] = 0

@dataclass
class StringLit(ASTNode):
    value: str = ""

@dataclass
class InterpStringLit(ASTNode):
    """String with interpolation parts: list of (str | ASTNode)."""
    parts: List[Any] = field(default_factory=list)

@dataclass
class BoolLit(ASTNode):
    value: bool = False

@dataclass
class VoidLit(ASTNode):
    pass

@dataclass
class ArrayLit(ASTNode):
    elements: List[ASTNode] = field(default_factory=list)

@dataclass
class MapLit(ASTNode):
    pairs: List[Tuple[ASTNode, ASTNode]] = field(default_factory=list)

# -- Expressions ---------------------------------------------------------------

@dataclass
class Identifier(ASTNode):
    name: str = ""

@dataclass
class SelfExpr(ASTNode):
    pass

@dataclass
class ParentExpr(ASTNode):
    pass

@dataclass
class BinaryOp(ASTNode):
    op: str = ""
    left: ASTNode = field(default_factory=ASTNode)
    right: ASTNode = field(default_factory=ASTNode)

@dataclass
class UnaryOp(ASTNode):
    op: str = ""
    operand: ASTNode = field(default_factory=ASTNode)

@dataclass
class LogicalOp(ASTNode):
    op: str = ""   # "and" / "or"
    left: ASTNode = field(default_factory=ASTNode)
    right: ASTNode = field(default_factory=ASTNode)

@dataclass
class Assignment(ASTNode):
    target: ASTNode = field(default_factory=ASTNode)
    value: ASTNode = field(default_factory=ASTNode)

@dataclass
class CompoundAssignment(ASTNode):
    target: ASTNode = field(default_factory=ASTNode)
    op: str = ""   # +=  -=  *=  /=
    value: ASTNode = field(default_factory=ASTNode)

@dataclass
class CallExpr(ASTNode):
    callee: ASTNode = field(default_factory=ASTNode)
    args: List[ASTNode] = field(default_factory=list)

@dataclass
class IndexExpr(ASTNode):
    obj: ASTNode = field(default_factory=ASTNode)
    index: ASTNode = field(default_factory=ASTNode)

@dataclass
class DotExpr(ASTNode):
    obj: ASTNode = field(default_factory=ASTNode)
    attr: str = ""

@dataclass
class PipeExpr(ASTNode):
    left: ASTNode = field(default_factory=ASTNode)
    right: ASTNode = field(default_factory=ASTNode)

@dataclass
class RangeExpr(ASTNode):
    start: ASTNode = field(default_factory=ASTNode)
    end: ASTNode = field(default_factory=ASTNode)

@dataclass
class LambdaExpr(ASTNode):
    params: List[str] = field(default_factory=list)
    body: ASTNode = field(default_factory=ASTNode)

# -- Statements ----------------------------------------------------------------

@dataclass
class Program(ASTNode):
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class GrabStmt(ASTNode):
    name: str = ""
    value: ASTNode = field(default_factory=ASTNode)

@dataclass
class LockStmt(ASTNode):
    name: str = ""
    value: ASTNode = field(default_factory=ASTNode)

@dataclass
class ForgeStmt(ASTNode):
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class YieldStmt(ASTNode):
    value: ASTNode = field(default_factory=ASTNode)

@dataclass
class TestStmt(ASTNode):
    """if / elif / else chain."""
    condition: ASTNode = field(default_factory=ASTNode)
    body: List[ASTNode] = field(default_factory=list)
    also_branches: List[Tuple[ASTNode, List[ASTNode]]] = field(default_factory=list)
    rival_body: Optional[List[ASTNode]] = None

@dataclass
class SpinFromStmt(ASTNode):
    """spin i from start to end { body }"""
    var: str = ""
    start: ASTNode = field(default_factory=ASTNode)
    end: ASTNode = field(default_factory=ASTNode)
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class SpinInStmt(ASTNode):
    """spin item in collection { body }"""
    var: str = ""
    iterable: ASTNode = field(default_factory=ASTNode)
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class OrbitStmt(ASTNode):
    condition: ASTNode = field(default_factory=ASTNode)
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class SnapStmt(ASTNode):
    pass

@dataclass
class SkipStmt(ASTNode):
    pass

@dataclass
class ShapeStmt(ASTNode):
    name: str = ""
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class EvolveStmt(ASTNode):
    name: str = ""
    parent_name: str = ""
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class AttemptStmt(ASTNode):
    body: List[ASTNode] = field(default_factory=list)
    rescue_var: str = ""
    rescue_body: List[ASTNode] = field(default_factory=list)

@dataclass
class EjectStmt(ASTNode):
    value: ASTNode = field(default_factory=ASTNode)

@dataclass
class PullStmt(ASTNode):
    path: str = ""

@dataclass
class ExposeStmt(ASTNode):
    name: str = ""

@dataclass
class MorphStmt(ASTNode):
    value: ASTNode = field(default_factory=ASTNode)
    arms: List[Tuple[ASTNode, List[ASTNode]]] = field(default_factory=list)  # (pattern, body)
    default_body: Optional[List[ASTNode]] = None

@dataclass
class DeferStmt(ASTNode):
    body: List[ASTNode] = field(default_factory=list)

@dataclass
class ExprStmt(ASTNode):
    expr: ASTNode = field(default_factory=ASTNode)

@dataclass
class IndexAssign(ASTNode):
    obj: ASTNode = field(default_factory=ASTNode)
    index: ASTNode = field(default_factory=ASTNode)
    value: ASTNode = field(default_factory=ASTNode)

@dataclass
class DotAssign(ASTNode):
    obj: ASTNode = field(default_factory=ASTNode)
    attr: str = ""
    value: ASTNode = field(default_factory=ASTNode)

@dataclass
class CompoundIndexAssign(ASTNode):
    obj: ASTNode = field(default_factory=ASTNode)
    index: ASTNode = field(default_factory=ASTNode)
    op: str = ""
    value: ASTNode = field(default_factory=ASTNode)

@dataclass
class CompoundDotAssign(ASTNode):
    obj: ASTNode = field(default_factory=ASTNode)
    attr: str = ""
    op: str = ""
    value: ASTNode = field(default_factory=ASTNode)


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — PARSER
# ═══════════════════════════════════════════════════════════════════════════════

class Parser:
    """
    Recursive-descent parser for KOVA.

    Converts a token list into an AST (Program node).
    Operator precedence (low to high):
      pipe |>
      or
      and
      not
      comparison  == != < > <= >=
      range       ..
      addition    + -
      multiplication * / %
      power       ** (right-assoc)
      unary       - not
      postfix     call () index [] dot .
      primary     literals, identifiers, ( ), lambda
    """

    def __init__(self, tokens: List[Token], source: str = "",
                 filename: str = "<stdin>") -> None:
        self.tokens = tokens
        self.source = source
        self.filename = filename
        self.pos = 0
        self._lines = source.split("\n")

    # -- helpers ---------------------------------------------------------------

    def _src_line(self, lineno: int) -> str:
        if 1 <= lineno <= len(self._lines):
            return self._lines[lineno - 1]
        return ""

    def _cur(self) -> Token:
        return self.tokens[self.pos]

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]  # EOF

    def _at(self, *types: TT) -> bool:
        return self._cur().type in types

    def _eat(self, tt: TT, msg: str = "") -> Token:
        tok = self._cur()
        if tok.type != tt:
            err_msg = msg or f"Expected {tt.name}, got {tok.type.name} ({tok.value!r})"
            raise KovaSyntaxError(err_msg, tok.line, tok.col, self._src_line(tok.line))
        self.pos += 1
        return tok

    def _eat_any(self) -> Token:
        tok = self._cur()
        self.pos += 1
        return tok

    def _skip_newlines(self) -> None:
        while self._at(TT.NEWLINE):
            self.pos += 1

    def _skip_terminators(self) -> None:
        while self._at(TT.NEWLINE, TT.SEMICOLON):
            self.pos += 1

    # -- entry -----------------------------------------------------------------

    def parse(self) -> Program:
        """Parse the full program."""
        self._skip_newlines()
        stmts: List[ASTNode] = []
        while not self._at(TT.EOF):
            stmts.append(self._statement())
            self._skip_terminators()
        return Program(body=stmts, line=1, col=1)

    # -- statements ------------------------------------------------------------

    def _statement(self) -> ASTNode:
        """Parse a single statement."""
        self._skip_newlines()
        tok = self._cur()

        if tok.type == TT.GRAB:
            return self._grab_stmt()
        if tok.type == TT.LOCK:
            return self._lock_stmt()
        if tok.type == TT.FORGE:
            return self._forge_stmt()
        if tok.type == TT.YIELD:
            return self._yield_stmt()
        if tok.type == TT.TEST:
            return self._test_stmt()
        if tok.type == TT.SPIN:
            return self._spin_stmt()
        if tok.type == TT.ORBIT:
            return self._orbit_stmt()
        if tok.type == TT.SNAP:
            self.pos += 1
            return SnapStmt(line=tok.line, col=tok.col)
        if tok.type == TT.SKIP:
            self.pos += 1
            return SkipStmt(line=tok.line, col=tok.col)
        if tok.type == TT.SHAPE:
            return self._shape_stmt()
        if tok.type == TT.EVOLVE:
            return self._evolve_stmt()
        if tok.type == TT.ATTEMPT:
            return self._attempt_stmt()
        if tok.type == TT.EJECT:
            return self._eject_stmt()
        if tok.type == TT.PULL:
            return self._pull_stmt()
        if tok.type == TT.EXPOSE:
            return self._expose_stmt()
        if tok.type == TT.MORPH:
            return self._morph_stmt()
        if tok.type == TT.DEFER:
            return self._defer_stmt()

        # Expression statement (may include assignment)
        return self._expr_statement()

    def _grab_stmt(self) -> GrabStmt:
        tok = self._eat(TT.GRAB)
        name_tok = self._eat(TT.IDENT, "Expected variable name after 'grab'")
        self._eat(TT.ASSIGN, "Expected '=' in grab statement")
        value = self._expression()
        return GrabStmt(name=name_tok.value, value=value, line=tok.line, col=tok.col)

    def _lock_stmt(self) -> LockStmt:
        tok = self._eat(TT.LOCK)
        name_tok = self._eat(TT.IDENT, "Expected constant name after 'lock'")
        self._eat(TT.ASSIGN, "Expected '=' in lock statement")
        value = self._expression()
        return LockStmt(name=name_tok.value, value=value, line=tok.line, col=tok.col)

    def _forge_stmt(self) -> ForgeStmt:
        tok = self._eat(TT.FORGE)
        name_tok = self._eat(TT.IDENT, "Expected function name after 'forge'")
        self._eat(TT.LPAREN, "Expected '(' after function name")
        params: List[str] = []
        if not self._at(TT.RPAREN):
            params.append(self._eat(TT.IDENT, "Expected parameter name").value)
            while self._at(TT.COMMA):
                self.pos += 1
                params.append(self._eat(TT.IDENT, "Expected parameter name").value)
        self._eat(TT.RPAREN, "Expected ')' after parameters")
        body = self._block()
        return ForgeStmt(name=name_tok.value, params=params, body=body,
                         line=tok.line, col=tok.col)

    def _yield_stmt(self) -> YieldStmt:
        tok = self._eat(TT.YIELD)
        value: ASTNode = VoidLit(line=tok.line, col=tok.col)
        if not self._at(TT.NEWLINE, TT.RBRACE, TT.EOF, TT.SEMICOLON):
            value = self._expression()
        return YieldStmt(value=value, line=tok.line, col=tok.col)

    def _test_stmt(self) -> TestStmt:
        tok = self._eat(TT.TEST)
        cond = self._expression()
        body = self._block()
        also_branches: List[Tuple[ASTNode, List[ASTNode]]] = []
        rival_body: Optional[List[ASTNode]] = None
        self._skip_newlines()
        while self._at(TT.ALSO):
            self.pos += 1
            also_cond = self._expression()
            also_body = self._block()
            also_branches.append((also_cond, also_body))
            self._skip_newlines()
        if self._at(TT.RIVAL):
            self.pos += 1
            rival_body = self._block()
        return TestStmt(condition=cond, body=body, also_branches=also_branches,
                        rival_body=rival_body, line=tok.line, col=tok.col)

    def _spin_stmt(self) -> ASTNode:
        tok = self._eat(TT.SPIN)
        var_tok = self._eat(TT.IDENT, "Expected variable name after 'spin'")
        if self._at(TT.FROM):
            # spin i from start to end { }
            self.pos += 1
            start = self._expression()
            self._eat(TT.TO, "Expected 'to' in spin..from..to")
            end = self._expression()
            body = self._block()
            return SpinFromStmt(var=var_tok.value, start=start, end=end,
                                body=body, line=tok.line, col=tok.col)
        elif self._at(TT.IN):
            # spin item in collection { }
            self.pos += 1
            iterable = self._expression()
            body = self._block()
            return SpinInStmt(var=var_tok.value, iterable=iterable,
                              body=body, line=tok.line, col=tok.col)
        else:
            raise KovaSyntaxError("Expected 'from' or 'in' after spin variable",
                                  tok.line, tok.col, self._src_line(tok.line))

    def _orbit_stmt(self) -> OrbitStmt:
        tok = self._eat(TT.ORBIT)
        cond = self._expression()
        body = self._block()
        return OrbitStmt(condition=cond, body=body, line=tok.line, col=tok.col)

    def _shape_stmt(self) -> ShapeStmt:
        tok = self._eat(TT.SHAPE)
        name_tok = self._eat(TT.IDENT, "Expected class name after 'shape'")
        body = self._block()
        return ShapeStmt(name=name_tok.value, body=body,
                         line=tok.line, col=tok.col)

    def _evolve_stmt(self) -> EvolveStmt:
        tok = self._eat(TT.EVOLVE)
        name_tok = self._eat(TT.IDENT, "Expected class name after 'evolve'")
        self._eat(TT.FROM, "Expected 'from' after class name in evolve")
        parent_tok = self._eat(TT.IDENT, "Expected parent class name")
        body = self._block()
        return EvolveStmt(name=name_tok.value, parent_name=parent_tok.value,
                          body=body, line=tok.line, col=tok.col)

    def _attempt_stmt(self) -> AttemptStmt:
        tok = self._eat(TT.ATTEMPT)
        body = self._block()
        self._skip_newlines()
        self._eat(TT.RESCUE, "Expected 'rescue' after attempt block")
        var_tok = self._eat(TT.IDENT, "Expected error variable name after 'rescue'")
        rescue_body = self._block()
        return AttemptStmt(body=body, rescue_var=var_tok.value,
                           rescue_body=rescue_body, line=tok.line, col=tok.col)

    def _eject_stmt(self) -> EjectStmt:
        tok = self._eat(TT.EJECT)
        value = self._expression()
        return EjectStmt(value=value, line=tok.line, col=tok.col)

    def _pull_stmt(self) -> PullStmt:
        tok = self._eat(TT.PULL)
        path_tok = self._eat(TT.STRING, "Expected string path after 'pull'")
        return PullStmt(path=path_tok.value, line=tok.line, col=tok.col)

    def _expose_stmt(self) -> ExposeStmt:
        tok = self._eat(TT.EXPOSE)
        name_tok = self._eat(TT.IDENT, "Expected name after 'expose'")
        return ExposeStmt(name=name_tok.value, line=tok.line, col=tok.col)

    def _morph_stmt(self) -> MorphStmt:
        tok = self._eat(TT.MORPH)
        value = self._expression()
        self._skip_newlines()
        self._eat(TT.LBRACE, "Expected '{' after morph value")
        self._skip_newlines()
        arms: List[Tuple[ASTNode, List[ASTNode]]] = []
        default_body: Optional[List[ASTNode]] = None
        while not self._at(TT.RBRACE, TT.EOF):
            self._skip_newlines()
            if self._at(TT.RBRACE):
                break
            # Check for default arm: _ => ...
            if self._cur().type == TT.IDENT and self._cur().value == "_":
                self.pos += 1
                self._eat(TT.ARROW, "Expected '=>' after '_'")
                self._skip_newlines()
                default_body = self._morph_arm_body()
            else:
                pattern = self._expression()
                self._eat(TT.ARROW, "Expected '=>' after pattern")
                self._skip_newlines()
                body = self._morph_arm_body()
                arms.append((pattern, body))
            self._skip_newlines()
            # Optional comma between arms
            if self._at(TT.COMMA):
                self.pos += 1
            self._skip_newlines()
        self._eat(TT.RBRACE, "Expected '}' to close morph")
        return MorphStmt(value=value, arms=arms, default_body=default_body,
                         line=tok.line, col=tok.col)

    def _morph_arm_body(self) -> List[ASTNode]:
        """Parse the body of a morph arm — either a block or a single statement."""
        self._skip_newlines()
        if self._at(TT.LBRACE):
            return self._block()
        # Single statement
        stmt = self._statement()
        return [stmt]

    def _defer_stmt(self) -> DeferStmt:
        tok = self._eat(TT.DEFER)
        body = self._block()
        return DeferStmt(body=body, line=tok.line, col=tok.col)

    def _block(self) -> List[ASTNode]:
        """Parse a brace-delimited block of statements."""
        self._skip_newlines()
        self._eat(TT.LBRACE, "Expected '{'")
        self._skip_newlines()
        stmts: List[ASTNode] = []
        while not self._at(TT.RBRACE, TT.EOF):
            stmts.append(self._statement())
            self._skip_terminators()
        self._eat(TT.RBRACE, "Expected '}'")
        return stmts

    def _expr_statement(self) -> ASTNode:
        """Parse an expression-statement, which may be an assignment."""
        expr = self._expression()
        # Check for plain assignment: expr = value
        if self._at(TT.ASSIGN):
            self.pos += 1
            val = self._expression()
            if isinstance(expr, Identifier):
                return Assignment(target=expr, value=val, line=expr.line, col=expr.col)
            elif isinstance(expr, IndexExpr):
                return IndexAssign(obj=expr.obj, index=expr.index, value=val,
                                   line=expr.line, col=expr.col)
            elif isinstance(expr, DotExpr):
                return DotAssign(obj=expr.obj, attr=expr.attr, value=val,
                                 line=expr.line, col=expr.col)
            else:
                raise KovaSyntaxError("Invalid assignment target",
                                      expr.line, expr.col, self._src_line(expr.line))
        # Compound assignment: += -= *= /=
        if self._at(TT.PLUS_EQ, TT.MINUS_EQ, TT.STAR_EQ, TT.SLASH_EQ):
            op_tok = self._eat_any()
            val = self._expression()
            op_map = {"+=": "+", "-=": "-", "*=": "*", "/=": "/"}
            op_str = op_map[op_tok.value]
            if isinstance(expr, Identifier):
                return CompoundAssignment(target=expr, op=op_str, value=val,
                                          line=expr.line, col=expr.col)
            elif isinstance(expr, IndexExpr):
                return CompoundIndexAssign(obj=expr.obj, index=expr.index,
                                           op=op_str, value=val,
                                           line=expr.line, col=expr.col)
            elif isinstance(expr, DotExpr):
                return CompoundDotAssign(obj=expr.obj, attr=expr.attr,
                                         op=op_str, value=val,
                                         line=expr.line, col=expr.col)
            else:
                raise KovaSyntaxError("Invalid compound assignment target",
                                      expr.line, expr.col, self._src_line(expr.line))
        return ExprStmt(expr=expr, line=expr.line, col=expr.col)

    # -- expressions (precedence climbing) -------------------------------------

    def _expression(self) -> ASTNode:
        return self._pipe_expr()

    def _pipe_expr(self) -> ASTNode:
        """pipe: or ( '|>' or )*"""
        left = self._or_expr()
        while self._at(TT.PIPE):
            self.pos += 1
            right = self._or_expr()
            left = PipeExpr(left=left, right=right, line=left.line, col=left.col)
        return left

    def _or_expr(self) -> ASTNode:
        left = self._and_expr()
        while self._at(TT.OR):
            self.pos += 1
            right = self._and_expr()
            left = LogicalOp(op="or", left=left, right=right,
                             line=left.line, col=left.col)
        return left

    def _and_expr(self) -> ASTNode:
        left = self._not_expr()
        while self._at(TT.AND):
            self.pos += 1
            right = self._not_expr()
            left = LogicalOp(op="and", left=left, right=right,
                             line=left.line, col=left.col)
        return left

    def _not_expr(self) -> ASTNode:
        if self._at(TT.NOT):
            tok = self._eat(TT.NOT)
            operand = self._not_expr()
            return UnaryOp(op="not", operand=operand, line=tok.line, col=tok.col)
        return self._comparison()

    def _comparison(self) -> ASTNode:
        left = self._range_expr()
        while self._at(TT.EQ, TT.NEQ, TT.GT, TT.LT, TT.GTE, TT.LTE):
            op_tok = self._eat_any()
            right = self._range_expr()
            left = BinaryOp(op=op_tok.value, left=left, right=right,
                            line=left.line, col=left.col)
        return left

    def _range_expr(self) -> ASTNode:
        left = self._addition()
        if self._at(TT.DOTDOT):
            self.pos += 1
            right = self._addition()
            return RangeExpr(start=left, end=right, line=left.line, col=left.col)
        return left

    def _addition(self) -> ASTNode:
        left = self._multiplication()
        while self._at(TT.PLUS, TT.MINUS):
            op_tok = self._eat_any()
            right = self._multiplication()
            left = BinaryOp(op=op_tok.value, left=left, right=right,
                            line=left.line, col=left.col)
        return left

    def _multiplication(self) -> ASTNode:
        left = self._power()
        while self._at(TT.STAR, TT.SLASH, TT.PERCENT):
            op_tok = self._eat_any()
            right = self._power()
            left = BinaryOp(op=op_tok.value, left=left, right=right,
                            line=left.line, col=left.col)
        return left

    def _power(self) -> ASTNode:
        base = self._unary()
        if self._at(TT.POWER):
            self.pos += 1
            exp = self._power()  # right-associative
            return BinaryOp(op="**", left=base, right=exp,
                            line=base.line, col=base.col)
        return base

    def _unary(self) -> ASTNode:
        if self._at(TT.MINUS):
            tok = self._eat(TT.MINUS)
            operand = self._unary()
            return UnaryOp(op="-", operand=operand, line=tok.line, col=tok.col)
        if self._at(TT.NOT):
            tok = self._eat(TT.NOT)
            operand = self._unary()
            return UnaryOp(op="not", operand=operand, line=tok.line, col=tok.col)
        return self._postfix()

    def _postfix(self) -> ASTNode:
        """Parse call, index, and dot access (left-to-right)."""
        node = self._primary()
        while True:
            if self._at(TT.LPAREN):
                # Function call
                self.pos += 1
                args: List[ASTNode] = []
                self._skip_newlines()
                if not self._at(TT.RPAREN):
                    args.append(self._expression())
                    while self._at(TT.COMMA):
                        self.pos += 1
                        self._skip_newlines()
                        args.append(self._expression())
                self._skip_newlines()
                self._eat(TT.RPAREN, "Expected ')' after arguments")
                node = CallExpr(callee=node, args=args, line=node.line, col=node.col)
            elif self._at(TT.LBRACKET):
                # Index access
                self.pos += 1
                idx = self._expression()
                self._eat(TT.RBRACKET, "Expected ']'")
                node = IndexExpr(obj=node, index=idx, line=node.line, col=node.col)
            elif self._at(TT.DOT):
                # Dot access
                self.pos += 1
                attr_tok = self._eat(TT.IDENT, "Expected attribute name after '.'")
                node = DotExpr(obj=node, attr=attr_tok.value,
                               line=node.line, col=node.col)
            else:
                break
        return node

    def _primary(self) -> ASTNode:
        tok = self._cur()

        # Number literal
        if tok.type == TT.NUMBER:
            self.pos += 1
            return NumberLit(value=tok.value, line=tok.line, col=tok.col)

        # String literal
        if tok.type == TT.STRING:
            self.pos += 1
            return StringLit(value=tok.value, line=tok.line, col=tok.col)

        # Interpolated string
        if tok.type == TT.INTERP_STRING:
            self.pos += 1
            parsed_parts: List[Any] = []
            for part in tok.value:
                if isinstance(part, str):
                    parsed_parts.append(part)
                else:
                    # part is ("expr", expr_text, line, col)
                    _, expr_text, pline, pcol = part
                    sub_lexer = Lexer(expr_text, self.filename)
                    sub_tokens = sub_lexer.tokenise()
                    sub_parser = Parser(sub_tokens, expr_text, self.filename)
                    expr_node = sub_parser._expression()
                    parsed_parts.append(expr_node)
            return InterpStringLit(parts=parsed_parts, line=tok.line, col=tok.col)

        # Boolean
        if tok.type == TT.YES:
            self.pos += 1
            return BoolLit(value=True, line=tok.line, col=tok.col)
        if tok.type == TT.NO:
            self.pos += 1
            return BoolLit(value=False, line=tok.line, col=tok.col)

        # Void
        if tok.type == TT.VOID:
            self.pos += 1
            return VoidLit(line=tok.line, col=tok.col)

        # Self
        if tok.type == TT.SELF:
            self.pos += 1
            return SelfExpr(line=tok.line, col=tok.col)

        # Parent
        if tok.type == TT.PARENT:
            self.pos += 1
            return ParentExpr(line=tok.line, col=tok.col)

        # Identifier
        if tok.type == TT.IDENT:
            self.pos += 1
            return Identifier(name=tok.value, line=tok.line, col=tok.col)

        # Parenthesised expression
        if tok.type == TT.LPAREN:
            self.pos += 1
            self._skip_newlines()
            expr = self._expression()
            self._skip_newlines()
            self._eat(TT.RPAREN, "Expected ')'")
            return expr

        # Array literal  [ ... ]
        if tok.type == TT.LBRACKET:
            return self._array_literal()

        # Map literal  { key: value, ... }
        if tok.type == TT.LBRACE:
            return self._map_literal()

        # Lambda: |params| => expr   or   |params| => { stmts }
        if tok.type == TT.BAR:
            return self._lambda_expr()

        raise KovaSyntaxError(f"Unexpected token: {tok.type.name} ({tok.value!r})",
                              tok.line, tok.col, self._src_line(tok.line))

    def _array_literal(self) -> ArrayLit:
        tok = self._eat(TT.LBRACKET)
        elements: List[ASTNode] = []
        self._skip_newlines()
        if not self._at(TT.RBRACKET):
            elements.append(self._expression())
            while self._at(TT.COMMA):
                self.pos += 1
                self._skip_newlines()
                if self._at(TT.RBRACKET):
                    break  # trailing comma
                elements.append(self._expression())
        self._skip_newlines()
        self._eat(TT.RBRACKET, "Expected ']'")
        return ArrayLit(elements=elements, line=tok.line, col=tok.col)

    def _map_literal(self) -> MapLit:
        tok = self._eat(TT.LBRACE)
        pairs: List[Tuple[ASTNode, ASTNode]] = []
        self._skip_newlines()
        if not self._at(TT.RBRACE):
            key = self._expression()
            self._eat(TT.COLON, "Expected ':' in map literal")
            self._skip_newlines()
            val = self._expression()
            pairs.append((key, val))
            while self._at(TT.COMMA):
                self.pos += 1
                self._skip_newlines()
                if self._at(TT.RBRACE):
                    break
                key = self._expression()
                self._eat(TT.COLON, "Expected ':' in map literal")
                self._skip_newlines()
                val = self._expression()
                pairs.append((key, val))
        self._skip_newlines()
        self._eat(TT.RBRACE, "Expected '}'")
        return MapLit(pairs=pairs, line=tok.line, col=tok.col)

    def _lambda_expr(self) -> LambdaExpr:
        """Parse  |params| => body"""
        tok = self._eat(TT.BAR)
        params: List[str] = []
        if not self._at(TT.BAR):
            params.append(self._eat(TT.IDENT, "Expected parameter name in lambda").value)
            while self._at(TT.COMMA):
                self.pos += 1
                params.append(self._eat(TT.IDENT, "Expected parameter name in lambda").value)
        self._eat(TT.BAR, "Expected '|' to close lambda parameters")
        self._eat(TT.ARROW, "Expected '=>' after lambda parameters")
        self._skip_newlines()
        if self._at(TT.LBRACE):
            body_stmts = self._block()
            # Wrap block in a special node — we'll handle it in interpreter
            body = Program(body=body_stmts, line=tok.line, col=tok.col)
        else:
            body = self._expression()
        return LambdaExpr(params=params, body=body, line=tok.line, col=tok.col)


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — ENVIRONMENT (SCOPE CHAIN)
# ═══════════════════════════════════════════════════════════════════════════════

class Environment:
    """
    Variable scope.

    Each environment has a dict of bindings and an optional parent.
    Locked names (constants) are tracked separately.
    """

    def __init__(self, parent: Optional[Environment] = None) -> None:
        self.bindings: Dict[str, Any] = {}
        self.locked: set = set()
        self.parent: Optional[Environment] = parent
        self.exports: Dict[str, Any] = {}

    def define(self, name: str, value: Any, lock: bool = False) -> None:
        """Define a new variable in the current scope."""
        self.bindings[name] = value
        if lock:
            self.locked.add(name)

    def get(self, name: str, line: int = 0, col: int = 0) -> Any:
        """Look up a variable, walking up the scope chain."""
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.get(name, line, col)
        raise KovaRuntimeError(f"Undefined variable: '{name}'", line, col)

    def set(self, name: str, value: Any, line: int = 0, col: int = 0) -> None:
        """Set an existing variable (walk up scopes)."""
        if name in self.bindings:
            if name in self.locked:
                raise KovaRuntimeError(
                    f"Cannot reassign constant '{name}'", line, col)
            self.bindings[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value, line, col)
            return
        raise KovaRuntimeError(f"Undefined variable: '{name}'", line, col)

    def has(self, name: str) -> bool:
        if name in self.bindings:
            return True
        if self.parent:
            return self.parent.has(name)
        return False

    def child(self) -> Environment:
        """Create a child scope."""
        return Environment(parent=self)


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 7 — RUNTIME VALUES (FUNCTIONS, CLASSES, INSTANCES)
# ═══════════════════════════════════════════════════════════════════════════════

class KovaFunction:
    """A user-defined KOVA function (or method)."""

    def __init__(self, name: str, params: List[str], body: List[ASTNode],
                 closure: Environment) -> None:
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def __repr__(self) -> str:
        return f"<forge {self.name}>"


class KovaLambda:
    """An anonymous lambda function."""

    def __init__(self, params: List[str], body: ASTNode,
                 closure: Environment) -> None:
        self.params = params
        self.body = body
        self.closure = closure

    def __repr__(self) -> str:
        return f"<lambda({', '.join(self.params)})>"


class KovaClass:
    """A KOVA class (shape)."""

    def __init__(self, name: str, methods: Dict[str, KovaFunction],
                 parent: Optional[KovaClass] = None) -> None:
        self.name = name
        self.methods = methods
        self.parent = parent

    def find_method(self, name: str) -> Optional[KovaFunction]:
        if name in self.methods:
            return self.methods[name]
        if self.parent:
            return self.parent.find_method(name)
        return None

    def __repr__(self) -> str:
        return f"<shape {self.name}>"


class KovaInstance:
    """An instance of a KOVA class."""

    def __init__(self, klass: KovaClass) -> None:
        self.klass = klass
        self.fields: Dict[str, Any] = {}

    def get_field(self, name: str, line: int = 0, col: int = 0) -> Any:
        if name in self.fields:
            return self.fields[name]
        method = self.klass.find_method(name)
        if method is not None:
            return BoundMethod(self, method)
        raise KovaRuntimeError(
            f"'{self.klass.name}' has no attribute '{name}'", line, col)

    def set_field(self, name: str, value: Any) -> None:
        self.fields[name] = value

    def __repr__(self) -> str:
        return f"<{self.klass.name} instance>"


class BoundMethod:
    """A method bound to a specific instance."""

    def __init__(self, instance: KovaInstance, method: KovaFunction) -> None:
        self.instance = instance
        self.method = method

    def __repr__(self) -> str:
        return f"<method {self.method.name} of {self.instance.klass.name}>"


class KovaBuiltin:
    """A built-in (native) function."""

    def __init__(self, name: str, func: Callable, arity: Optional[int] = None) -> None:
        self.name = name
        self.func = func
        self.arity = arity   # None means variadic

    def __repr__(self) -> str:
        return f"<builtin {self.name}>"


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 8 — INTERPRETER
# ═══════════════════════════════════════════════════════════════════════════════

class Interpreter:
    """
    Tree-walking interpreter for KOVA.

    Walks the AST produced by the Parser and evaluates each node.
    Maintains a global environment and supports nested scopes,
    closures, classes with inheritance, error handling, and modules.
    """

    def __init__(self, filename: str = "<stdin>",
                 allowed_dirs: Optional[List[str]] = None) -> None:
        self.filename = filename
        self.global_env = Environment()
        self.call_depth = 0
        self.allowed_dirs = allowed_dirs  # None = allow all
        self.imported: set = set()       # track imported module paths
        self.import_depth = 0
        self._source_lines: List[str] = []
        self._register_builtins()

    # -- helpers ---------------------------------------------------------------

    def _src_line(self, lineno: int) -> str:
        if 1 <= lineno <= len(self._source_lines):
            return self._source_lines[lineno - 1]
        return ""

    def _check_file_access(self, path: str, line: int = 0, col: int = 0) -> str:
        """Resolve and optionally sandbox a file path."""
        resolved = os.path.abspath(path)
        if self.allowed_dirs is not None:
            ok = any(resolved.startswith(os.path.abspath(d)) for d in self.allowed_dirs)
            if not ok:
                raise KovaRuntimeError(
                    f"File access denied: {path}", line, col)
        return resolved

    # -- public API ------------------------------------------------------------

    def run(self, source: str, env: Optional[Environment] = None) -> Any:
        """Lex, parse, and interpret a source string."""
        self._source_lines = source.split("\n")
        lexer = Lexer(source, self.filename)
        tokens = lexer.tokenise()
        parser = Parser(tokens, source, self.filename)
        program = parser.parse()
        return self._exec_program(program, env or self.global_env)

    def run_file(self, filepath: str) -> Any:
        """Read and run a .kv file."""
        resolved = os.path.abspath(filepath)
        self.filename = resolved
        try:
            with open(resolved, "r", encoding="utf-8") as f:
                source = f.read()
        except FileNotFoundError:
            raise KovaRuntimeError(f"File not found: {filepath}")
        except IOError as e:
            raise KovaRuntimeError(f"Cannot read file: {e}")
        return self.run(source)

    # -- program / block execution ---------------------------------------------

    def _exec_program(self, prog: Program, env: Environment) -> Any:
        result: Any = None
        deferred: List[List[ASTNode]] = []
        for stmt in prog.body:
            if isinstance(stmt, DeferStmt):
                deferred.append(stmt.body)
                continue
            result = self._exec(stmt, env)
        # Run deferred blocks in reverse order
        for block in reversed(deferred):
            self._exec_block(block, env)
        return result

    def _exec_block(self, stmts: List[ASTNode], env: Environment) -> Any:
        result: Any = None
        deferred: List[List[ASTNode]] = []
        for stmt in stmts:
            if isinstance(stmt, DeferStmt):
                deferred.append(stmt.body)
                continue
            result = self._exec(stmt, env)
        for block in reversed(deferred):
            self._exec_block(block, env)
        return result

    # -- main dispatch ---------------------------------------------------------

    def _exec(self, node: ASTNode, env: Environment) -> Any:
        """Execute/evaluate an AST node."""
        # Statements
        if isinstance(node, ExprStmt):
            return self._eval(node.expr, env)
        if isinstance(node, GrabStmt):
            return self._exec_grab(node, env)
        if isinstance(node, LockStmt):
            return self._exec_lock(node, env)
        if isinstance(node, ForgeStmt):
            return self._exec_forge(node, env)
        if isinstance(node, YieldStmt):
            val = self._eval(node.value, env)
            raise KovaReturnSignal(val)
        if isinstance(node, TestStmt):
            return self._exec_test(node, env)
        if isinstance(node, SpinFromStmt):
            return self._exec_spin_from(node, env)
        if isinstance(node, SpinInStmt):
            return self._exec_spin_in(node, env)
        if isinstance(node, OrbitStmt):
            return self._exec_orbit(node, env)
        if isinstance(node, SnapStmt):
            raise KovaBreakSignal()
        if isinstance(node, SkipStmt):
            raise KovaContinueSignal()
        if isinstance(node, ShapeStmt):
            return self._exec_shape(node, env)
        if isinstance(node, EvolveStmt):
            return self._exec_evolve(node, env)
        if isinstance(node, AttemptStmt):
            return self._exec_attempt(node, env)
        if isinstance(node, EjectStmt):
            val = self._eval(node.value, env)
            raise KovaEjectSignal(val, node.line, node.col)
        if isinstance(node, PullStmt):
            return self._exec_pull(node, env)
        if isinstance(node, ExposeStmt):
            return self._exec_expose(node, env)
        if isinstance(node, MorphStmt):
            return self._exec_morph(node, env)
        if isinstance(node, DeferStmt):
            # Handled at block level
            return None
        if isinstance(node, Assignment):
            return self._exec_assignment(node, env)
        if isinstance(node, CompoundAssignment):
            return self._exec_compound_assignment(node, env)
        if isinstance(node, IndexAssign):
            return self._exec_index_assign(node, env)
        if isinstance(node, DotAssign):
            return self._exec_dot_assign(node, env)
        if isinstance(node, CompoundIndexAssign):
            return self._exec_compound_index_assign(node, env)
        if isinstance(node, CompoundDotAssign):
            return self._exec_compound_dot_assign(node, env)

        # If it's an expression node, evaluate it
        return self._eval(node, env)

    # -- statement executors ---------------------------------------------------

    def _exec_grab(self, node: GrabStmt, env: Environment) -> None:
        val = self._eval(node.value, env)
        # If the variable already exists in an outer scope, update it there.
        # Otherwise define it in the current scope.
        if env.has(node.name):
            try:
                env.set(node.name, val, node.line, node.col)
            except KovaRuntimeError:
                # locked — define a new shadow in current scope
                env.define(node.name, val, lock=False)
        else:
            env.define(node.name, val, lock=False)

    def _exec_lock(self, node: LockStmt, env: Environment) -> None:
        val = self._eval(node.value, env)
        env.define(node.name, val, lock=True)

    def _exec_forge(self, node: ForgeStmt, env: Environment) -> None:
        fn = KovaFunction(node.name, node.params, node.body, env)
        env.define(node.name, fn)

    def _exec_test(self, node: TestStmt, env: Environment) -> Any:
        cond = self._eval(node.condition, env)
        if self._truthy(cond):
            return self._exec_block(node.body, env.child())
        for also_cond, also_body in node.also_branches:
            c = self._eval(also_cond, env)
            if self._truthy(c):
                return self._exec_block(also_body, env.child())
        if node.rival_body is not None:
            return self._exec_block(node.rival_body, env.child())
        return None

    def _exec_spin_from(self, node: SpinFromStmt, env: Environment) -> None:
        start = self._eval(node.start, env)
        end = self._eval(node.end, env)
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            raise KovaTypeError("spin..from..to requires numeric bounds",
                                node.line, node.col, self._src_line(node.line))
        start_i = int(start)
        end_i = int(end)
        iterations = 0
        i = start_i
        while i <= end_i:
            iterations += 1
            if iterations > LOOP_LIMIT:
                raise KovaRuntimeError("Loop iteration limit exceeded",
                                       node.line, node.col)
            loop_env = env.child()
            loop_env.define(node.var, i)
            try:
                self._exec_block(node.body, loop_env)
            except KovaBreakSignal:
                break
            except KovaContinueSignal:
                pass
            i += 1

    def _exec_spin_in(self, node: SpinInStmt, env: Environment) -> None:
        iterable = self._eval(node.iterable, env)
        if isinstance(iterable, list):
            items = iterable
        elif isinstance(iterable, str):
            items = list(iterable)
        elif isinstance(iterable, dict):
            items = list(iterable.keys())
        else:
            raise KovaTypeError("spin..in requires an iterable (array, string, or map)",
                                node.line, node.col, self._src_line(node.line))
        iterations = 0
        for item in items:
            iterations += 1
            if iterations > LOOP_LIMIT:
                raise KovaRuntimeError("Loop iteration limit exceeded",
                                       node.line, node.col)
            loop_env = env.child()
            loop_env.define(node.var, item)
            try:
                self._exec_block(node.body, loop_env)
            except KovaBreakSignal:
                break
            except KovaContinueSignal:
                continue

    def _exec_orbit(self, node: OrbitStmt, env: Environment) -> None:
        iterations = 0
        while True:
            cond = self._eval(node.condition, env)
            if not self._truthy(cond):
                break
            iterations += 1
            if iterations > LOOP_LIMIT:
                raise KovaRuntimeError("Loop iteration limit exceeded",
                                       node.line, node.col)
            loop_env = env.child()
            try:
                self._exec_block(node.body, loop_env)
            except KovaBreakSignal:
                break
            except KovaContinueSignal:
                continue

    def _exec_shape(self, node: ShapeStmt, env: Environment) -> None:
        methods: Dict[str, KovaFunction] = {}
        # Evaluate forge statements inside the shape body
        for stmt in node.body:
            if isinstance(stmt, ForgeStmt):
                fn = KovaFunction(stmt.name, stmt.params, stmt.body, env)
                methods[stmt.name] = fn
            # Allow other statements (e.g. grab for class-level fields) — skip them
        klass = KovaClass(node.name, methods, parent=None)
        env.define(node.name, klass)

    def _exec_evolve(self, node: EvolveStmt, env: Environment) -> None:
        parent = env.get(node.parent_name, node.line, node.col)
        if not isinstance(parent, KovaClass):
            raise KovaTypeError(
                f"'{node.parent_name}' is not a shape (class)", node.line, node.col)
        methods: Dict[str, KovaFunction] = {}
        for stmt in node.body:
            if isinstance(stmt, ForgeStmt):
                fn = KovaFunction(stmt.name, stmt.params, stmt.body, env)
                methods[stmt.name] = fn
        klass = KovaClass(node.name, methods, parent=parent)
        env.define(node.name, klass)

    def _exec_attempt(self, node: AttemptStmt, env: Environment) -> Any:
        try:
            return self._exec_block(node.body, env.child())
        except KovaEjectSignal as e:
            rescue_env = env.child()
            rescue_env.define(node.rescue_var, e.value)
            return self._exec_block(node.rescue_body, rescue_env)
        except KovaRuntimeError as e:
            rescue_env = env.child()
            rescue_env.define(node.rescue_var, e.message)
            return self._exec_block(node.rescue_body, rescue_env)
        except KovaTypeError as e:
            rescue_env = env.child()
            rescue_env.define(node.rescue_var, e.message)
            return self._exec_block(node.rescue_body, rescue_env)

    def _exec_pull(self, node: PullStmt, env: Environment) -> None:
        """Import another .kv module."""
        self.import_depth += 1
        if self.import_depth > IMPORT_DEPTH_LIMIT:
            raise KovaRuntimeError("Import depth limit exceeded (circular import?)",
                                   node.line, node.col)
        # Resolve path relative to current file
        base_dir = os.path.dirname(os.path.abspath(self.filename))
        path = node.path
        if not path.endswith(".kv"):
            path += ".kv"
        full_path = os.path.normpath(os.path.join(base_dir, path))

        if full_path in self.imported:
            self.import_depth -= 1
            return  # already imported
        self.imported.add(full_path)

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                source = f.read()
        except FileNotFoundError:
            raise KovaRuntimeError(f"Module not found: {node.path}",
                                   node.line, node.col)

        # Create a module environment that inherits from global
        mod_env = self.global_env.child()
        old_filename = self.filename
        old_lines = self._source_lines
        self.filename = full_path
        self.run(source, mod_env)
        self.filename = old_filename
        self._source_lines = old_lines

        # Copy exported names into current env
        for name, val in mod_env.exports.items():
            env.define(name, val)
        # Also copy all top-level bindings (non-exported) for convenience
        for name, val in mod_env.bindings.items():
            if name not in env.bindings:
                env.define(name, val)

        self.import_depth -= 1

    def _exec_expose(self, node: ExposeStmt, env: Environment) -> None:
        val = env.get(node.name, node.line, node.col)
        env.exports[node.name] = val

    def _exec_morph(self, node: MorphStmt, env: Environment) -> Any:
        value = self._eval(node.value, env)
        for pattern, body in node.arms:
            pat_val = self._eval(pattern, env)
            if self._values_equal(value, pat_val):
                return self._exec_block(body, env.child())
        if node.default_body is not None:
            return self._exec_block(node.default_body, env.child())
        return None

    def _exec_assignment(self, node: Assignment, env: Environment) -> None:
        val = self._eval(node.value, env)
        target = node.target
        if isinstance(target, Identifier):
            env.set(target.name, val, node.line, node.col)
        else:
            raise KovaRuntimeError("Invalid assignment target", node.line, node.col)

    def _exec_compound_assignment(self, node: CompoundAssignment, env: Environment) -> None:
        target = node.target
        if isinstance(target, Identifier):
            old = env.get(target.name, node.line, node.col)
            rhs = self._eval(node.value, env)
            new_val = self._apply_binop(node.op, old, rhs, node.line, node.col)
            env.set(target.name, new_val, node.line, node.col)
        else:
            raise KovaRuntimeError("Invalid compound assignment target",
                                   node.line, node.col)

    def _exec_index_assign(self, node: IndexAssign, env: Environment) -> None:
        obj = self._eval(node.obj, env)
        idx = self._eval(node.index, env)
        val = self._eval(node.value, env)
        if isinstance(obj, list):
            if not isinstance(idx, (int, float)):
                raise KovaTypeError("Array index must be a number",
                                    node.line, node.col)
            obj[int(idx)] = val
        elif isinstance(obj, dict):
            obj[idx] = val
        else:
            raise KovaTypeError("Cannot index-assign on this type",
                                node.line, node.col)

    def _exec_dot_assign(self, node: DotAssign, env: Environment) -> None:
        obj = self._eval(node.obj, env)
        val = self._eval(node.value, env)
        if isinstance(obj, KovaInstance):
            obj.set_field(node.attr, val)
        elif isinstance(obj, dict):
            obj[node.attr] = val
        else:
            raise KovaTypeError(
                f"Cannot set attribute '{node.attr}' on {self._type_name(obj)}",
                node.line, node.col)

    def _exec_compound_index_assign(self, node: CompoundIndexAssign, env: Environment) -> None:
        obj = self._eval(node.obj, env)
        idx = self._eval(node.index, env)
        rhs = self._eval(node.value, env)
        if isinstance(obj, list):
            i = int(idx)
            obj[i] = self._apply_binop(node.op, obj[i], rhs, node.line, node.col)
        elif isinstance(obj, dict):
            obj[idx] = self._apply_binop(node.op, obj[idx], rhs, node.line, node.col)
        else:
            raise KovaTypeError("Cannot compound-index-assign on this type",
                                node.line, node.col)

    def _exec_compound_dot_assign(self, node: CompoundDotAssign, env: Environment) -> None:
        obj = self._eval(node.obj, env)
        rhs = self._eval(node.value, env)
        if isinstance(obj, KovaInstance):
            old = obj.get_field(node.attr, node.line, node.col)
            obj.set_field(node.attr, self._apply_binop(node.op, old, rhs,
                                                        node.line, node.col))
        elif isinstance(obj, dict):
            old = obj[node.attr]
            obj[node.attr] = self._apply_binop(node.op, old, rhs, node.line, node.col)
        else:
            raise KovaTypeError(
                f"Cannot compound-assign attribute on {self._type_name(obj)}",
                node.line, node.col)

    # -- expression evaluation -------------------------------------------------

    def _eval(self, node: ASTNode, env: Environment) -> Any:
        """Evaluate an expression node and return its value."""
        if isinstance(node, NumberLit):
            return node.value
        if isinstance(node, StringLit):
            return node.value
        if isinstance(node, InterpStringLit):
            return self._eval_interp_string(node, env)
        if isinstance(node, BoolLit):
            return node.value
        if isinstance(node, VoidLit):
            return None
        if isinstance(node, ArrayLit):
            return [self._eval(e, env) for e in node.elements]
        if isinstance(node, MapLit):
            result: Dict[Any, Any] = {}
            for k, v in node.pairs:
                result[self._eval(k, env)] = self._eval(v, env)
            return result
        if isinstance(node, Identifier):
            return env.get(node.name, node.line, node.col)
        if isinstance(node, SelfExpr):
            return env.get("self", node.line, node.col)
        if isinstance(node, ParentExpr):
            return env.get("__parent__", node.line, node.col)
        if isinstance(node, BinaryOp):
            return self._eval_binary(node, env)
        if isinstance(node, UnaryOp):
            return self._eval_unary(node, env)
        if isinstance(node, LogicalOp):
            return self._eval_logical(node, env)
        if isinstance(node, CallExpr):
            return self._eval_call(node, env)
        if isinstance(node, IndexExpr):
            return self._eval_index(node, env)
        if isinstance(node, DotExpr):
            return self._eval_dot(node, env)
        if isinstance(node, PipeExpr):
            return self._eval_pipe(node, env)
        if isinstance(node, RangeExpr):
            return self._eval_range(node, env)
        if isinstance(node, LambdaExpr):
            return KovaLambda(node.params, node.body, env)
        if isinstance(node, Assignment):
            self._exec_assignment(node, env)
            return None
        if isinstance(node, Program):
            # This can happen with block-body lambdas
            return self._exec_program(node, env)

        raise KovaRuntimeError(
            f"Unknown AST node: {type(node).__name__}", node.line, node.col)

    def _eval_interp_string(self, node: InterpStringLit, env: Environment) -> str:
        parts: List[str] = []
        for part in node.parts:
            if isinstance(part, str):
                parts.append(part)
            else:
                val = self._eval(part, env)
                parts.append(self._stringify(val))
        return "".join(parts)

    def _eval_binary(self, node: BinaryOp, env: Environment) -> Any:
        left = self._eval(node.left, env)
        right = self._eval(node.right, env)
        return self._apply_binop(node.op, left, right, node.line, node.col)

    def _apply_binop(self, op: str, left: Any, right: Any,
                     line: int = 0, col: int = 0) -> Any:
        """Apply a binary operator."""
        # String concatenation with +
        if op == "+" and (isinstance(left, str) or isinstance(right, str)):
            return self._stringify(left) + self._stringify(right)

        # Array concatenation with +
        if op == "+" and isinstance(left, list) and isinstance(right, list):
            return left + right

        # Numeric operations
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            if op == "+":
                return left + right
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if op == "/":
                if right == 0:
                    raise KovaRuntimeError("Division by zero", line, col)
                result = left / right
                # Return int if result is whole
                if isinstance(result, float) and result == int(result) and \
                   isinstance(left, int) and isinstance(right, int):
                    return int(result)
                return result
            if op == "%":
                if right == 0:
                    raise KovaRuntimeError("Modulo by zero", line, col)
                return left % right
            if op == "**":
                return left ** right

        # String repetition
        if op == "*" and isinstance(left, str) and isinstance(right, (int, float)):
            return left * int(right)

        # Comparison operators (work on any comparable types)
        if op == "==":
            return self._values_equal(left, right)
        if op == "!=":
            return not self._values_equal(left, right)
        if op in (">", "<", ">=", "<="):
            return self._compare(op, left, right, line, col)

        raise KovaTypeError(
            f"Unsupported operation: {self._type_name(left)} {op} {self._type_name(right)}",
            line, col)

    def _compare(self, op: str, left: Any, right: Any,
                 line: int = 0, col: int = 0) -> bool:
        try:
            if op == ">":
                return left > right
            if op == "<":
                return left < right
            if op == ">=":
                return left >= right
            if op == "<=":
                return left <= right
        except TypeError:
            raise KovaTypeError(
                f"Cannot compare {self._type_name(left)} and {self._type_name(right)}",
                line, col)
        return False

    def _eval_unary(self, node: UnaryOp, env: Environment) -> Any:
        val = self._eval(node.operand, env)
        if node.op == "-":
            if isinstance(val, (int, float)):
                return -val
            raise KovaTypeError("Unary '-' requires a number",
                                node.line, node.col)
        if node.op == "not":
            return not self._truthy(val)
        raise KovaRuntimeError(f"Unknown unary operator: {node.op}",
                               node.line, node.col)

    def _eval_logical(self, node: LogicalOp, env: Environment) -> Any:
        left = self._eval(node.left, env)
        if node.op == "or":
            return left if self._truthy(left) else self._eval(node.right, env)
        if node.op == "and":
            return self._eval(node.right, env) if self._truthy(left) else left
        raise KovaRuntimeError(f"Unknown logical operator: {node.op}",
                               node.line, node.col)

    def _eval_call(self, node: CallExpr, env: Environment) -> Any:
        callee = self._eval(node.callee, env)
        args = [self._eval(a, env) for a in node.args]
        return self._call_value(callee, args, node.line, node.col)

    def _call_value(self, callee: Any, args: List[Any],
                    line: int = 0, col: int = 0) -> Any:
        """Call a callable value (function, lambda, builtin, class)."""
        # Built-in function
        if isinstance(callee, KovaBuiltin):
            if callee.arity is not None and len(args) != callee.arity:
                raise KovaRuntimeError(
                    f"'{callee.name}' expects {callee.arity} argument(s), got {len(args)}",
                    line, col)
            try:
                return callee.func(args, line, col)
            except KovaEjectSignal:
                raise
            except KovaReturnSignal:
                raise
            except (KovaRuntimeError, KovaTypeError, KovaSyntaxError):
                raise
            except Exception as e:
                raise KovaRuntimeError(f"Error in builtin '{callee.name}': {e}",
                                       line, col)

        # User-defined function
        if isinstance(callee, KovaFunction):
            return self._call_function(callee, args, line, col)

        # Lambda
        if isinstance(callee, KovaLambda):
            return self._call_lambda(callee, args, line, col)

        # Bound method
        if isinstance(callee, BoundMethod):
            return self._call_method(callee, args, line, col)

        # Class instantiation
        if isinstance(callee, KovaClass):
            return self._call_class(callee, args, line, col)

        raise KovaTypeError(
            f"'{self._type_name(callee)}' is not callable", line, col)

    def _call_function(self, fn: KovaFunction, args: List[Any],
                       line: int = 0, col: int = 0) -> Any:
        if len(args) != len(fn.params):
            raise KovaRuntimeError(
                f"'{fn.name}' expects {len(fn.params)} argument(s), got {len(args)}",
                line, col)
        self.call_depth += 1
        if self.call_depth > RECURSION_LIMIT:
            self.call_depth -= 1
            raise KovaRuntimeError("Maximum recursion depth exceeded", line, col)
        call_env = fn.closure.child()
        for name, val in zip(fn.params, args):
            call_env.define(name, val)
        try:
            self._exec_block(fn.body, call_env)
        except KovaReturnSignal as ret:
            self.call_depth -= 1
            return ret.value
        self.call_depth -= 1
        return None

    def _call_lambda(self, lam: KovaLambda, args: List[Any],
                     line: int = 0, col: int = 0) -> Any:
        if len(args) != len(lam.params):
            raise KovaRuntimeError(
                f"Lambda expects {len(lam.params)} argument(s), got {len(args)}",
                line, col)
        self.call_depth += 1
        if self.call_depth > RECURSION_LIMIT:
            self.call_depth -= 1
            raise KovaRuntimeError("Maximum recursion depth exceeded", line, col)
        call_env = lam.closure.child()
        for name, val in zip(lam.params, args):
            call_env.define(name, val)
        try:
            if isinstance(lam.body, Program):
                self._exec_program(lam.body, call_env)
            else:
                result = self._eval(lam.body, call_env)
                self.call_depth -= 1
                return result
        except KovaReturnSignal as ret:
            self.call_depth -= 1
            return ret.value
        self.call_depth -= 1
        return None

    def _call_method(self, bm: BoundMethod, args: List[Any],
                     line: int = 0, col: int = 0) -> Any:
        method = bm.method
        instance = bm.instance
        if len(args) != len(method.params):
            raise KovaRuntimeError(
                f"Method '{method.name}' expects {len(method.params)} argument(s), got {len(args)}",
                line, col)
        self.call_depth += 1
        if self.call_depth > RECURSION_LIMIT:
            self.call_depth -= 1
            raise KovaRuntimeError("Maximum recursion depth exceeded", line, col)
        call_env = method.closure.child()
        call_env.define("self", instance)
        # Set up parent reference for super calls
        if instance.klass.parent:
            parent_proxy = _ParentProxy(instance, instance.klass.parent, self)
            call_env.define("__parent__", parent_proxy)
        for name, val in zip(method.params, args):
            call_env.define(name, val)
        try:
            self._exec_block(method.body, call_env)
        except KovaReturnSignal as ret:
            self.call_depth -= 1
            return ret.value
        self.call_depth -= 1
        return None

    def _call_class(self, klass: KovaClass, args: List[Any],
                    line: int = 0, col: int = 0) -> KovaInstance:
        instance = KovaInstance(klass)
        init = klass.find_method("init")
        if init is not None:
            bm = BoundMethod(instance, init)
            self._call_method(bm, args, line, col)
        elif args:
            raise KovaRuntimeError(
                f"'{klass.name}' constructor takes no arguments", line, col)
        return instance

    def _eval_index(self, node: IndexExpr, env: Environment) -> Any:
        obj = self._eval(node.obj, env)
        idx = self._eval(node.index, env)
        if isinstance(obj, list):
            if not isinstance(idx, (int, float)):
                raise KovaTypeError("Array index must be a number",
                                    node.line, node.col)
            i = int(idx)
            if i < 0 or i >= len(obj):
                raise KovaRuntimeError(
                    f"Array index {i} out of bounds (length {len(obj)})",
                    node.line, node.col)
            return obj[i]
        if isinstance(obj, dict):
            if idx not in obj:
                raise KovaRuntimeError(
                    f"Key '{idx}' not found in map", node.line, node.col)
            return obj[idx]
        if isinstance(obj, str):
            if not isinstance(idx, (int, float)):
                raise KovaTypeError("String index must be a number",
                                    node.line, node.col)
            i = int(idx)
            if i < 0 or i >= len(obj):
                raise KovaRuntimeError(
                    f"String index {i} out of bounds (length {len(obj)})",
                    node.line, node.col)
            return obj[i]
        raise KovaTypeError(
            f"Cannot index into {self._type_name(obj)}", node.line, node.col)

    def _eval_dot(self, node: DotExpr, env: Environment) -> Any:
        obj = self._eval(node.obj, env)

        # Instance attribute/method
        if isinstance(obj, KovaInstance):
            return obj.get_field(node.attr, node.line, node.col)

        # Parent proxy
        if isinstance(obj, _ParentProxy):
            return obj.get_method(node.attr, node.line, node.col)

        # Map field access
        if isinstance(obj, dict):
            if node.attr in obj:
                return obj[node.attr]
            # Map methods
            map_method = self._get_map_method(obj, node.attr, node.line, node.col)
            if map_method:
                return map_method
            raise KovaRuntimeError(
                f"Key '{node.attr}' not found in map", node.line, node.col)

        # String methods
        if isinstance(obj, str):
            return self._get_string_method(obj, node.attr, node.line, node.col)

        # Array methods
        if isinstance(obj, list):
            return self._get_array_method(obj, node.attr, node.line, node.col)

        # Class static access
        if isinstance(obj, KovaClass):
            m = obj.find_method(node.attr)
            if m:
                return m
            raise KovaRuntimeError(
                f"'{obj.name}' has no method '{node.attr}'", node.line, node.col)

        raise KovaTypeError(
            f"Cannot access attribute '{node.attr}' on {self._type_name(obj)}",
            node.line, node.col)

    def _eval_pipe(self, node: PipeExpr, env: Environment) -> Any:
        """Pipe operator: left |> right  —  right must be a callable, receives left as first arg."""
        left_val = self._eval(node.left, env)
        right_val = self._eval(node.right, env)
        return self._call_value(right_val, [left_val], node.line, node.col)

    def _eval_range(self, node: RangeExpr, env: Environment) -> List[int]:
        start = self._eval(node.start, env)
        end = self._eval(node.end, env)
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
            raise KovaTypeError("Range requires numeric bounds",
                                node.line, node.col)
        return list(range(int(start), int(end) + 1))

    # -- string methods --------------------------------------------------------

    def _get_string_method(self, s: str, name: str,
                           line: int = 0, col: int = 0) -> KovaBuiltin:
        """Return a bound string method."""
        methods: Dict[str, Callable] = {
            "crush": lambda args, l, c: s.lower(),
            "rise": lambda args, l, c: s.upper(),
            "trim": lambda args, l, c: s.strip(),
            "split": lambda args, l, c: s.split(args[0] if args else " "),
            "has": lambda args, l, c: args[0] in s if args else False,
            "swap": lambda args, l, c: s.replace(args[0], args[1]) if len(args) >= 2 else s,
            "span": lambda args, l, c: len(s),
            "starts": lambda args, l, c: s.startswith(args[0]) if args else False,
            "ends": lambda args, l, c: s.endswith(args[0]) if args else False,
            "slice": lambda args, l, c: (
                s[int(args[0]):int(args[1])] if len(args) >= 2
                else s[int(args[0]):] if args else s
            ),
        }
        if name in methods:
            return KovaBuiltin(f"String.{name}", methods[name])
        raise KovaRuntimeError(
            f"String has no method '{name}'", line, col)

    # -- array methods ---------------------------------------------------------

    def _get_array_method(self, arr: list, name: str,
                          line: int = 0, col: int = 0) -> KovaBuiltin:
        """Return a bound array method."""

        def _push(args: list, l: int, c: int) -> Any:
            arr.append(args[0])
            return arr

        def _pop(args: list, l: int, c: int) -> Any:
            if not arr:
                raise KovaRuntimeError("Cannot pop from empty array", l, c)
            return arr.pop()

        def _shift(args: list, l: int, c: int) -> Any:
            if not arr:
                raise KovaRuntimeError("Cannot shift from empty array", l, c)
            return arr.pop(0)

        def _span(args: list, l: int, c: int) -> int:
            return len(arr)

        def _seek(args: list, l: int, c: int) -> int:
            try:
                return arr.index(args[0])
            except ValueError:
                return -1

        def _has(args: list, l: int, c: int) -> bool:
            return args[0] in arr

        def _each(args: list, l: int, c: int) -> None:
            fn = args[0]
            for item in arr:
                self._call_value(fn, [item], l, c)

        def _map_fn(args: list, l: int, c: int) -> list:
            fn = args[0]
            return [self._call_value(fn, [item], l, c) for item in arr]

        def _sift(args: list, l: int, c: int) -> list:
            fn = args[0]
            return [item for item in arr if self._truthy(self._call_value(fn, [item], l, c))]

        def _fold(args: list, l: int, c: int) -> Any:
            acc = args[0]
            fn = args[1]
            for item in arr:
                acc = self._call_value(fn, [acc, item], l, c)
            return acc

        def _sort_fn(args: list, l: int, c: int) -> list:
            return sorted(arr)

        def _flip(args: list, l: int, c: int) -> list:
            return list(reversed(arr))

        def _fuse(args: list, l: int, c: int) -> list:
            other = args[0]
            if not isinstance(other, list):
                raise KovaTypeError("fuse expects an array", l, c)
            return arr + other

        def _slice_fn(args: list, l: int, c: int) -> list:
            if len(args) >= 2:
                return arr[int(args[0]):int(args[1])]
            elif args:
                return arr[int(args[0]):]
            return arr[:]

        def _bond(args: list, l: int, c: int) -> str:
            delim = args[0] if args else ""
            return delim.join(self._stringify(x) for x in arr)

        methods: Dict[str, Callable] = {
            "push": _push,
            "pop": _pop,
            "shift": _shift,
            "span": _span,
            "seek": _seek,
            "has": _has,
            "each": _each,
            "map": _map_fn,
            "sift": _sift,
            "fold": _fold,
            "sort": _sort_fn,
            "flip": _flip,
            "fuse": _fuse,
            "slice": _slice_fn,
            "bond": _bond,
        }
        if name in methods:
            return KovaBuiltin(f"Array.{name}", methods[name])
        raise KovaRuntimeError(
            f"Array has no method '{name}'", line, col)

    # -- map methods -----------------------------------------------------------

    def _get_map_method(self, m: dict, name: str,
                        line: int = 0, col: int = 0) -> Optional[KovaBuiltin]:
        """Return a bound map method, or None."""
        if name == "keys":
            return KovaBuiltin("Map.keys", lambda args, l, c: list(m.keys()))
        if name == "vals":
            return KovaBuiltin("Map.vals", lambda args, l, c: list(m.values()))
        if name == "has":
            return KovaBuiltin("Map.has", lambda args, l, c: args[0] in m)
        if name == "span":
            return KovaBuiltin("Map.span", lambda args, l, c: len(m))
        return None

    # -- utility ---------------------------------------------------------------

    def _truthy(self, value: Any) -> bool:
        """KOVA truthiness: void and no are falsy; 0 and "" are falsy."""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, list):
            return len(value) > 0
        return True

    def _values_equal(self, a: Any, b: Any) -> bool:
        """Deep equality check."""
        if a is None and b is None:
            return True
        if a is None or b is None:
            return False
        if type(a) != type(b):
            # Allow int/float comparison
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return a == b
            return False
        return a == b

    def _stringify(self, value: Any) -> str:
        """Convert a KOVA value to its string representation."""
        if value is None:
            return "void"
        if isinstance(value, bool):
            return "yes" if value else "no"
        if isinstance(value, float):
            if value == int(value):
                return str(int(value))
            return str(value)
        if isinstance(value, int):
            return str(value)
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            inner = ", ".join(self._display(x) for x in value)
            return f"[{inner}]"
        if isinstance(value, dict):
            pairs = ", ".join(
                f"{self._display(k)}: {self._display(v)}"
                for k, v in value.items()
            )
            return "{" + pairs + "}"
        if isinstance(value, (KovaFunction, KovaLambda, KovaBuiltin,
                              KovaClass, KovaInstance, BoundMethod)):
            return repr(value)
        return str(value)

    def _display(self, value: Any) -> str:
        """Display a value with strings quoted (for array/map printing)."""
        if isinstance(value, str):
            return f'"{value}"'
        return self._stringify(value)

    def _type_name(self, value: Any) -> str:
        """Get the KOVA type name of a value."""
        if value is None:
            return "void"
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, (int, float)):
            return "number"
        if isinstance(value, str):
            return "string"
        if isinstance(value, list):
            return "array"
        if isinstance(value, dict):
            return "map"
        if isinstance(value, (KovaFunction, KovaLambda, KovaBuiltin)):
            return "function"
        if isinstance(value, KovaClass):
            return "shape"
        if isinstance(value, KovaInstance):
            return value.klass.name
        if isinstance(value, BoundMethod):
            return "function"
        return "unknown"

    # ── BUILTINS ──────────────────────────────────────────────────────────────

    def _register_builtins(self) -> None:
        """Register all built-in functions in the global environment."""
        g = self.global_env

        # -- I/O ---------------------------------------------------------------

        def _emit(args: list, l: int, c: int) -> None:
            print(self._stringify(args[0]))

        def _absorb(args: list, l: int, c: int) -> str:
            prompt = self._stringify(args[0]) if args else ""
            return input(prompt)

        g.define("emit", KovaBuiltin("emit", _emit, 1))
        g.define("absorb", KovaBuiltin("absorb", _absorb))

        # -- Type conversion ----------------------------------------------------

        def _cast(args: list, l: int, c: int) -> Any:
            val, target = args[0], args[1]
            if target == "number":
                if isinstance(val, (int, float)):
                    return val
                if isinstance(val, str):
                    try:
                        return int(val)
                    except ValueError:
                        try:
                            return float(val)
                        except ValueError:
                            raise KovaRuntimeError(f"Cannot cast '{val}' to number", l, c)
                if isinstance(val, bool):
                    return 1 if val else 0
                raise KovaTypeError(f"Cannot cast {self._type_name(val)} to number", l, c)
            if target == "string":
                return self._stringify(val)
            if target == "boolean":
                return self._truthy(val)
            raise KovaRuntimeError(f"Unknown cast target: '{target}'", l, c)

        g.define("cast", KovaBuiltin("cast", _cast, 2))

        # -- Collections -------------------------------------------------------

        def _span(args: list, l: int, c: int) -> int:
            val = args[0]
            if isinstance(val, (list, str, dict)):
                return len(val)
            raise KovaTypeError(f"span: expected collection, got {self._type_name(val)}", l, c)

        def _fuse(args: list, l: int, c: int) -> list:
            a, b = args
            if isinstance(a, list) and isinstance(b, list):
                return a + b
            raise KovaTypeError("fuse: expected two arrays", l, c)

        def _slice_fn(args: list, l: int, c: int) -> Any:
            coll = args[0]
            start = int(args[1])
            end = int(args[2]) if len(args) > 2 else len(coll)
            if isinstance(coll, (list, str)):
                return coll[start:end]
            raise KovaTypeError("slice: expected array or string", l, c)

        def _seek(args: list, l: int, c: int) -> int:
            coll, val = args[0], args[1]
            if isinstance(coll, list):
                try:
                    return coll.index(val)
                except ValueError:
                    return -1
            if isinstance(coll, str):
                return coll.find(val)
            raise KovaTypeError("seek: expected array or string", l, c)

        g.define("span", KovaBuiltin("span", _span, 1))
        g.define("fuse", KovaBuiltin("fuse", _fuse, 2))
        g.define("slice", KovaBuiltin("slice", _slice_fn))
        g.define("seek", KovaBuiltin("seek", _seek, 2))

        # -- String functions --------------------------------------------------

        def _crush(args: list, l: int, c: int) -> str:
            return str(args[0]).lower()

        def _rise(args: list, l: int, c: int) -> str:
            return str(args[0]).upper()

        def _split_fn(args: list, l: int, c: int) -> list:
            return str(args[0]).split(args[1] if len(args) > 1 else " ")

        def _bond(args: list, l: int, c: int) -> str:
            arr, delim = args[0], args[1] if len(args) > 1 else ""
            if not isinstance(arr, list):
                raise KovaTypeError("bond: expected array", l, c)
            return delim.join(self._stringify(x) for x in arr)

        g.define("crush", KovaBuiltin("crush", _crush, 1))
        g.define("rise", KovaBuiltin("rise", _rise, 1))
        g.define("split", KovaBuiltin("split", _split_fn))
        g.define("bond", KovaBuiltin("bond", _bond))

        # -- Utility -----------------------------------------------------------

        def _clone(args: list, l: int, c: int) -> Any:
            return copy.deepcopy(args[0])

        def _kind(args: list, l: int, c: int) -> str:
            return self._type_name(args[0])

        def _tick(args: list, l: int, c: int) -> int:
            return int(time.time() * 1000)

        def _rand(args: list, l: int, c: int) -> int:
            return random.randint(int(args[0]), int(args[1]))

        def _keys(args: list, l: int, c: int) -> list:
            if isinstance(args[0], dict):
                return list(args[0].keys())
            raise KovaTypeError("keys: expected map", l, c)

        def _vals(args: list, l: int, c: int) -> list:
            if isinstance(args[0], dict):
                return list(args[0].values())
            raise KovaTypeError("vals: expected map", l, c)

        g.define("clone", KovaBuiltin("clone", _clone, 1))
        g.define("kind", KovaBuiltin("kind", _kind, 1))
        g.define("typeof", KovaBuiltin("typeof", _kind, 1))
        g.define("tick", KovaBuiltin("tick", _tick, 0))
        g.define("rand", KovaBuiltin("rand", _rand, 2))
        g.define("keys", KovaBuiltin("keys", _keys, 1))
        g.define("vals", KovaBuiltin("vals", _vals, 1))

        # -- File I/O ----------------------------------------------------------

        def _read(args: list, l: int, c: int) -> str:
            path = self._check_file_access(str(args[0]), l, c)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except IOError as e:
                raise KovaRuntimeError(f"Cannot read file: {e}", l, c)

        def _write(args: list, l: int, c: int) -> None:
            path = self._check_file_access(str(args[0]), l, c)
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(str(args[1]))
            except IOError as e:
                raise KovaRuntimeError(f"Cannot write file: {e}", l, c)

        def _append_file(args: list, l: int, c: int) -> None:
            path = self._check_file_access(str(args[0]), l, c)
            try:
                with open(path, "a", encoding="utf-8") as f:
                    f.write(str(args[1]))
            except IOError as e:
                raise KovaRuntimeError(f"Cannot append to file: {e}", l, c)

        g.define("read", KovaBuiltin("read", _read, 1))
        g.define("write", KovaBuiltin("write", _write, 2))
        g.define("append", KovaBuiltin("append", _append_file, 2))

        # -- Math ---------------------------------------------------------------

        def _floor(args: list, l: int, c: int) -> int:
            return int(math.floor(args[0]))

        def _ceil(args: list, l: int, c: int) -> int:
            return int(math.ceil(args[0]))

        def _round_fn(args: list, l: int, c: int) -> int:
            return int(round(args[0]))

        def _abs_fn(args: list, l: int, c: int) -> Union[int, float]:
            return abs(args[0])

        def _sqrt(args: list, l: int, c: int) -> float:
            if args[0] < 0:
                raise KovaRuntimeError("Cannot take sqrt of negative number", l, c)
            return math.sqrt(args[0])

        def _max_fn(args: list, l: int, c: int) -> Any:
            return max(args[0], args[1])

        def _min_fn(args: list, l: int, c: int) -> Any:
            return min(args[0], args[1])

        g.define("floor", KovaBuiltin("floor", _floor, 1))
        g.define("ceil", KovaBuiltin("ceil", _ceil, 1))
        g.define("round", KovaBuiltin("round", _round_fn, 1))
        g.define("abs", KovaBuiltin("abs", _abs_fn, 1))
        g.define("sqrt", KovaBuiltin("sqrt", _sqrt, 1))
        g.define("max", KovaBuiltin("max", _max_fn, 2))
        g.define("min", KovaBuiltin("min", _min_fn, 2))

        # -- Array functions ----------------------------------------------------

        def _sort_fn(args: list, l: int, c: int) -> list:
            if not isinstance(args[0], list):
                raise KovaTypeError("sort: expected array", l, c)
            return sorted(args[0])

        def _reverse_fn(args: list, l: int, c: int) -> list:
            if not isinstance(args[0], list):
                raise KovaTypeError("reverse: expected array", l, c)
            return list(reversed(args[0]))

        def _push_fn(args: list, l: int, c: int) -> list:
            if not isinstance(args[0], list):
                raise KovaTypeError("push: expected array as first argument", l, c)
            args[0].append(args[1])
            return args[0]

        def _pop_fn(args: list, l: int, c: int) -> Any:
            if not isinstance(args[0], list):
                raise KovaTypeError("pop: expected array", l, c)
            if not args[0]:
                raise KovaRuntimeError("Cannot pop from empty array", l, c)
            return args[0].pop()

        def _range_fn(args: list, l: int, c: int) -> list:
            start = int(args[0])
            end = int(args[1])
            return list(range(start, end + 1))

        g.define("sort", KovaBuiltin("sort", _sort_fn, 1))
        g.define("reverse", KovaBuiltin("reverse", _reverse_fn, 1))
        g.define("push", KovaBuiltin("push", _push_fn, 2))
        g.define("pop", KovaBuiltin("pop", _pop_fn, 1))
        g.define("range", KovaBuiltin("range", _range_fn, 2))

        # -- Functional --------------------------------------------------------

        def _map_fn(args: list, l: int, c: int) -> list:
            arr, fn = args[0], args[1]
            if not isinstance(arr, list):
                raise KovaTypeError("map: expected array as first argument", l, c)
            return [self._call_value(fn, [x], l, c) for x in arr]

        def _filter_fn(args: list, l: int, c: int) -> list:
            arr, fn = args[0], args[1]
            if not isinstance(arr, list):
                raise KovaTypeError("filter: expected array as first argument", l, c)
            return [x for x in arr if self._truthy(self._call_value(fn, [x], l, c))]

        def _reduce_fn(args: list, l: int, c: int) -> Any:
            arr, init, fn = args[0], args[1], args[2]
            if not isinstance(arr, list):
                raise KovaTypeError("reduce: expected array as first argument", l, c)
            acc = init
            for x in arr:
                acc = self._call_value(fn, [acc, x], l, c)
            return acc

        g.define("map", KovaBuiltin("map", _map_fn, 2))
        g.define("filter", KovaBuiltin("filter", _filter_fn, 2))
        g.define("reduce", KovaBuiltin("reduce", _reduce_fn, 3))

        # -- System ------------------------------------------------------------

        def _exit_fn(args: list, l: int, c: int) -> None:
            code = int(args[0]) if args else 0
            sys.exit(code)

        def _time_fn(args: list, l: int, c: int) -> str:
            return time.strftime("%Y-%m-%d %H:%M:%S")

        def _sleep_fn(args: list, l: int, c: int) -> None:
            ms = args[0]
            if isinstance(ms, (int, float)):
                time.sleep(ms / 1000.0)

        g.define("exit", KovaBuiltin("exit", _exit_fn))
        g.define("time", KovaBuiltin("time", _time_fn, 0))
        g.define("sleep", KovaBuiltin("sleep", _sleep_fn, 1))


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 9 — PARENT PROXY (for 'parent' / super calls)
# ═══════════════════════════════════════════════════════════════════════════════

class _ParentProxy:
    """
    Proxy object that resolves method lookups against the parent class,
    but binds them to the current instance.
    """

    def __init__(self, instance: KovaInstance, parent_class: KovaClass,
                 interpreter: Interpreter) -> None:
        self.instance = instance
        self.parent_class = parent_class
        self.interpreter = interpreter

    def get_method(self, name: str, line: int = 0, col: int = 0) -> BoundMethod:
        method = self.parent_class.find_method(name)
        if method is None:
            raise KovaRuntimeError(
                f"Parent class '{self.parent_class.name}' has no method '{name}'",
                line, col)
        return BoundMethod(self.instance, method)

    def __repr__(self) -> str:
        return f"<parent {self.parent_class.name}>"


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 10 — REPL
# ═══════════════════════════════════════════════════════════════════════════════

KOVA_BANNER = r"""
  ██╗  ██╗ ██████╗ ██╗   ██╗ █████╗
  ██║ ██╔╝██╔═══██╗██║   ██║██╔══██╗
  █████╔╝ ██║   ██║██║   ██║███████║
  ██╔═██╗ ██║   ██║╚██╗ ██╔╝██╔══██║
  ██║  ██╗╚██████╔╝ ╚████╔╝ ██║  ██║
  ╚═╝  ╚═╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝

  KOVA Programming Language v{version}
  Author: {author}
  Type .help for help, .exit to quit
"""

REPL_HELP = """
  KOVA REPL Commands:
    .help     — Show this help message
    .clear    — Clear the screen
    .exit     — Exit the REPL
    .version  — Show version info

  Language Quick Reference:
    grab x = 10         — Declare mutable variable
    lock PI = 3.14      — Declare constant
    forge f(x) {{ }}     — Define function
    emit("hello")       — Print output
    test x > 0 {{ }}     — If statement
    spin i from 1 to 5 {{ }} — For loop
"""


def run_repl() -> None:
    """Launch the interactive KOVA REPL."""
    # Try to enable readline for history and line editing
    try:
        import readline
        readline.parse_and_bind("tab: complete")
    except ImportError:
        pass

    print(_cyan(KOVA_BANNER.format(version=KOVA_VERSION, author=KOVA_AUTHOR)))

    interp = Interpreter("<repl>")
    buffer_lines: List[str] = []

    while True:
        try:
            if buffer_lines:
                prompt = _green("  ... ")
            else:
                prompt = _green("kova> ")

            try:
                line = input(prompt)
            except EOFError:
                print()
                break

            # REPL commands
            stripped = line.strip()
            if not buffer_lines:
                if stripped == ".exit":
                    print(_cyan("Goodbye!"))
                    break
                if stripped == ".help":
                    print(_yellow(REPL_HELP))
                    continue
                if stripped == ".clear":
                    os.system("cls" if os.name == "nt" else "clear")
                    continue
                if stripped == ".version":
                    print(_cyan(f"KOVA v{KOVA_VERSION} by {KOVA_AUTHOR}"))
                    continue

            buffer_lines.append(line)
            source = "\n".join(buffer_lines)

            # Check if we have complete blocks (balanced braces)
            open_braces = source.count("{") - source.count("}")
            if open_braces > 0:
                continue  # Need more input

            # Try to run
            buffer_lines = []
            if not source.strip():
                continue

            try:
                result = interp.run(source)
                if result is not None:
                    print(_cyan(interp._stringify(result)))
            except KovaReturnSignal as e:
                # yield at top level in REPL — just print the value
                print(_cyan(interp._stringify(e.value)))
            except (KovaSyntaxError, KovaRuntimeError, KovaTypeError) as e:
                print(str(e), file=sys.stderr)
            except KovaEjectSignal as e:
                print(_red(f"Uncaught error: {e.value}"), file=sys.stderr)
            except SystemExit:
                break
            except KeyboardInterrupt:
                print()
                buffer_lines = []
                continue

        except KeyboardInterrupt:
            print()
            buffer_lines = []
            continue


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 11 — MODULE-LEVEL RUNNER (for use by kova.py)
# ═══════════════════════════════════════════════════════════════════════════════

def run_file(filepath: str) -> None:
    """Run a .kv file and handle errors."""
    interp = Interpreter(filepath)
    try:
        interp.run_file(filepath)
    except (KovaSyntaxError, KovaRuntimeError, KovaTypeError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except KovaEjectSignal as e:
        print(_red(f"Uncaught error: {e.value}"), file=sys.stderr)
        sys.exit(1)
    except KovaReturnSignal:
        pass  # top-level yield — ignore
    except SystemExit:
        raise
    except Exception as e:
        print(_red(f"Internal error: {e}"), file=sys.stderr)
        sys.exit(1)


def run_source(source: str, filename: str = "<string>") -> Any:
    """Run a source string and return the result."""
    interp = Interpreter(filename)
    return interp.run(source)


# ═══════════════════════════════════════════════════════════════════════════════
#  END OF kova_core.py
# ═══════════════════════════════════════════════════════════════════════════════
