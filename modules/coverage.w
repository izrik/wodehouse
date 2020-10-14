(import sys exit)
(import runw run_module_with_rt)

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
        0))

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

(def run_cmd (argv)
    (let (argv (cdr argv))
        (cond
            ((eq (car argv) "-m")
                (let (module_name (car (cdr argv)))
                     (rt (runtime (cdr (cdr argv))))
                    (run_module_with_rt rt module_name (cdr (cdr argv)))))
            (true
                (exec
                    (print "This is the run cmd")
                    (print argv)
                    0)))))

(define commands_by_name
    (new_scope (list
        (list 'help (list help_cmd "Get help on using coverage"))
        (list 'run (list run_cmd "Run a Wodehouse command and measure code execution."))) ))

#####

(if (eq __name__ "__main__")
    (exit
        (main (get sys 'argv))))
