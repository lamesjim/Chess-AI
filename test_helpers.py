def heuristic_gen(list):
    for num in list:
        yield num
    yield "Done generating"

def get_successors(value=None, n=3):
    successors = []
    for i in range(0, n):
        successors.append(value)
    return successors

if __name__ == "__main__":
    import unittest
    class Test_heuristic(unittest.TestCase):

        def test_heuristic(self):
            list_a = [1,2,3]
            x = heuristic_gen(list_a)
            self.assertEqual(next(x), 1)
            self.assertEqual(next(x), 2)
            self.assertEqual(next(x), 3)
            self.assertEqual(next(x), "Done generating")

    class Test_get_successors(unittest.TestCase):

        def test_get_successors(self):
            self.assertEqual(get_successors(), [None, None, None], "Should handle defaults")
            self.assertEqual(get_successors("Dai", 5), ["Dai", "Dai", "Dai", "Dai", "Dai"], "Should print Daix5")
            self.assertEqual(get_successors("James", 0), [], "Should print Jamesx0")

    unittest.main()
