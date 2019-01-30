
(def test_define_adds_objects_to_scope ()
(exec
    # given
    (define s (new_scope_within __module__))
    (assert (not (in 'xyz (dir s))))
    # when
    (exec_src "(define xyz 123)" __builtins__ "<unit_test>" s)
    # then
    (assert (in 'xyz (dir s)))
    (assert (eq (get s 'xyz) 123))))

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
