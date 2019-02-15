(import cover_example do_something)

(def test_greater_than_three_returns_yes ()
    (assert (eq "yes" (do_something 4))))
