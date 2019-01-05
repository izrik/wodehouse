
# given
(assert (not (in 'xyz (list_scope fls))))
# when
(define xyz 123)
# then
(assert (in 'xyz (list_scope fls)))
(assert (eq xyz 123))
