(import wodehouse read_symbol)

(def test_reads_symbol_made_of_letters ()
    (assert
        (eq (read_symbol (stream "bertie"))
            'bertie)))

(def test_reads_symbols_of_math_signs ()
    (exec
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
                '>=))))
