
# given
(assert (not (in 'xyz (list_scope ms))))
# when
(define xyz 123)
# then
(assert (in 'xyz (list_scope ms)))
(assert (eq xyz 123))
