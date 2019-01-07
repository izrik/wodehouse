import string

from functions.convert import int_from_str
from wtypes.list import WList
from wtypes.stream import WStream
from wtypes.string import WString
from wtypes.symbol import WSymbol, WSymbolAt


def parse(s):
    """
    (define parse
    (lambda (s)
        (read_expr
            (if
                (isinstance s 'Stream)
                s
                (stream s)))) )
    :param s:
    :return:
    """
    if not isinstance(s, WStream):
        s = WStream(str(s))
    return read_expr(s)


def read_whitespace_and_comments(s):
    """
(define read_comment_char
(lambda (s)
(cond
    ((not (has_chars s))
        '())
    ((eq (peek s) "\n")
        (cons (get_next_char s) (read_wsc_char s)))
    (true
        (cons (get_next_char s) (read_comment_char s))))))

(define read_comment
(lambda (s)
(if (not (eq (peek s) "#"))
    (raise
        (format
            "Unknown starting character \"{}\" in read_comment" (peek s)))
    (read_comment_char s))))

(define read_wsc_char
(lambda (s)
(cond
    ((not (has_chars s))
        '())
    ((eq (peek s) "#")
        (read_comment s))
    ((in (peek s) " \r\n\t")
        (cons (get_next_char s) (read_wsc_char s)))
    (true
        '()))))

(define read_whitespace_and_comments
(lambda (s)
(if (not (in (peek s) " \r\n\t#"))
    ""
    (+ (read_wsc_char s)))))
    """
    ch = s.peek()
    while s.has_chars() and (ch.isspace() or ch == '#'):
        if ch == '#':
            # read a comment
            while s.has_chars() and ch != '\n':
                s.get_next_char()
                ch = s.peek()
            if not s.has_chars():
                raise Exception(
                    "Ran out of characters before reading expression.")
        s.get_next_char()
        ch = s.peek()


def read_expr(s):
    """
(define read_expr
(lambda (s)
(let (whitespace (read_whitespace_and_comments s))
     (ch (peek s))
    (cond
        ((not (has_chars s))
            (raise "Ran out of characters before reading expression."))
        ((eq ch "(") (read_list s))
        ((in ch "0123456789") (read_integer_literal s))
        ((or (in ch "+-*/<>_") (in ch "abcdefghijklmnopqrstuvwxyz"))
            (read_symbol s))
        ((eq ch "\"") (read_string s))
        ((eq ch "'")
            (exec
                (get_next_char s)
                (list 'quote (read_expr s))))
        (true
            (raise
                (format
                    "Unknown starting character \"{}\" in read_expr"
                    ch)))))))
    """
    # _i = s.i
    ch = s.peek()
    if s.has_chars() and (ch.isspace() or ch == '#'):
        read_whitespace_and_comments(s)
    ch = s.peek()
    if not s.has_chars():
        raise Exception(
            "Ran out of characters before reading expression.")
    if ch == '(':
        return read_list(s)
    if ch in string.digits:
        return read_integer_literal(s)
    if ch in '+-*/<>_' or ch in string.ascii_letters:
        return read_symbol(s)
    if ch == '"':
        return read_string(s)
    if ch == '\'':
        s.get_next_char()
        expr = read_expr(s)
        return WList(WSymbol.get('quote'), expr)
    raise Exception('Unknown starting character "{}" in read_expr'.format(ch))


def read_string(s):
    """
    (define read_string_char
    (lambda (s)
    (if (not (has_chars s))
        (raise "Ran out of characters before string was finished.")
        (let (ch (get_next_char s))
        (if (eq ch "\"")
            '()
            (cons
                (if (eq ch "\\")
                    (if (not (has_chars s))
                        (raise (+ "Ran out of characters before escape "
                                  "sequence was finished."))
                        (let (ch2 (get_next_char s))
                        (cond
                            ((eq ch2 "n") "\n")
                            ((eq ch2 "r") "\r")
                            ((eq ch2 "t") "\t")
                            (true ch2))))
                    ch)
                (read_string_char s)))))))

    (define read_string
    (lambda (s)
    (let (delim (get_next_char s))
    (exec
        (assert (eq "\"" delim))
        (+ (read_string_char s))))))

    :param s:
    :return:
    """
    delim = s.get_next_char()
    assert delim == '"'
    chs = []
    while s.has_chars():
        ch = s.get_next_char()
        if ch == delim:
            value = ''.join(chs)
            return WString(value, position=s.get_position())
        if ch == '\\':
            ch = s.get_next_char()
            if ch == 'n':
                ch = '\n'
            if ch == 'r':
                ch = '\r'
            if ch == 't':
                ch = '\t'
        chs.append(ch)
    raise Exception('Ran out of characters before string was finished.')


