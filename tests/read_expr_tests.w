(import wodehouse read_expr)

(def test_reads_integer_literals ()
    (assert
        (eq (read_expr (stream "123"))
            123)))

(def test_reads_string_literals ()
    (assert
        (eq (read_expr (stream "\"mulliner\""))
            "mulliner")))

(def test_reads_symbols ()
    (assert
        (eq (read_expr (stream "jeeves"))
            'jeeves)))

(def test_ignores_whitespace_and_comments ()
    (exec
        (assert
            (eq (read_expr (stream "   123   "))
                123))
        (assert
            (eq (read_expr (stream "  #abc\n 123 #def  "))
                123))))

(def test_reads_lists ()
    (assert
        (eq (read_expr (stream "(123 abc   'def \"ghi\" # $$$$ \n)"))
            '(123 abc 'def "ghi"))))
