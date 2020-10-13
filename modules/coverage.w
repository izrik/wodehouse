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
        (print "    help    Get help on using coverage.")
        (print "")
        (print "Use \"coverage help <command>\" for detailed help on any command.")
        (print "For full documentation, please wait...")
        0))

#####

(if (eq __name__ "__main__")
    (exit
        (main (get sys 'argv))))
