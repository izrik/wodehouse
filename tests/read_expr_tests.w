(import "wodehouse.w" read_expr read_whitespace_and_comments
    read_integer_literal read_integer_literal_char read_string read_string_char
    read_symbol read_name read_name_char)

(assert
    (eq (read_expr (stream "123"))
        123))

(assert
    (eq (read_expr (stream "\"mulliner\""))
        "mulliner"))

(assert
    (eq (read_expr (stream "jeeves"))
        'jeeves))
