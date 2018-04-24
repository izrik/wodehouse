(import "wodehouse.w" read_integer_literal read_integer_literal_char)

(assert
    (eq (read_integer_literal (stream "123"))
        123))
