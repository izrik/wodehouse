
(assert (not (in 'example (list_scope fls))))
(import "example.w")
(assert (in 'example (list_scope fls)))
(assert (isinstance example 'Scope))
#(assert (eq (list_scope example) '(import fls something define)))
(assert (in 'define (list_scope example)))
(assert (in 'fls (list_scope example)))
(assert (in 'import (list_scope example)))
(assert (in 'something (list_scope example)))
(assert (not (eq define (get example 'define))))
(assert (not (eq import (get example 'import))))
(assert (not (eq fls (get example 'fls))))
(assert (eq example (get example 'fls)))

# importing with additional names imports those names into the current fls
# given
(assert (not (in 'something (list_scope fls))))
# when
(import "example.w" something)
# then
(assert (in 'something (list_scope fls)))
(assert (eq something "abc"))

# importing caches and re-uses the fls
# given
(assert (eq example example))
(define example_one example)
(assert (eq example example_one))
# when
(import "example.w")
# then
(define example_two example)
(assert (eq example_one example_two))
