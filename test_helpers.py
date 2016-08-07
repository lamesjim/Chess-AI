from node import Node

def heuristic_gen(list):
    for num in list:
        yield num
    yield "Done generating"

def get_successors(n=3):
    successors = []
    for i in range(0, n):
        successors.append(Node())
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
            node_check = all(isinstance(successor, Node) for successor in get_successors(5))
            self.assertEqual(len(get_successors()), 3, "Should handle defaults")
            self.assertEqual(len(get_successors(0)), 0, "Should return 0")
            self.assertEqual(node_check, True, "Should print a list of 5 nodes")

    unittest.main()
