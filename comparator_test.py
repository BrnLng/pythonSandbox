import comparator
import unittest


class TestComparator(unittest.TestCase):
    comparator = comparator.Comparator()

    # def __init__(self):
    #     super().__init__()

    def test_put_an_item_first_against_initial(self):
        """put in order shall return a as first list item"""
        self.comparator._reset_put_initial('initial')
        self.comparator._put_in_order('a', 0)
        self.assertEqual(self.comparator.list_ordered, ['a', 'initial'])

    def test_put_first_item(self):
        """put first item"""
        self.comparator._reset_put_initial('initial')
        self.assertEqual(self.comparator.list_ordered, ['initial'])

    def test_ordered_output(self):
        """ordered list output should return simple ordered list"""
        self.comparator._reset_put_initial('initial')
        self.assertEqual(self.comparator.ordered(), ['initial'])

    def test_ordered_output_initially_empty(self):
        """ordered list output should return some error if empty"""
        self.comparator.list_ordered.clear()
        self.assertRaises(comparator.ComparatorErrorEmptyOrderedList, self.comparator.ordered)

    def test_add_new_items(self):
        """if new items to chaotic list are ok"""
        self.comparator.add_new_items(['a', 'b', 'c'])
        self.assertTrue(self.comparator.list_chaotic == {'a', 'b', 'c'})

    def test_add_new_items_with_duplicates(self):
        """if new items to chaotic list are ok with duplicates simply discarded"""
        self.comparator.add_new_items(['a', 'b', 'c', 'b'])
        self.assertTrue(self.comparator.list_chaotic == {'a', 'b', 'c'})


# if __name__ == '__main__':
#     unittest.main()
