(import sys exit)

#####

(def main (argv)
    (exec
        (print argv)
        0))

#####

(if (eq __name__ "__main__")
    (exit
        (main (get sys 'argv))))