def read_symbol(s):
    """
(define read_symbol
(lambda (s)
(let (ch (peek s))
(cond
    ((in ch "abcdefghijklmnopqrstuvwxyz_0123456789")
        (read_name s))
    ((in ch "+-*/")
        (let (_ (get_next_char s))
        (symbol_at ch (get_position s))))
    ((in ch "<>")
        (let (_ (get_next_char s))
             (ch2 (peek s))
               # note: side-effects in s prevent instruction re-ordering
            (if (eq ch2 "=")
                (let (_ (get_next_char s))
                    (symbol_at (+ ch ch2) (get_position s)))
                (symbol_at ch (get_position s)))))
    (true
        (raise
            (format
                "Unexpected character while reading symbol: \"{}\""
                ch)))))))
    """
    ch = s.peek()
    if ch in string.ascii_letters or ch in '_':
        return read_name(s)
    if ch in '+-*/':
        s.get_next_char()
        return WSymbolAt(ch, s.get_position())
    if ch in '<>':
        s.get_next_char()
        ch2 = s.peek()
        if ch2 == '=':
            s.get_next_char()
            return WSymbolAt(ch + ch2, position=s.get_position())
        return WSymbolAt(ch, position=s.get_position())
    raise Exception(
        "Unexpected character while reading symbol: \"{}\"".format(ch))


def read_name(s):
    """
(define read_name_char
(lambda (s)
(cond
    ((not (has_chars s))
        '())
    ((in (peek s) "abcdefghijklmnopqrstuvwxyz_0123456789")
        (cons (get_next_char s) (read_name_char s)))
    (true '()))))

(define read_name
(lambda (s)
(if (not (in (peek s) "abcdefghijklmnopqrstuvwxyz_"))
    (raise
        (format
            "Unexpected character at the beginning of a name: \"{}\""
             (peek s)))
    (symbol_at (+ (read_name_char s)) (get_position s)))))
    """
    chs = []
    assert s.peek() not in string.digits
    while s.has_chars() and \
            (s.peek() in string.ascii_letters or
             s.peek() in '_' or
             s.peek() in string.digits):
        chs.append(s.get_next_char())
    name = ''.join(chs)
    return WSymbolAt(name, position=s.get_position())


def read_integer_literal(s):
    """
(define read_integer_literal_char
(lambda (s)
(cond
    ((not (has_chars s))
        '())
    ((in (peek s) "0123456789")
        (cons (get_next_char s) (read_integer_literal_char s)))
    (true '()))))

(define read_integer_literal
(lambda (s)
(if (not (in (peek s) "0123456789"))
    (raise
        (format
            "Unexpected character at the beginning of integer literal: \"{}\""
            (peek s)))
    (int_from_str (+ (read_integer_literal_char s)) (get_position s)))))
    """
    chs = []
    while s.has_chars() and s.peek() in string.digits:
        chs.append(s.get_next_char())
    _s = ''.join(chs)
    return int_from_str(_s, position=s.get_position())


def read_list(s):
    """
(define read_list_element
(lambda (s)
(let (whitespace (read_whitespace_and_comments s))
    (if (not (has_chars s))
        (raise "Ran out of characters while reading the list.")
        (let (ch (peek s))
            (if (eq ch ")")
                (let (_ (get_next_char s))
                    '())
                (cons (read_expr s) (read_list_element s))))))))

(define read_list
(lambda (s)
(let (whitespace (read_whitespace_and_comments s))
    (if (not (has_chars s))
        (raise "Ran out of characters before starting the list.")
        (let (ch (get_next_char s))
            (if (not (eq ch "("))
                (raise
                    (format
                        "Unknown starting character \"{}\" in read_list" ch))
                (read_list_element s)))))))
    """
    assert s.peek() == '('
    exprs = []
    s.get_next_char()
    while True:
        while True:
            if not s.has_chars():
                raise Exception(
                    'Ran out of characters before list was finished.')
            ch = s.peek()
            if ch not in string.whitespace:
                break
            s.get_next_char()
        if s.peek() == ')':
            s.get_next_char()
            break
        expr = read_expr(s)
        exprs.append(expr)
    return WList(*exprs)
