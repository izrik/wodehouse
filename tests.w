(assert (< 1 2))
(assert (eq ((lambda (x) (* x x)) 4) 16))

(assert (not (in 'xyz (list_state fls))))
(define xyz 123)
(assert (in 'xyz (list_state fls)))
(assert (eq xyz 123))

(assert (not (in 'example (list_state fls))))
(import "example.w")
(assert (in 'example (list_state fls)))
(assert (isinstance example 'State))
#(assert (eq (list_state example) '(import fls something define)))
(assert (in 'define (list_state example)))
(assert (in 'fls (list_state example)))
(assert (in 'import (list_state example)))
(assert (in 'something (list_state example)))
(assert (not (eq define (get example 'define))))
(assert (not (eq import (get example 'import))))
(assert (not (eq fls (get example 'fls))))
(assert (eq example (get example 'fls)))

# importing with additional names imports those names into the current fls
(assert (not (in 'something (list_state fls))))
(import "example.w" something)
(assert (in 'something (list_state fls)))

# importing caches and re-uses the fls
(assert (eq example example))
(define example_one example)
(assert (eq example example_one))
(import "example.w")
(define example_two example)
(assert (eq example_one example_two))
