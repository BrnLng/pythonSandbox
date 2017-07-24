from pcolors import PColors
from pprint import pprint
from unittest.mock import patch
import unittest
from io import StringIO

DEBUG = True


class Comparisons:
    def __init__(self, *args):
        self.l_chaos = list(args)
        self.total_chaos = len(self.l_chaos)
        self.l_order = [self.l_chaos.pop()]
        self.t_comparisons = {}
        self.l_axis = ''
        self._current_index = -1
        self._current_direction_space = 0
        self._current_direction_first = True

    def __str__(self):
        print_string = "items organized/total: " + \
                       str(len(self.l_order)) + "/" + \
                       str(self.total_chaos) + "\n" + \
                       "actual org.list: " + self.l_order.__str__()
        return print_string

    def set_axis(self, axis):
        self.l_axis = " according to " + axis  # TODO: or axis+'-ness' like cute-ness

    def _update_markers(self, bool_direction_first=True):
        self._current_direction_first = bool_direction_first
        len_total = len(self.l_order)
        if self._current_direction_first:
            self._current_index = self._current_direction_space // 2
            self._current_direction_space = len_total - (len_total - self._current_index)
        else:
            self._current_index = len_total - 1 + self._current_direction_space // 2
            self._current_direction_space = len_total - self._current_index
        if DEBUG:
            self._print_locations(bool_direction_first)

    def step_compare(self):
        current_comparing_item = self.l_chaos[-1]
        while self._print_choose_options(current_comparing_item):
            try:
                current_comparing_item = self.l_chaos[-1]
                # if DEBUG:
                #     print(PColors.A_MAGENTA + "comparing item: " + current_comparing_item + PColors.CTR_RESET)
                print(self)
            except IndexError:
                # TODO: list completion, add options!
                print("complete comparison!")
                return

    def _print_choose_options(self, current_comparing_item):
        l_a_over_b = ["a", ",", "<", current_comparing_item.lower()]
        l_equals_special = ["="]
        l_exit_answers = ["q", "quit"]

        # if DEBUG:
        #     print(PColors.A_MAGENTA, "chaotic list and index: ",
        #           self.l_chaos, ' ', self._current_index, PColors.CTR_RESET)

        print("comparing: " + current_comparing_item +
              " <-?-> " + self.l_order[self._current_index])
        answer = str(input(PColors.A_BLUE + "¿what's greater" + self.l_axis + "? "
                           + PColors.CTR_RESET)).lower()
        if answer in l_a_over_b:
            self._do_update(current_comparing_item, True)
            return True
        elif answer in l_equals_special:
            return True  # TODO: optional equal
        elif answer in l_exit_answers:
            print("quitting...")  # TODO: +saving
            return False
        else:  # a NOT over b, ie. b > a
            self._do_update(current_comparing_item, False)
            return True

    def _do_update(self, current_comparing_item, bool_a_over_b):
        if bool_a_over_b:
            # s: string part; a: a or b item; o: offset needed
            s = " > "
            a = current_comparing_item
            o = 0
        else:
            s = " < "
            a = self.l_order[self._current_index]
            o = 1
        print(current_comparing_item + s + self.l_order[self._current_index])
        self.t_comparisons.update({frozenset([current_comparing_item,
                                              self.l_order[self._current_index]]): a})
        if self._current_direction_space <= 0:
            if DEBUG:
                print(PColors.A_TEAL, "inserting", current_comparing_item, end=' ')
            if self._current_index + 1 >= len(self.l_order) and not bool_a_over_b:
                if DEBUG:
                    print("after last item")
                self.l_order.append(current_comparing_item)
            else:
                if DEBUG:
                    item_now = self.l_order[self._current_index]
                    if bool_a_over_b:
                        print("before", item_now, end='')
                    else:
                        print("after", item_now, end='')
                    print(PColors.CTR_RESET)
                self.l_order.insert(self._current_index + o, current_comparing_item)
            self.l_chaos.remove(current_comparing_item)
        else:
            if DEBUG:
                print(PColors.LIGHT_TEAL, "no insertion now, recalculating markers", PColors.CTR_RESET)
        self._update_markers(bool_direction_first=bool_a_over_b)

    def _print_locations(self, bool_a_over_b):
        string_builder = ""
        if bool_a_over_b:
            string_builder = s = " < "
        else:
            s = " > "
        for c in range(len(self.l_order)):
            if not bool_a_over_b:
                string_builder += "." + self.l_order[c][0]
            if c == self._current_index:
                string_builder += s
            if bool_a_over_b:
                string_builder += "." + self.l_order[c][0]
        if not bool_a_over_b:
            string_builder += " >"
        string_builder += " + space: " + str(self._current_direction_space) + \
                          "\n\t\t\t index: " + str(self._current_index)
        print(PColors.LIGHT_MAGENTA, string_builder, PColors.CTR_RESET)
        # print(PColors.LIGHT_MAGENTA, "current direction space = ",
        #       self._current_direction_space, "\n",
        #       "current direction = ", s, "\n",
        #       "current index = ", self._current_index, "\n",
        #       "ordered list length = ", len(self.l_order), PColors.CTR_RESET)

    def show_current_results(self):
        self.print_comparisons_table()
        print(self)

    def print_comparisons_table(self):
        # TODO: proper table print : 1 2 3 | 4 3 2 triangulated
        pprint(self.t_comparisons)

    def __del__(self):
        print("needs to save?")  # TODO: last attempt to save


# class TestComparisons(unittest.TestCase):
#     test_comparisons = Comparisons("a", "B", "3", "four", "v", "ses")
#
#     def runTest(self, given_answer, expected_out):
#         with patch('builtins.input', return_value=given_answer), \
#              patch('sys.stdout', new=StringIO()) as fake_out:
#             while self.test_comparisons.step_compare():
#                 pass
#             self.assertEqual(fake_out.getvalue().strip(), expected_out)
#
#     def testSimple(self):
#         inputs = ['<', '<', '<', '<', '<']
#         outputs = ['a', 'B', '3', 'four', 'v', 'ses']
#         self.runTest(inputs, outputs)
#
#     # def testWeird(self):
#     #     inputs = ['<', '<', '<', '<', '<']
#     #     outputs = ['3', 'a', 'v', 'B', 'ses', 'four']
#     #     self.runTest(inputs, outputs)


if __name__ == '__main__':
    test_comparisons = Comparisons("a", "B", "3", "four", "v", "ses")
    # test_comparisons.set_axis('importance')
    while test_comparisons.step_compare():
        print(test_comparisons)
    test_comparisons.show_current_results()

    # unittest.main()
