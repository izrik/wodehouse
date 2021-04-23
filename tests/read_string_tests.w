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

#########################
# Triple-quoted strings #
#########################

(def test_triple_regular_string ()
    (assert
        (eq (read_string (stream "\"\"\"abc\"\"\""))
            "abc")))

(def test_triple_empty_string ()
    (assert
        (eq (read_string (stream "\"\"\"\"\"\""))
            "")))

(def test_triple_escaped_dquote ()
    (let (s (stream "\"\"\"\\\"\"\"\""))
        (exec
            (assert (eq (get_stream_index s) 0))
            (assert
                (eq (read_string s)
                    "\""))
            (assert (eq (get_stream_index s) 8)))))

(def test_triple_newline_also_included ()
    (let (s (stream "\"\"\"\n\"\"\""))
        (exec
            (assert (eq (get_stream_index s) 0))
            (assert
                (eq (read_string s)
                    "\n"))
            (assert (eq (get_stream_index s) 7)))))

(def test_triple_escaped_newline ()
    (let (s (stream "\"\"\"\\n\"\"\""))
        (exec
            (assert (eq (get_stream_index s) 0))
            (assert
                (eq (read_string s)
                    "\n"))
            (assert (eq (get_stream_index s) 8)))))

(def test_triple_escaped_tab ()
    (let (s (stream "\"\"\"\\t\"\"\""))
        (exec
            (assert (eq (get_stream_index s) 0))
            (assert
                (eq (read_string s)
                    "\t"))
            (assert (eq (get_stream_index s) 8)))))

(def test_triple_no_closing_delim_raises ()
    (let (s (stream "\"\"\"abc"))
        (exec
            (assert (eq (get_stream_index s) 0))
            (try
                (exec
                    (read_string s)
                    (raise "The function did not raise an error"))
            (except as e
                (assert
                 (eq (get_message e)
                     "Ran out of characters before string was finished."))))
            (assert (eq (get_stream_index s) 6)))))

(def test_triple_not_enough_closing_delim_raises_1 ()
    (let (s (stream "\"\"\"abc\""))
        (exec
            (assert (eq (get_stream_index s) 0))
            (try
                (exec
                    (read_string s)
                    (raise "The function did not raise an error"))
            (except as e
                (assert
                 (eq (get_message e)
                     "Ran out of characters before string was finished."))))
            (assert (eq (get_stream_index s) 7)))))

(def test_triple_not_enough_closing_delim_raises_2 ()
    (let (s (stream "\"\"\"abc\"\""))
        (exec
            (assert (eq (get_stream_index s) 0))
            (try
                (exec
                    (read_string s)
                    (raise "The function did not raise an error"))
            (except as e
                (assert
                 (eq (get_message e)
                     "Ran out of characters before string was finished."))))
            (assert (eq (get_stream_index s) 8)))))

(def test_triple_embedded_dquote ()
    (let (s (stream "\"\"\"a\"b\"\"\""))
        (exec
            (assert (eq (get_stream_index s) 0))
            (assert (eq (read_string s) "a\"b"))
            (assert (eq (get_stream_index s) 9)))))

(def test_triple_two_embedded_dquotes ()
    (let (s (stream "\"\"\"a\"\"b\"\"\""))
        (exec
            (assert (eq (get_stream_index s) 0))
            (assert (eq (read_string s) "a\"\"b"))
            (assert (eq (get_stream_index s) 10)))))
