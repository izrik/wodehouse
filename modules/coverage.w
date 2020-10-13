(import sys exit)

#####

(def main (argv)
    (if (eq argv '())
        (exec
            (print "Code coverage for Wodehouse.")
            0)
        (if (eq (car argv) "help")
            (help (cdr argv))
            (exec
                (print argv)
                0))))

(def help (argv)
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

(define commands_by_name
    (new_scope (list
        (list 'help (list help "Get help on using coverage")))))

#####

(if (eq __name__ "__main__")
    (exit
        (main (get sys 'argv))))
