(import argparse parse_args)
(import sys)

(define print_test_function_names false)

(def main (argv)
    (let (parsed (parse_args '((start ("-s" "--start-directory") 1 ".")) argv))
        (let (tests (gather_tests_in_folder (get parsed 'start)))
            (let (results (run_tests tests))
                (let (failures (filter is_failure results))
                    (let (num_failed (len failures))
                        (exec
                            (if (not print_test_function_names) (print ""))
                            (if (> num_failed 0)
                                (map print_failure failures))
                            (print "----------------------------------------------------------------------")
                            (print (format "Ran {} tests." (len tests)))
                            (print "")
                            (if (eq 0 num_failed)
                                (print "OK")
                                (print (format "FAILED (failures={})" num_failed))))))))))

(def is_failure (x)
    (not (eq x ".")))

(def print_failure (x)
    (let (func (car x))
         (exc (nth x 1))
        (exec
            # TODO: print the function's containing module or class
            (print "======================================================================")
            (print (format "FAIL: {}" (name_of func)))
            (print "----------------------------------------------------------------------")
            (print (format_stacktrace exc))
            (print (format "Exception: {}" (get_message exc)))
            (print ""))))

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
    (let (s (exec_src (read_file file) __builtins__ "name" file
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
            (print (format "{} " (name_of func)) ""))
        (let (result
                (try
                    (exec
                        (eval (list func) (get_current_scope))
                        ".")
                (except as e
                    (list func e))))
            (exec
                (if print_test_function_names
                    (print "")
                    (print (if (eq "." result) "." "F") ""))

                result))))

#####

(if (eq __name__ "__main__")
    (main (get sys 'argv)))
