
# given
(assert (not (in 'xyz (list_state fls))))
# when
(define xyz 123)
# then
(assert (in 'xyz (list_state fls)))
(assert (eq xyz 123))
