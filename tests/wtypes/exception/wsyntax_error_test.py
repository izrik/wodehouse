
from wtypes.exception import WSyntaxError
from wtypes.position import Position


def test_create():
    # when
    e = WSyntaxError('this is the message',
                     Position('module.w', 2, 3, None))
    # then
    assert e is not None
    assert e.message == 'this is the message'
    assert e.position.filename == 'module.w'
    assert e.position.line == 2
    assert e.position.char == 3
