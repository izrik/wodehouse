(import "wodehouse.w" read_whitespace_and_comments read_wsc_char read_comment
    read_comment_char)

(assert
    (eq (read_whitespace_and_comments (stream "# this is a comment\n"))
        "# this is a comment\n"))
(assert
    (eq (read_whitespace_and_comments (stream "# this is a comment"))
        "# this is a comment"))

(assert
    (eq (read_whitespace_and_comments (stream "   "))
        "   "))

(assert
    (eq (read_whitespace_and_comments (stream "\r\n\t"))
        "\r\n\t"))
(assert
    (eq (read_whitespace_and_comments (stream "# abc\r\n\t #def"))
        "# abc\r\n\t #def"))


(assert
    (eq (read_whitespace_and_comments (stream "123"))
        ""))
