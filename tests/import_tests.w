
(assert (not (in 'example (list_scope ms))))
(import "example.w")
(assert (in 'example (list_scope ms)))
(assert (isinstance example 'Scope))
#(assert (eq (list_scope example) '(import ms something define)))
(assert (in 'define (list_scope example)))
(assert (in 'ms (list_scope example)))
(assert (in 'import (list_scope example)))
(assert (in 'something (list_scope example)))
(assert (not (eq define (get example 'define))))
(assert (not (eq import (get example 'import))))
(assert (not (eq ms (get example 'ms))))
(assert (eq example (get example 'ms)))

# importing with additional names imports those names into the current ms
# given
(assert (not (in 'something (list_scope ms))))
# when
(import "example.w" something)
# then
(assert (in 'something (list_scope ms)))
(assert (eq something "abc"))

# importing caches and re-uses the ms
# given
(assert (eq example example))
(define example_one example)
(assert (eq example example_one))
# when
(import "example.w")
# then
(define example_two example)
(assert (eq example_one example_two))
