(import "wodehouse.w" read_string read_string_char)

(assert
    (eq (read_string_char (stream "\""))
        '()))

(assert
    (eq (read_string (stream "\"clarence connie freddie beach\""))
        "clarence connie freddie beach"))

