(import wodehouse read_list)

(def test_reads_empty_list ()
    (assert
        (eq (read_list (stream "()"))
            '())))

(def test_reads_list_of_single_item ()
    (assert
        (eq (read_list (stream "(one)"))
            '(one))))

(def test_reads_list_of_multiple_items ()
    (assert
        (eq (read_list (stream "(one two three)"))
            '(one two three))))

(def test_reads_list_within_list ()
    (assert
        (eq (read_list (stream "((1))"))
            '((1)))))

(def test_reads_severally_nested_lists ()
    (assert
        (eq (read_list (stream "(1 (2 (3 (4 (5)))))"))
            '(1 (2 (3 (4 (5))))))))
