(import "wodehouse.w" read_list)

(assert
    (eq (read_list (stream "()"))
        '()))

(assert
    (eq (read_list (stream "(one)"))
        '(one)))
(assert
    (eq (read_list (stream "(one two three)"))
        '(one two three)))

(assert
    (eq (read_list (stream "((1))"))
        '((1))))

(assert
    (eq (read_list (stream "(1 (2 (3 (4 (5)))))"))
        '(1 (2 (3 (4 (5)))))))
