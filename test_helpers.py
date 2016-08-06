def heuristicGen(list):
    for num in list:
        yield num
    yield "Done generating"

if __name__ == "__main__":
    import unittest
    class Test_heuristic(unittest.TestCase):

        def test_heuristic(self):
            list_a = [1,2,3]
            x = heuristicGen(list_a)
            self.assertEqual(next(x), 1)
            self.assertEqual(next(x), 2)
            self.assertEqual(next(x), 3)
            self.assertEqual(next(x), "Done generating")
    unittest.main()
