(import wodehouse read_symbol)

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
