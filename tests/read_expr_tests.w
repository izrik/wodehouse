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

#####

(define print_test_function_names false)

(def check_item (key)
    (exec
        # (print (format "key: {}" key))
        # (print (format "(str key): {}" (str key)))
        (let (obj (get __module__ key))
            (exec
                # (print (format "isinstance obj 'Function: {}" (isinstance obj 'Function)))
                (if (is_valid_test_function obj)
                    (run_test_func obj))))))

(def is_valid_test_function (obj)
    (if (isinstance obj 'Function)
        (starts_with (name_of obj) "test_")
        false))

(def run_test_func (func)
    (exec
        (if print_test_function_names
            (print (format "{}" (name_of func))))
        (func)
        (if (not print_test_function_names)
            (print "." ""))))

(map check_item (dir __module__))
