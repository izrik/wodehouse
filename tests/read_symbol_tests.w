(import "wodehouse.w" read_symbol read_name read_name_char)

(assert
    (eq (read_symbol (stream "bertie"))
        'bertie))
(assert
    (eq (read_symbol (stream "+"))
        '+))
(assert
    (eq (read_symbol (stream "<"))
        '<))
(assert
    (eq (read_symbol (stream "<="))
        '<=))
(assert
    (eq (read_symbol (stream ">"))
        '>))
(assert
    (eq (read_symbol (stream ">="))
        '>=))
