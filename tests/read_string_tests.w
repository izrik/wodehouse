(import wodehouse read_string read_string_char)

(def test_rsc_terminates_on_dquote_returns_empty_list ()
    (assert
        (eq (read_string_char (stream "\""))
            '())))

(def test_rsc_reads_chars_terminated_by_dquote_returns_list_of_strings ()
    (exec
        (assert
            (eq (read_string_char (stream "c\""))
                '("c")))
        (assert
            (eq (read_string_char (stream "bc\""))
                '("b" "c")))
        (assert
            (eq (read_string_char (stream "abc\""))
                '("a" "b" "c")))))

(def test_reads_full_string ()
    (assert
        (eq (read_string (stream "\"clarence connie freddie beach\""))
            "clarence connie freddie beach")))
