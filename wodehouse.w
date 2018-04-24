(define w_eval
(lambda (expr state)
    (cond
    ((isinstance expr 'Symbol)
        (get state expr))
    ((isinstance expr '(Number String Boolean))
        expr)
    ((isinstance expr 'List)
        (let (head (car expr))
        (if
            (eq head 'quote)
            (car (cdr expr))
            (let (callee w_eval(head state))
            (let (args (cdr expr))
            (cond
            ((isinstance callee 'Macro)
                (let (exprs_state (call_macro callee args state))
                (let (exprs (car exprs_state))
                (let (state (car (cdr exprs_state)))
                (w_eval exprs state)))))
            ((not (isinstance callee 'Function))
                (raise
                    (format
                        "Callee is not a function. Got \"{}\" ({}) instead."
                        callee
                        (type callee))))
            (true
                (let (args
                    (map
                        (lambda (name value)
                            (list name (w_eval value state)))
                        args (get_func_args callee)))
                (let (state (new_state_proto state args))
                (if
                    (isinstance callee 'MagicFunction)
                    implementation_specific
                    (w_eval (second callee) state)))))))))))
    (true
        (raise
            (format
                "Unknown object type: \"{}\" ({})" expr (type expr))))))
)


(define read_string_char
(lambda (s)
(if (not (has_chars s))
    (raise "Ran out of characters before string was finished.")
    (let (ch (get_next_char s))
    (if (eq ch "\"")
            '()
            (cons
                (if (eq ch "\\")
                    (if (not (has_chars s))
                        (raise (+ "Ran out of characters before escape "
                                  "sequence was finished."))
                        (let (ch2 (get_next_char s))
                        (cond
                            ((eq ch2 "n") "\n")
                            ((eq ch2 "r") "\r")
                            ((eq ch2 "t") "\t")
                            (true ch2))))
                    ch)
                (read_string_char s)))))))

(define read_string
(lambda (s)
(let (delim (get_next_char s))
(exec
    (assert (eq "\"" delim))
    (+ (read_string_char s))))))


(define read_symbol
(lambda (s)
(let (ch (peek s))
(cond
    ((in ch "abcdefghijklmnopqrstuvwxyz_0123456789")
        (read_name s))
    ((in ch "+-*/")
        (let (_ (get_next_char s))
        (symbol_at ch (get_position s))))
    ((in ch "<>")
        (let (_ (get_next_char s))
             (ch2 (peek s))
               # note: side-effects in s prevent instruction re-ordering
            (if (eq ch2 "=")
                (let (_ (get_next_char s))
                    (symbol_at (+ ch ch2) (get_position s)))
                (symbol_at ch (get_position s)))))
    (true
        (raise
            (format
                "Unexpected character while reading symbol: \"{}\""
                ch)))))))

(define read_name_char
(lambda (s)
(cond
    ((not (has_chars s))
        '())
    ((in (peek s) "abcdefghijklmnopqrstuvwxyz_0123456789")
        (cons (get_next_char s) (read_name_char s)))
    (true '()))))

(define read_name
(lambda (s)
(if (not (in (peek s) "abcdefghijklmnopqrstuvwxyz_"))
    (raise
        (format
            "Unexpected character at the beginning of a name: \"{}\""
             (peek s)))
    (symbol_at (+ (read_name_char s)) (get_position s)))))

(define read_integer_literal_char
(lambda (s)
(cond
    ((not (has_chars s))
        '())
    ((in (peek s) "0123456789")
        (cons (get_next_char s) (read_integer_literal_char s)))
    (true '()))))

(define read_integer_literal
(lambda (s)
(if (not (in (peek s) "0123456789"))
    (raise
        (format
            "Unexpected character at the beginning of integer literal: \"{}\""
            (peek s)))
    (int_from_str (+ (read_integer_literal_char s)) (get_position s)))))
