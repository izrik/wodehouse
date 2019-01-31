(import argparse parse_args)
(import sys)

(define print_test_function_names false)

(def main (argv)
    (let (parsed (parse_args '((start ("-s" "--start-directory") 1 ".")) argv))
        (let (tests (gather_tests_in_folder (get parsed 'start)))
            (exec
                (run_tests tests)
                (if (not print_test_function_names) (print ""))
                (print (format "Ran {} tests. All tests passed." (len tests)))))))

(def gather_tests_in_folder (folder)
    (if (not (is_dir folder))
        (raise (format "Path \"{}\" is not a directory." folder))
        (gather_tests_in_folder_items folder (list_dir folder))))

(def gather_tests_in_folder_items (folder items)
    (if (eq items '())
        '()
        (let (basename (car items))
             (item (+ folder "/" (car items)))
            (+  (gather_tests_in_folder_items folder (cdr items))
                (if (is_dir item)
                    (if (is_excluded_folder basename)
                        '()
                        (gather_tests_in_folder item))
                    (if (is_file item)
                        (if (is_excluded_file basename)
                            '()
                            (gather_tests_in_file item))
                        (raise
                            (format
                                "Path \"{}\" is neither a directory nor a file."
                                item))))))))

(def is_excluded_file (item)
    (or (is_excluded_folder item)
        (not (ends_with item ".w"))))

(def is_excluded_folder (item)
    (or (starts_with item "__")
        (starts_with item ".")))

(def gather_tests_in_file (file)
    (let (s (exec_src (read_file file) __builtins__ file
                        (module __builtins__ file file)))
        (filter is_valid_test_function
                (map (lambda (key) (get s key)) (dir s)))))

(def is_valid_test_function (obj)
    (if (isinstance obj 'Function)
        (starts_with (name_of obj) "test_")
        false))

(def run_tests (tests)
    (map run_test_func tests))

(def run_test_func (func)
    (exec
        (if print_test_function_names
            (print (format "{}" (name_of func))))
        (func)
        (if (not print_test_function_names)
            (print "." ""))))

#####

(main (cdr (get sys 'argv)))
