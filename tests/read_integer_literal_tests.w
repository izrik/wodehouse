(import wodehouse read_integer_literal)

(def test_reads_integer_literal ()
    (assert
        (eq (read_integer_literal (stream "123"))
            123)))
