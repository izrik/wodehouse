(import "wodehouse.w" w_eval read_expr)

(assert
    (eq (w_eval (read_expr (stream "123")) (new_scope))
        123))
