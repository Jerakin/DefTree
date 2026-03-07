import math
from pathlib import Path
from os import PathLike
from typing import Optional, overload

from deftree.ast.astnodes import ASTKeyValue, ASTBlock


class DecodeError(Exception):
    pass


class Token:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class Keyword(Token):
    ...


class Syntax(Token):
    ...


class Reader:
    """Loads the raw data."""
    def __init__(self):
        self.raw = ""
        self.pos = 0

    def load(self, file: Path):
        """Load a file path."""
        with file.open() as fp:
            self.raw = fp.read().strip()

    def loads(self, string: str):
        """Load a raw string."""
        self.raw = string.strip()

    def peek(self, k: int = 1) -> str:
        """Look at the character at position k."""
        return self.raw[self.pos + k - 1]

    def consume(self, k: int = 1) -> str:
        """Updates the current position and returns the character."""
        char = self.raw[self.pos + k - 1]
        self.pos += k
        return char

    def is_eof(self, peek=0) -> bool:
        """Checks if we are at end of file."""
        raw_len = len(self.raw)
        return self.raw and (raw_len == self.pos or raw_len < (self.pos + 1 + peek))


class Lexer:
    """Converts the raw Reader data into Tokens."""
    def __init__(self):
        self.reader: Reader = Reader()

    def _peek_until(self, end_of_content: tuple[str], peek_offset=0) -> [str, int, str]:
        position = 1 + peek_offset
        string_literal = self.reader.peek(position-1)
        while True:
            if self.reader.is_eof(position-1):
                break
            char = self.reader.peek(position)
            if char in end_of_content:
                position -= 1
                break
            position += 1
            string_literal += char
        return string_literal, position

    def _consume_until(self, end_of_content: tuple[str], *args) -> [str, int, str]:
        string_literal = self.reader.peek(0)
        position = 1
        while True:
            if self.reader.is_eof():
                break
            char = self.reader.consume()
            if char in end_of_content:
                self.reader.pos -= 1
                break
            position += 1
            string_literal += char
        return string_literal, position

    def tokenize(self, char: str, peek=True, peek_offset=0) -> [Optional[Token], int]:
        """Converts a character into a token."""
        method = self._peek_until if peek else self._consume_until
        pos = 1
        if char in [" ", "\n", "\t"]:
            token = None
        elif char in ["-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            num, pos = method(("\n", "\\"), peek_offset)
            token = Keyword(float(num.strip()) if "." in num else int(num.strip()))
        elif char == "{":
            token = Syntax(char)
        elif char == "}":
            token = Syntax(char)
        elif char == ":":
            token = Syntax(char)
        else:
            literal, pos = method(("{", ":", " ", "\n", '"'), peek_offset)
            if literal == '"':
                token = None
            else:
                if literal.startswith('"') and not literal.endswith('"'):
                    literal = literal + '"'
                token = Keyword(literal.strip())

        return token, pos

    def load(self, file: Path):
        """Reads content form a file path."""
        self.reader.load(file)

    def loads(self, string: str):
        """Reads the content from the string."""
        self.reader.loads(string)

    def peek(self, k: int = 1):
        """Returns a token without consuming it."""
        if self.reader.is_eof():
            return None
        tokens = []
        peek_pos = 1
        while True:
            if self.reader.is_eof() or len(tokens) >= k:
                break
            char = self.reader.peek(peek_pos)

            token, pos = self.tokenize(char, peek_offset=peek_pos)
            peek_pos += pos
            if token:
                tokens.append(token)

        return tokens[k-1]

    def consume(self, k: int = 1):
        """Returns a token and updates the position."""
        if self.reader.is_eof():
            return None
        tokens = []
        while True:
            if self.reader.is_eof() or len(tokens) >= k:
                break
            char = self.reader.consume()
            token, pos = self.tokenize(char, peek=False)
            if token:
                tokens.append(token)
        return tokens[k-1] if tokens else None


class Parser:
    """Builds an abstract syntax tree from tokens."""
    def __init__(self):
        self.lexer: Lexer = Lexer()
        self.parse_tree = None
        self._current_block = None

    @overload
    def parse(self, file: PathLike):
        """Parse content form a file path."""

    @overload
    def parse(self, string: str):
        """Parse content form a string."""

    def parse(self, path_or_string):
        if isinstance(path_or_string, PathLike):
            self.lexer.load(Path(path_or_string))
        else:
            self.lexer.loads(path_or_string)
        return self._parse()

    def _parse(self):
        blocks = []
        previous_token = None
        while True:
            token = self.lexer.consume()
            if token is None:
                break
            print(token)
            if self.parse_tree is None:
                # New document
                self.parse_tree = ASTBlock()
                self._current_block = self.parse_tree
            elif token == "{":
                # Create the block.
                block = ASTBlock()

                # Create the KeyValue that should hold the block
                kv = ASTKeyValue()
                # The key of the KeyValue is that previous tokens value
                kv.key = previous_token.value
                kv.value = block

                block.parent = kv

                self._current_block.children.append(kv)
                self._current_block = block
                blocks.append(self._current_block)

            elif token == ":":
                kv = ASTKeyValue()
                kv.key = previous_token.value
                if kv.key == "data" and isinstance(self.lexer.peek(2), Syntax):
                    print("data block")
                else:
                    # It's _not_ a data block
                    value_token = self.lexer.peek(1)
                    kv.value = value_token.value

                self._current_block.children.append(kv)
            elif token == "}":
                # exit of a block
                if not blocks:
                    raise DecodeError(self, "Miss-matched blocks. Extra '}'?")
                blocks.pop()
                if len(blocks):
                    self._current_block = blocks[-1]
            previous_token = token




            # if token == "{":
            #     if self.parse_tree is None:
            #         # New document
            #         self.parse_tree = ASTBlock()
            #         self._current_block = self.parse_tree
            #     else:
            #         if not self._current_block.children:
            #             # If it doesn't have children that means we are in within a nested block,
            #             # and we are the first child, we need to add the KeyValue the block should
            #             # be added to first.
            #             kv = ASTKeyValue()
            #             kv.key = 0
            #             self._current_block.children.append(kv)
            #         elif self._current_block.children[-1].value is not None:
            #             # If do have children, but their value is already set that means that
            #             # we are within a nested list and need to add the KeyValue that the block
            #             # should be added to first.
            #             inc = self._current_block.children[-1].key
            #             if not isinstance(self._current_block.children[-1].key, int):
            #                 inc = -1
            #             kv = ASTKeyValue()
            #             kv.key = inc + 1
            #             self._current_block.children.append(kv)
            #         # We add the new block to the latest KeyValue value.
            #         ast = ASTBlock()
            #         ast.parent = self._current_block.children[-1]
            #         self._current_block.children[-1].value = ast
            #         self._current_block = ast
            #     blocks.append(self._current_block)
            # elif token == "}":
            #     # exit of a block
            #     if not blocks:
            #         raise DecodeError(self, "Miss-matched blocks. Extra '}'?")
            #     blocks.pop()
            #     if len(blocks):
            #         self._current_block = blocks[-1]
            # elif isinstance(token, Keyword):
            #     kv = ASTKeyValue()
            #     kv.key = token.value
            #     self._current_block.children.append(kv)
            # elif isinstance(token, Literal):
            #     if self._current_block.children:
            #         if self._current_block.children[-1].value is None:
            #             self._current_block.children[-1].value = token.value
            #         else:
            #             kv = ASTKeyValue()
            #             kv.key = self._current_block.children[-1].key + 1
            #             kv.value = token.value
            #             self._current_block.children.append(kv)
            #     else:
            #         kv = ASTKeyValue()
            #         kv.key = 0
            #         kv.value = token.value
            #         self._current_block.children.append(kv)

        return self.parse_tree
