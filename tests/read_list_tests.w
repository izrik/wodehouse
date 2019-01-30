(import wodehouse read_list)

(def test_reads_empty_list ()
    (assert
        (eq (read_list (stream "()"))
            '())))

(def test_reads_list_of_single_item ()
    (assert
        (eq (read_list (stream "(one)"))
            '(one))))

(def test_reads_list_of_multiple_items ()
    (assert
        (eq (read_list (stream "(one two three)"))
            '(one two three))))

(def test_reads_list_within_list ()
    (assert
        (eq (read_list (stream "((1))"))
            '((1)))))

(def test_reads_severally_nested_lists ()
    (assert
        (eq (read_list (stream "(1 (2 (3 (4 (5)))))"))
            '(1 (2 (3 (4 (5))))))))

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
