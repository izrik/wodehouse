(import "wodehouse.w" read_string read_string_char)

(assert
    (eq (read_string_char (stream "\""))
        '()))
(assert
    (eq (read_string_char (stream "c\""))
        '("c")))
(assert
    (eq (read_string_char (stream "bc\""))
        '("b" "c")))
(assert
    (eq (read_string_char (stream "abc\""))
        '("a" "b" "c")))

(assert
    (eq (read_string (stream "\"clarence connie freddie beach\""))
        "clarence connie freddie beach"))

