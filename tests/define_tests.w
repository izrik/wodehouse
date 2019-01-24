
# given
(assert (not (in 'xyz (dir __module__))))
# when
(define xyz 123)
# then
(assert (in 'xyz (dir __module__)))
(assert (eq xyz 123))
