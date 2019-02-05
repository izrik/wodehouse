(import wodehouse read_whitespace_and_comments)

(def test_reads_comment_terminated_by_newline ()
    (assert
        (eq (read_whitespace_and_comments (stream "# this is a comment\n"))
            "# this is a comment\n")))

(def test_reads_comment_terminated_by_end_of_string ()
    (assert
        (eq (read_whitespace_and_comments (stream "# this is a comment"))
            "# this is a comment")))

(def test_reads_spaces ()
    (assert
        (eq (read_whitespace_and_comments (stream "   "))
            "   ")))

(def test_reads_cr_and_lf_and_tabs ()
    (assert
        (eq (read_whitespace_and_comments (stream "\r\n\t"))
            "\r\n\t")))

(def test_reads_all_kinds_of_whitespace ()
    (assert
        (eq (read_whitespace_and_comments (stream "# abc\r\n\t #def"))
            "# abc\r\n\t #def")))

(def test_does_not_read_non_whitespace ()
    (assert
        (eq (read_whitespace_and_comments (stream "123"))
            "")))
