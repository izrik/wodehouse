
(assert (not (in 'example (list_scope __module__))))
(import "example.w")
(assert (in 'example (list_scope __module__)))
(assert (isinstance example 'Scope))
#(assert (eq (list_scope example) '(import __module__ something define)))
(assert (in 'define (list_scope example)))
(assert (in '__module__ (list_scope example)))
(assert (in 'import (list_scope example)))
(assert (in 'something (list_scope example)))
(assert (eq define (get example 'define)))
(assert (eq import (get example 'import)))
(assert (not (eq __module__ (get example '__module__))))
(assert (eq example (get example '__module__)))

# importing with additional names imports those names into the current module
# given
(assert (not (in 'something (list_scope __module__))))
# when
(import "example.w" something)
# then
(assert (in 'something (list_scope __module__)))
(assert (eq something "abc"))

# importing caches and re-uses the __module__
# given
(assert (eq example example))
(define example_one example)
(assert (eq example example_one))
# when
(import "example.w")
# then
(define example_two example)
(assert (eq example_one example_two))
