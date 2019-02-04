from unittest import TestCase


# noinspection PyUnreachableCode
class TryPyTest(TestCase):
    def test_py_exception_handling_permutation_aaaa(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            else:
                els = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_aaar(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            else:
                els = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_aaae(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            else:
                els = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_aara(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            else:
                return "els"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("els", result)

    def test_py_exception_handling_permutation_aarr(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            else:
                return "els"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_aare(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            else:
                return "els"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_aaea(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            else:
                raise Exception("els")
            finally:
                fin = 1
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("els", str(cm.exception))

    def test_py_exception_handling_permutation_aaer(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            else:
                raise Exception("els")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_aaee(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            else:
                raise Exception("els")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_araa(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            else:
                els = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_arar(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            else:
                els = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_arae(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            else:
                els = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_arra(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            else:
                return "els"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("els", result)

    def test_py_exception_handling_permutation_arrr(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            else:
                return "els"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_arre(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            else:
                return "els"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_area(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            else:
                raise Exception("els")
            finally:
                fin = 1
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("els", str(cm.exception))

    def test_py_exception_handling_permutation_arer(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            else:
                raise Exception("els")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_aree(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            else:
                raise Exception("els")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_aeaa(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            else:
                els = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_aear(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            else:
                els = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_aeae(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            else:
                els = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_aera(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            else:
                return "els"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("els", result)

    def test_py_exception_handling_permutation_aerr(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            else:
                return "els"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_aere(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            else:
                return "els"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_aeea(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            else:
                raise Exception("els")
            finally:
                fin = 1
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("els", str(cm.exception))

    def test_py_exception_handling_permutation_aeer(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            else:
                raise Exception("els")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_aeee(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            else:
                raise Exception("els")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_raaa(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            else:
                els = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_raar(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            else:
                els = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_raae(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            else:
                els = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_rara(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            else:
                return "els"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_rarr(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            else:
                return "els"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_rare(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            else:
                return "els"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_raea(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            else:
                raise Exception("els")
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_raer(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            else:
                raise Exception("els")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_raee(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            else:
                raise Exception("els")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_rraa(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            else:
                els = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_rrar(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            else:
                els = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_rrae(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            else:
                els = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_rrra(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            else:
                return "els"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_rrrr(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            else:
                return "els"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_rrre(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            else:
                return "els"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_rrea(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            else:
                raise Exception("els")
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_rrer(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            else:
                raise Exception("els")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_rree(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            else:
                raise Exception("els")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_reaa(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            else:
                els = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_rear(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            else:
                els = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_reae(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            else:
                els = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_rera(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            else:
                return "els"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_rerr(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            else:
                return "els"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_rere(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            else:
                return "els"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_reea(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            else:
                raise Exception("els")
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_reer(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            else:
                raise Exception("els")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_reee(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            else:
                raise Exception("els")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_eaaa(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            else:
                els = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_eaar(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            else:
                els = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_eaae(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            else:
                els = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_eara(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            else:
                return "els"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_earr(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            else:
                return "els"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_eare(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            else:
                return "els"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_eaea(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            else:
                raise Exception("els")
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_eaer(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            else:
                raise Exception("els")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_eaee(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            else:
                raise Exception("els")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_eraa(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            else:
                els = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("exc", result)

    def test_py_exception_handling_permutation_erar(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            else:
                els = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_erae(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            else:
                els = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_erra(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            else:
                return "els"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("exc", result)

    def test_py_exception_handling_permutation_errr(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            else:
                return "els"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_erre(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            else:
                return "els"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_erea(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            else:
                raise Exception("els")
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("exc", result)

    def test_py_exception_handling_permutation_erer(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            else:
                raise Exception("els")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_eree(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            else:
                raise Exception("els")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_eeaa(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            else:
                els = 1
            finally:
                fin = 1
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("exc", str(cm.exception))

    def test_py_exception_handling_permutation_eear(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            else:
                els = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_eeae(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            else:
                els = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_eera(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            else:
                return "els"
            finally:
                fin = 1
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("exc", str(cm.exception))

    def test_py_exception_handling_permutation_eerr(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            else:
                return "els"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_eere(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            else:
                return "els"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_eeea(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            else:
                raise Exception("els")
            finally:
                fin = 1
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("exc", str(cm.exception))

    def test_py_exception_handling_permutation_eeer(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            else:
                raise Exception("els")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_eeee(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            else:
                raise Exception("els")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_aaa(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_aar(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_aae(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_ara(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_arr(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_are(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_aea(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_aer(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_aee(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_raa(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_rar(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_rae(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_rra(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_rrr(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_rre(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_rea(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_rer(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_ree(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_eaa(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_ear(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_eae(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_era(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("exc", result)

    def test_py_exception_handling_permutation_err(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_ere(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_eea(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            finally:
                fin = 1
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("exc", str(cm.exception))

    def test_py_exception_handling_permutation_eer(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_eee(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_exc_aa(self):
        # given
        def x():
            try:
                code = 1
            except:
                exc = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_exc_ar(self):
        # given
        def x():
            try:
                code = 1
            except:
                return "exc"
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_exc_ae(self):
        # given
        def x():
            try:
                code = 1
            except:
                raise Exception("exc")
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_exc_ra(self):
        # given
        def x():
            try:
                return "code"
            except:
                exc = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_exc_rr(self):
        # given
        def x():
            try:
                return "code"
            except:
                return "exc"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_exc_re(self):
        # given
        def x():
            try:
                return "code"
            except:
                raise Exception("exc")
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_exc_ea(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                exc = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_exc_er(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                return "exc"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("exc", result)

    def test_py_exception_handling_permutation_exc_ee(self):
        # given
        def x():
            try:
                raise Exception("code")
            except:
                raise Exception("exc")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("exc", str(cm.exception))

    def test_py_exception_handling_permutation_fin_aa(self):
        # given
        def x():
            try:
                code = 1
            finally:
                fin = 2
            return 0

        # when
        result = x()
        # then
        self.assertEqual(0, result)

    def test_py_exception_handling_permutation_fin_ar(self):
        # given
        def x():
            try:
                code = 1
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_fin_ae(self):
        # given
        def x():
            try:
                code = 1
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_fin_ra(self):
        # given
        def x():
            try:
                return "code"
            finally:
                fin = 1
            return 0

        # when
        result = x()
        # then
        self.assertEqual("code", result)

    def test_py_exception_handling_permutation_fin_rr(self):
        # given
        def x():
            try:
                return "code"
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_fin_re(self):
        # given
        def x():
            try:
                return "code"
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))

    def test_py_exception_handling_permutation_fin_ea(self):
        # given
        def x():
            try:
                raise Exception("code")
            finally:
                fin = 1
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("code", str(cm.exception))

    def test_py_exception_handling_permutation_fin_er(self):
        # given
        def x():
            try:
                raise Exception("code")
            finally:
                return "fin"
            return 0

        # when
        result = x()
        # then
        self.assertEqual("fin", result)

    def test_py_exception_handling_permutation_fin_ee(self):
        # given
        def x():
            try:
                raise Exception("code")
            finally:
                raise Exception("fin")
            return 0

        # when
        with self.assertRaises(Exception) as cm:
            x()
        # then
        self.assertEqual("fin", str(cm.exception))
