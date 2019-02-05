(import wodehouse w_eval read_expr)

(def test_evals_integer_literal ()
    (assert
        (eq (w_eval (read_expr (stream "123")) (new_scope))
            123)))
