import pytest

from deftree.ast.builder import Parser, Lexer, Keyword, Syntax


def test_lexer_peek():
    document = "blend_mode: BLEND_MODE_ALPHA"
    lexer = Lexer()
    lexer.loads(document)
    assert isinstance(lexer.peek(1), Keyword)
    assert isinstance(lexer.peek(2), Syntax)
    assert isinstance(lexer.peek(3), Keyword)


def test_lexer_consume():
    document = "blend_mode: BLEND_MODE_ALPHA"
    lexer = Lexer()
    lexer.loads(document)
    assert isinstance(lexer.consume(), Keyword)
    assert isinstance(lexer.consume(), Syntax)
    assert isinstance(lexer.consume(), Keyword)


def test_lexer_peek_block():
    document = """position {
  x: 0.0
}"""
    lexer = Lexer()
    lexer.loads(document)
    assert isinstance(lexer.peek(1), Keyword)
    assert isinstance(lexer.peek(2), Syntax)
    assert isinstance(lexer.peek(3), Keyword)
    assert isinstance(lexer.peek(4), Syntax)
    assert isinstance(lexer.peek(5), Keyword)


def test_doc():
    document = """animations {
  id: "anim"
  start_tile: 1
  end_tile: 1
  playback: PLAYBACK_ONCE_FORWARD
  fps: 30
  flip_horizontal: 0
  flip_vertical: 0
  position {
    x: 0.0
    y: 0.0
    z: 0.0
  }
}
extrude_borders: 20"""
    parser = Parser()
    tree = parser.parse(document)
    assert str(tree) == ('{animations: {id: "anim", start_tile: 1, end_tile: 1, playback: PLAYBACK_ONCE_FORWARD, '
                         "fps: 30, flip_horizontal: 0, flip_vertical: 0, position: {x: 0.0, y: 0.0, z: 0.0}, "
                         "extrude_borders: 20}}")


def test_line():
    document = "blend_mode: BLEND_MODE_ALPHA"
    parser = Parser()
    tree = parser.parse(document)

    assert str(tree) == "{blend_mode: BLEND_MODE_ALPHA}"


def test_line2():
    document = '''id: "anim"'''
    parser = Parser()
    tree = parser.parse(document)

    assert str(tree) == '{id: "anim"}'


def test_embedded():
    document = """embedded_components {
  data: "tile_set: \"\"\n"
  "default_animation: \"\"\n"
  "material: \"/builtins/materials/sprite.material\"\n"
  "blend_mode: BLEND_MODE_ALPHA\n"
  ""
  position {
    x: 0.0
  }
}
"""
    parser = Parser()
    tree = parser.parse(document)

    print(tree)
