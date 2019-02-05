
(def test_define_adds_objects_to_scope ()
(exec
    # given
    (define s (new_scope_within __module__))
    (assert (not (in 'xyz (dir s))))
    # when
    (exec_src "(define xyz 123)" __builtins__ "unit_test" "<unit_test>" s)
    # then
    (assert (in 'xyz (dir s)))
    (assert (eq (get s 'xyz) 123))))
