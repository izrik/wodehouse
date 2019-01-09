
# given
(assert (not (in 'xyz (list_scope __module__))))
# when
(define xyz 123)
# then
(assert (in 'xyz (list_scope __module__)))
(assert (eq xyz 123))
