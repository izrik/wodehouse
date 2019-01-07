(import "wodehouse.w" read_integer_literal)

(assert
    (eq (read_integer_literal (stream "123"))
        123))
