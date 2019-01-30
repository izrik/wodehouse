
(def test_adds_the_imported_module_to_the_importing_module_scope ()
    (exec
        # given
        (define s (new_scope_within __module__))

        # precondition
        (assert (not (in 'example (dir s))))

        # when
        (exec_src "(import example)" __builtins__ "<unit_test>" s)

        # then

        # the imported module is in the scope
        (assert (in 'example (dir s)))
        (define example (get s 'example))

        # and the imported module is a scope (module is a sub-type of scope)
        (assert (isinstance example 'Scope))
        #(assert (eq (dir example) '(import s something define)))

        # and the imported module does not include builtins
        (assert (not (in 'define (dir example))))

        # and the imported module has a __module__
        (assert (in '__module__ (dir example)))

        # and the imported module's __module__ is itself
        (assert (eq example (get example '__module__)))

        # and the importing scope is not the imported module's __module__
        (assert (not (eq s (get example '__module__))))

        # and items define'd in example.w are present in the imported module
        (assert (in 'something (dir example)))))

(def test_additional_names_imports_those_names_into_importing_scope ()
    # importing with additional names imports those names into the current module
    (exec
        # given
        (define s (new_scope_within __module__))
        # precondition
        (assert (not (in 'something (dir s))))
        # when
        (exec_src "(import example something)" __builtins__ "<unit_test>" s)
        # then
        (assert (in 'something (dir s)))
        (assert (eq (get s 'something) "abc"))))

(def test_importing_caches_and_reuses__module__ ()
    # importing caches and re-uses the __module__
    (exec
        # given
        (define s (new_scope_within __module__))
        (exec_src "(import example)" __builtins__ "<unit_test>" s)
        (define example_one (get s 'example))
        (define s2 (new_scope_within __module__))

        # precondition
        (assert (not (in 'example (dir s2))))

        # when
        (exec_src "(import example)" __builtins__ "<unit_test>" s2)

        # then the module is in the second scope
        (assert (in 'example (dir s2)))

        # and the first and second example are the same
        (define example_two (get s2 'example))
        (assert (eq example_one example_two))))

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
