(import sys exit)
(import runw run_module_with_rt add_emit_listener remove_emit_listener)

#####

(def main (argv)
    (if (eq argv '())
        (exec
            (print "Code coverage for Wodehouse.")
            0)
        (let (cmd_name (car argv))
            (if (not (in cmd_name commands_by_name))
                (exec
                    (print (format "Unknown command: '{}'" cmd_name))
                    (print "Use 'coverage help' for help.")
                    1)
                (let (cmd (car (get commands_by_name cmd_name)))
                    (cmd argv))))))

(def help_cmd (argv)
    (if (eq argv '())
        (exec
            (print "coverage module")
            (print "")
            (print "usage: wodehouse -m coverage <command> [options] [args]")
            (print "")
            (print "Commands:")
            (let (width (* (int (/ (get_max_width commands_by_name) 4)) 4))
                (map
                    (lambda command_name
                        (print_command_help command_name commands_by_name width))
                    (dir commands_by_name)))
            (print "")
            (print "Use \"coverage help <command>\" for detailed help on any command.")
            (print "For full documentation, please wait...")
            0)
        (exec
            (print (format "argv: {}" (str argv)))
            (let (cmd_name (car (cdr argv)))
                 (cmd_data (get commands_by_name cmd_name))
                (exec
                    (print (format "usage: wodehouse -m coverage {} [options] [args]" cmd_name))
                    (print "")
                    (print (car (cdr (cdr cmd_data))))
                    0)))))

(def print_command_help (command_name commands width)
    (let (space (* " " (+ (- width (len (str command_name))) 2)))
         (help_text (car (cdr (get commands command_name))))
        (print (format "    {}{}{}" command_name space help_text))))

(def get_max_width (commands)
    (get_max_width_1 (dir commands)))

(def max (a b)
    (if (> a b)
        a
        b))

(def get_max_width_1 (command_names)
    (let (cmd (car command_names))
         (rest (cdr command_names))
        (if (eq cmd '())
            0
            (max (len (str cmd))
                 (get_max_width_1 rest)))))

(def write_positions (filename positions)
    (exec
        (write_file filename "")
        (write_positions_1 filename positions)))

(def write_positions_1 (filename positions)
    (if (< (len positions) 1)
        0
        (exec
            (append_file filename (+ (str (car positions)) "\n"))
            (write_positions_1 filename (cdr positions))
            0)))

(def run_cmd (argv)
    (let (argv (cdr argv))
        (cond
            ((eq (car argv) "-m")
                (let (module_name (car (cdr argv)))
                     (rt (runtime (cdr (cdr argv))))
                     (all_positions (set))
                     (listener
                        (lambda (expr scope stack)
                            (exec
                                (add all_positions (position_of expr))
                                0)))
                    (exec
                        #(print (format "set size before: {}" (len all_positions)))
                        (add_emit_listener rt listener (get_current_scope))
                        (try
                            (run_module_with_rt rt module_name (cdr (cdr argv)))
                        (except SystemExit 0))
                        (remove_emit_listener rt listener)
                        #(print (format "set size after: {}" (len all_positions)))
                        (write_positions "coverage-w.txt" (to_list all_positions))
                        0)))
            (true
                (exec
                    # TODO: implement
                    (print "This is the run cmd")
                    (print argv)
                    0)))))

(def _get_positions_from_lines (lines)
    (if (eq lines '())
        '()
        (if (eq (car lines) "")
            (_get_positions_from_lines (cdr lines))
            (cons (position_from_str (car lines))
                (_get_positions_from_lines (cdr lines))))))

(def _get_modules_from_positions (positions)
    (if (eq positions '())
        '()
        (cons (filename_from_position (car positions))
            (_get_modules_from_positions (cdr positions)))))

(def _get_href_from_module_name (module)
    (+
        (replace
            (replace module "/" "_")
            "." "_")
        ".html"))

#########################
# HTML Report Templates #
#########################

(define _index_file_header """<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Coverage report</title>
    <link rel="stylesheet" href="style.css" type="text/css">
</head>
<body class="indexfile">
<div id="index">
    <table class="index">
        <thead>
        <tr class="tablehead" title="Click to sort">
            <th class="name left headerSortDown shortkey_n header">Module</th>
            <th class="shortkey_s header">statements</th>
            <th class="shortkey_m header">missing</th>
            <th class="shortkey_x header">excluded</th>
            <th class="shortkey_b header">branches</th>
            <th class="shortkey_p header">partial</th>
            <th class="right shortkey_c header">coverage</th>
        </tr>
        </thead>
        <tfoot>
        <tr class="total">
            <td class="name left">Total</td>
            <td>2355</td>
            <td>324</td>
            <td>0</td>
            <td>1033</td>
            <td>181</td>
            <td class="right" data-ratio="2805 3388">83%</td>
        </tr>
        <tr class="total_dynamic hidden">
            <td class="name left">Total</td>
            <td>2355</td>
            <td>324</td>
            <td>0</td>
            <td>1033</td>
            <td>181</td>
            <td class="right" data-ratio="2805 3388">83%</td>
        </tr>
        </tfoot>
        <tbody>
""")

(define _index_file_row_template """        <tr class="file">
            <td class="name left"><a href="{}">{}</a></td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td>0</td>
            <td class="right" data-ratio="0 0">100%</td>
        </tr>
""")

(define _index_file_footer """        </tbody>
    </table>
    <p id="no_rows" style="display: none;">
        No items found using the specified filter.
    </p>
</div>
<div id="footer">
    <div class="content">
        <p>
            <a class="nav" href="https://github.com/izrik/wodehouse">wodehouse v0.1</a>,
            created at 2020-10-26 09:01
        </p>
    </div>
</div>
</body>
</html>""")

(define _module_file_template """
This is the file contents: {} {}
""")

################

(def _generate_index_file (modules positions)
    (apply +
        (+
            (list _index_file_header)
            (map
                (lambda (module)
                    (let (href (_get_href_from_module_name module))
                        (format
                            _index_file_row_template
                            href
                            module)))
                modules)
        (list _index_file_footer))))

(def _generate_module_file (module positions)
    (let (filename (_get_href_from_module_name module))
        (format
            _module_file_template
            module
            filename)))

(def _write_module_files (modules positions)
    (if (eq modules '())
        0
        (let (module (car modules))
             (filename (_get_href_from_module_name module))
            (exec
                (print (format "Writing module {} to file {}" module filename))
                (write_file
                    (+ "whtmlcov/" filename)
                    (_generate_module_file module positions))
                (_write_module_files (cdr modules) positions)))))

(def _get_exprs_from_stream (s)
    (let (_ (read_whitespace_and_comments s))
        (if (not (has_chars s))
            '()
            (cons
                (try
                    (read_expr s)
                (except as e
                    (raise
                        (format "Error reading expressions from \"{}\": {}"
                            (get_position s)
                            (get_message e)))))
                (_get_exprs_from_stream s)))))

(def _get_exprs_from_file (contents)
    (let (s (stream contents))
         (exprs (_get_exprs_from_stream s))
        exprs))

(def _get_positions_from_exprs (exprs)
    (if (eq exprs '())
        '()
        (cons
            (position_of (car exprs))
            (_get_positions_from_exprs (cdr exprs)))))

(def _calculate_coverage_by_modules (modules positions_set)
    (if (eq modules '())
        '()
        (exec
            (print (format "Calulating coverage for {}" (car modules)))
        (cons
            (if (starts_with (car modules) "<")
                '(0 0)
                (let (module (car modules))
                     (contents (read_file module))
                     (exprs (_get_exprs_from_file contents))
                     (expr_positions (apply set (_get_positions_from_exprs exprs)))
                     (matching_positions (intersect expr_positions positions_set))
                    (list (len matching_positions) (len expr_positions))))
            (_calculate_coverage_by_modules (cdr modules) positions_set))))
        )

(def html_cmd (argv)
    (exec
        (print "Starting to produce html report from coverage numbers")
        (let (contents (read_file "coverage-w.txt"))
             (lines (split contents "\n"))
             (positions (_get_positions_from_lines lines))
             (modules (to_list (apply set (_get_modules_from_positions positions))))
             (exec
                (print (format "Found the following modules:\n  {}\n" (join "\n  " modules)))
                (let (coverage_by_module (_calculate_coverage_by_modules modules (apply set positions)))
                    (exec
                        (write_file "whtmlcov/index.html"
                            (_generate_index_file modules positions coverage_by_module))
                        (_write_module_files modules positions)))))))

(define commands_by_name
    (new_scope (list
        (list 'help (list help_cmd
                          "Get help on using coverage"
                          "Get help on using coverage"))
        (list 'run  (list run_cmd
                          "Run a Wodehouse command and measure code execution."
                          "Run a module and collect coverage info."))
        (list 'html (list html_cmd
                          "Generate an html report from the execution results."
                          "Generate an HTML report from the results of a previous invocation of 'coverage run'."))  )))

#####

(if (eq __name__ "__main__")
    (exit
        (main (get sys 'argv))))
