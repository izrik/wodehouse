(import sys exit)
(import argparse parse_args)

#####

(def main (argv)
    (let (parsed # TODO: manually parse argv without argparse?
                 #(parse_args '((source ("--source"     ) 1 "")
                 #              (append ("-a" "--append") 0 false)
                 #              (module ("-m") 1 ""))
                 #             argv))
                 (new_scope '((module "unittest")
                              (source "cover_example.w")
                              (__remaining_argv__ ("-s" "tests/modules")))))
        (if (and (not (in '__remaing_argv__ parsed))
                 (not (in 'module parsed)))
            (print "Nothing to do.")
            (let (run_as_module (in 'module parsed))
                 (item_to_run (if run_as_module
                                (get parsed 'module)
                                (first (get parsed '__remaining_argv__))))
                 (argv2 (if (in '__remaining_argv__ parsed)
                            (if run_as_module
                                (get parsed '__remaining_argv__)
                                (cdr (get parsed '__remaining_argv__)))
                            '()))
                 (source_files (split (get parsed 'source) ","))
                 (sources (map read_file source_files))
                 (parsed_sources (map parse sources))
                 (exprs (apply + (map get_all_exprs parsed_sources)))
                 (pairs (map (lambda (x) (list (position_of x) false)) exprs))
                 (positions (new_scope pairs))
                (exec
                    (print ("about to run stuff"))
                    (let (pos_and_rv
                            (with_capture_exprs
                                ((if run_as_module run_module run_file)
                                    item_to_run argv2)))
                         (captures (first pos_and_rv))
                         (evaled_positions
                            (filter
                                (lambda (key) (get positions key))
                                (dir positions)))
                        (exec
                            (map
                                (lambda (content)
                                    (append_file ".wcoverage" (str content)))
                                evaled_positions)
                            0)))))))

(def get_filename_from_pos_str (s)
    (nth (split s ":") 0))

(def get_line_num_from_pos_str (s)
    (nth (split (nth (split s ":") 1) ",") 0))

(def get_char_num_from_pos_str (s)
    (nth (split s ",") 1))

(def get_all_exprs (e)
    (if (not (isinstance e 'List))
        (list e)
        (cons e (apply + (map get_all_exprs e)))))

#####

(if (eq __name__ "__main__")
    (exit
        (main (get sys 'argv))))
