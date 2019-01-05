(define w_eval
(lambda (expr scope)
    (cond
    ((isinstance expr 'Symbol)
        (get scope expr))
    ((isinstance expr '(Number String Boolean))
        expr)
    ((isinstance expr 'List)
        (let (head (car expr))
        (if
            (eq head 'quote)
            (car (cdr expr))
            (let (callee w_eval(head scope))
            (let (args (cdr expr))
            (cond
            ((isinstance callee 'Macro)
                (let (exprs_scope (call_macro callee args scope))
                (let (exprs (car exprs_scope))
                (let (scope (car (cdr exprs_scope)))
                (w_eval exprs scope)))))
            ((not (isinstance callee 'Function))
                (raise
                    (format
                        "Callee is not a function. Got \"{}\" ({}) instead."
                        callee
                        (type callee))))
            (true
                (let (evaled_args
                    (map
                        (lambda (name value)
                            (list name (w_eval value scope)))
                        args (get_func_args callee)))
                (let (scope (new_scope_proto (get_func_enclosing_scope callee) evaled_args))
                (if
                    (isinstance callee 'MagicFunction)
                    implementation_specific
                    (w_eval (get_func_expr callee) scope)))))))))))
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


(define read_expr
(lambda (s)
(let (whitespace (read_whitespace_and_comments s))
     (ch (peek s))
    (cond
        ((not (has_chars s))
            (raise "Ran out of characters before reading expression."))
        ((eq ch "(") (read_list s))
        ((in ch "0123456789") (read_integer_literal s))
        ((or (in ch "+-*/<>_") (in ch "abcdefghijklmnopqrstuvwxyz")) (read_symbol s))
        ((eq ch "\"") (read_string s))
        ((eq ch "'")
            (exec
                (get_next_char s)
                (list 'quote (read_expr s))))
        (true
            (raise
                (format
                    "Unknown starting character \"{}\" in read_expr"
                    ch)))))))

(define read_list_element
(lambda (s)
(let (whitespace (read_whitespace_and_comments s))
    (if (not (has_chars s))
        (raise "Ran out of characters while reading the list.")
        (let (ch (peek s))
            (if (eq ch ")")
                (let (_ (get_next_char s))
                    '())
                (cons (read_expr s) (read_list_element s))))))))

(define read_list
(lambda (s)
(let (whitespace (read_whitespace_and_comments s))
    (if (not (has_chars s))
        (raise "Ran out of characters before starting the list.")
        (let (ch (get_next_char s))
            (if (not (eq ch "("))
                (raise (format "Unknown starting character \"{}\" in read_list" ch))
                (read_list_element s)))))))

(define read_comment_char
(lambda (s)
(cond
    ((not (has_chars s))
        '())
    ((eq (peek s) "\n")
        (cons (get_next_char s) (read_wsc_char s)))
    (true
        (cons (get_next_char s) (read_comment_char s))))))

(define read_comment
(lambda (s)
(if (not (eq (peek s) "#"))
    (raise
        (format
            "Unknown starting character \"{}\" in read_comment" (peek s)))
    (read_comment_char s))))

(define read_wsc_char
(lambda (s)
(cond
    ((not (has_chars s))
        '())
    ((eq (peek s) "#")
        (read_comment s))
    ((in (peek s) " \r\n\t")
        (cons (get_next_char s) (read_wsc_char s)))
    (true
        '()))))

(define read_whitespace_and_comments
(lambda (s)
(if (not (in (peek s) " \r\n\t#"))
    ""
    (+ (read_wsc_char s)))))
