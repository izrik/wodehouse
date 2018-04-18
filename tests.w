(assert (< 1 2))
(assert (eq ((lambda (x) (* x x)) 4) 16))

(assert (not (in 'xyz (list_state fls))))
(define xyz 123)
(assert (in 'xyz (list_state fls)))
(assert (eq xyz 123))
