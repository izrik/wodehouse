
# Parse command-line arguments
# `params` takes the form
#   (('name1 '(flag1a flag1b flag1c) nargs{0,1})
#    ('name2 '(flag2a flag2b flag2c) nargs{0,1})
#    ...
#    ('nameN '(flagNa flagNb flagNc) nargs{0,1}))

(def parse_args (params args)
    # TODO: if args not specified, use sys.argv
    #   TODO: (param default values) or (optional params)
    # TODO: check params
    (parse_args_into_scope params args '()))

(def parse_args_into_scope (params args pairs)
    (if (eq args '())
        (new_scope pairs)
        (let (m (match_arg_to_params args params))
            (if (eq m '())
                (new_scope (cons (list '__remaining_argv__ args) pairs))
                (parse_args_into_scope params (car m) (cons (cdr m) pairs))))))

(def match_arg_to_params (args params)
    (if (eq params '())
        '()
        (let (arg (car args))
             (param (car params))
            (let (pname (car param))
                 (pflags (car (cdr param)))
                 (pnum_args (car (cdr (cdr param))))
                (if (match_arg_to_flags arg pflags)
                    (cond
                        ((eq pnum_args 0)
                            (list (cdr args) pname true))
                        ((eq pnum_args 1)
                            (list (cdr (cdr args)) pname (car (cdr args))))
                        (true
                            (raise (format "Invalid num_args for parameter {}: expected 0 or 1, got {} instead" pname pnum_args))))
                    (match_arg_to_params args (cdr params)))))))

(def match_arg_to_flags (arg flags)
    (if (eq flags '())
        false
        (if (eq arg (car flags))
            true
            (match_arg_to_flags arg (cdr flags)))))
