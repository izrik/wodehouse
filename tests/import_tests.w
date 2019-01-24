
(assert (not (in 'example (dir __module__))))
(import example)
(assert (in 'example (dir __module__)))
(assert (isinstance example 'Scope))
#(assert (eq (dir example) '(import __module__ something define)))
(assert (not (in 'define (dir example))))
(assert (in '__module__ (dir example)))
(assert (not (in 'import (dir example))))
(assert (in 'something (dir example)))
(assert (not (eq __module__ (get example '__module__))))
(assert (eq example (get example '__module__)))

# importing with additional names imports those names into the current module
# given
(assert (not (in 'something (dir __module__))))
# when
(import example something)
# then
(assert (in 'something (dir __module__)))
(assert (eq something "abc"))

# importing caches and re-uses the __module__
# given
(assert (eq example example))
(define example_one example)
(assert (eq example example_one))
# when
(import example)
# then
(define example_two example)
(assert (eq example_one example_two))
