(import sys exit)

#####

(def main (argv)
    (if (eq argv '())
        (exec
            (print "Code coverage for Wodehouse.")
            0)
        (exec
            (print argv)
            0)))

#####

(if (eq __name__ "__main__")
    (exit
        (main (get sys 'argv))))
