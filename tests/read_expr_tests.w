(import "wodehouse.w" read_expr)

(assert
    (eq (read_expr (stream "123"))
        123))

(assert
    (eq (read_expr (stream "\"mulliner\""))
        "mulliner"))

(assert
    (eq (read_expr (stream "jeeves"))
        'jeeves))

(assert
    (eq (read_expr (stream "   123   "))
        123))
(assert
    (eq (read_expr (stream "  #abc\n 123 #def  "))
        123))

(assert
    (eq (read_expr (stream "(123 abc   'def \"ghi\" # $$$$ \n)"))
        '(123 abc 'def "ghi")))
