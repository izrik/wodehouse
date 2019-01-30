(import wodehouse read_string read_string_char)

(def test_rsc_terminates_on_dquote_returns_empty_list ()
    (assert
        (eq (read_string_char (stream "\""))
            '())))

(def test_rsc_reads_chars_terminated_by_dquote_returns_list_of_strings ()
    (exec
        (assert
            (eq (read_string_char (stream "c\""))
                '("c")))
        (assert
            (eq (read_string_char (stream "bc\""))
                '("b" "c")))
        (assert
            (eq (read_string_char (stream "abc\""))
                '("a" "b" "c")))))

(def test_reads_full_string ()
    (assert
        (eq (read_string (stream "\"clarence connie freddie beach\""))
            "clarence connie freddie beach")))

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

