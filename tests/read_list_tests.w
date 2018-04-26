(import "wodehouse.w" read_expr read_whitespace_and_comments
    read_integer_literal read_integer_literal_char read_string read_string_char
    read_symbol read_name read_name_char read_whitespace_and_comments
    read_wsc_char read_comment read_comment_char read_list read_list_element)

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
