from pcolors import PColors
# from math import ceil, floor
# from pprint import pprint


class ComparatorError(Exception):
    pass


class ComparatorErrorEmptyOrderedList(ComparatorError):
    pass


class Comparator:
    list_ordered = []
    list_chaotic = set()
    total_chaotic_entries = 0
    bool_done = False

    l_a_over_b = ["a", ",", "<"]
    l_equals_special = ["="]
    l_exit_answers = ["q", "-"]

    wall_left = 0
    wall_right = -1
    current_comparing_index = -1
    current_new_item = None

    def _step_compare(self):
        if self.bool_done:
            return False

        try:
            current_comparing_item = self.list_ordered[self.current_comparing_index]
        except IndexError:
            current_comparing_item = self.list_ordered[-1]

        print(self.print_list('first_part') + " < " + PColors.LIGHT_RED +
              self.current_new_item + PColors.CTR_RESET + " x " +
              current_comparing_item + " > " + self.print_list('last_part', ''), end=':\n')

        answer = str(input(PColors.LIGHT_RED + self.current_new_item + " ¿ < // > " +
                           PColors.CTR_RESET + current_comparing_item + " ? ")).lower()

        if answer[0] in self.l_a_over_b:
            if self._check_is_last_or_indexes_update(True):
                self._put_in_order(self.current_new_item, self.current_comparing_index)
                self._indexes_update()
            else:
                self._step_compare()
            return True
        elif answer[0] in self.l_equals_special:
            print("equals still not available...")  # TODO: optional equal
            return True
        elif answer[0] in self.l_exit_answers:
            print("quitting...")  # TODO: +saving
            return False
        else:  # a NOT over b, ie. b > a
            if self._check_is_last_or_indexes_update(False):
                if self.current_comparing_index >= len(self.list_ordered):
                    self.list_ordered.append(self.current_new_item)
                else:
                    self._put_in_order(self.current_new_item, self.current_comparing_index + 1)
                self._indexes_update()
            else:
                self._step_compare()
            return True

    def _check_is_last_or_indexes_update(self, direction_to_first=True):
        """bizarre : works but was done on intuition, don't know how to test
        """
        if direction_to_first:
            space_to_move = self.current_comparing_index - self.wall_left
            if space_to_move < 1:
                return True
            self.wall_right = self.current_comparing_index
        else:  # going to last direction
            space_to_move = self.wall_right - self.current_comparing_index
            if space_to_move <= 1:
                return True
            self.wall_left = self.current_comparing_index + 1
        self.current_comparing_index = (self.wall_left + self.wall_right) // 2
        return False

        # """tried BUT FAILED to do as follows -- ordered list to be seen as if it was:
        #  0 1 2 3 4 5 6 (example)
        # >| i   i   i |< [3 items: 0, 1 and 2 at positions 1, 3 and 5 respectively (i+0.5)*2
        #             >| = wall_left (would be 0/-1*notLast), |< = wall_right (6/3); 0-6 equals spaces available
        # at any point in time current_comparing_object should be at same spot as any i
        # at end all as normal
        # """
        # wall_left = self.wall_left * 2
        # wall_right = self.wall_right * 2
        # index = round((self.current_comparing_index + 0.5) * 2)
        # if direction_to_first:
        #     space_to_move = index - wall_left
        #     if space_to_move <= 2:
        #         return True
        #     self.wall_right = floor(index / 2)
        # else:  # going to last direction
        #     space_to_move = wall_right - index
        #     if space_to_move <= 2:
        #         return True
        #     self.wall_left = ceil(index / 2)
        # self.current_comparing_index = round((wall_left + wall_right) / 2)
        # return False

    def _indexes_update(self):
        try:
            self.current_new_item = self.list_chaotic.pop()  # this may raise exception

            ordered_length = len(self.list_ordered)
            self.current_comparing_index = ordered_length // 2
            self.wall_left = 0
            self.wall_right = ordered_length + 1
        except KeyError:
            self.bool_done = True

    def __init__(self, *args):
        if args:
            self.add_new_items(list(args))
        else:
            pass

    def add_new_items(self, new_items):
        for item in new_items:
            self.list_chaotic.add(item)
            self.total_chaotic_entries += 1
            if self.bool_done:
                self.bool_done = False

    def ordered(self):
        if not self.list_ordered:
            raise ComparatorErrorEmptyOrderedList("empty list @ ordered")
        return self.list_ordered

    def _reset_put_initial(self, item):
        if self.list_ordered:
            self.list_ordered.clear()
            if self.bool_done:
                self.bool_done = False
        self.list_ordered.append(item)

    def _put_in_order(self, item, order_index):
        self.list_ordered.insert(order_index, item)

    def __str__(self):
        return self.print_current_status()

    def print_current_status(self):
        if self.bool_done:
            return "100%!\n" + self.print_list('ordered')
        else:
            n_ordered = len(self.list_ordered)
            percent_done = float(n_ordered / self.total_chaotic_entries) * 100
            reading = "\t" + str(n_ordered) + " / " + str(self.total_chaotic_entries) + \
                      " ({:.1f}%)\nItems to compare: ".format(percent_done) + \
                      "\n" + self.print_list() + "\nItems in order: " + \
                      "\n" + self.print_list('ordered')
            return reading

    def print_list(self, inner_list='chaotic', init="\t"):
        # print("list + arg = " + inner_list)
        string_max_length = 25  # 80 for normal
        string_len = 0
        string = init
        for item in (self.list_chaotic if inner_list == 'chaotic'
                     else self.list_ordered[self.wall_left:self.current_comparing_index]
                     if inner_list == 'first_part'
                     else self.list_ordered[self.current_comparing_index+1:self.wall_right]
                     if inner_list == 'last_part'
                     else self.list_ordered):
            string_more = item + ", "
            string_len += len(string_more)
            string += string_more
            if string_len > string_max_length:
                string += "\n\t"
                string_len = 0
        return string.strip(', ')

    def step(self):
        if not self.list_ordered:
            self._step_compare_n_new_with_m_ordered(
                4 if self.total_chaotic_entries > 3 else 2, 0)  # min nums TODO: optionize
        else:
            self._indexes_update()
            self._step_compare()
            # self._step_compare_n_new_with_m_ordered(
            #     2 if self.total_chaotic_entries > 1 else 1, 2)

    def steps_until_quit(self):
        if not self.list_ordered:
            self._step_compare_n_new_with_m_ordered(
                4 if self.total_chaotic_entries > 3 else 2, 0)  # min nums TODO: optionize

            self._indexes_update()
        while self._step_compare():
            if self.bool_done:
                return

    def _step_compare_n_new_with_m_ordered(self, num_of_same_time_compared_items,
                                           num_of_items_already_ordered):
        """main concept here is try and ensure no wrong move made
        re:list_ordered initially"""
        if num_of_items_already_ordered == 0 and not self.list_ordered:
            ordered = self._initial_n(num_of_same_time_compared_items)
            self.list_ordered = ordered
        else:
            pass
            # self._rank_n_in_o(num_of_same_time_compared_items,
            #                   num_of_items_already_ordered)

    def _initial_n(self, num_of_same_time_compared_items):
        mini_chaotic_list = list()
        for _ in range(num_of_same_time_compared_items):
            mini_chaotic_list.append(self.list_chaotic.pop())
        rank_order_list = dict()  # .fromkeys(mini_chaotic_list)
        print("define order for: ", end="\n\t")
        for item in mini_chaotic_list:
            print(item, end=', ')
        print("\b\b")
        for item in mini_chaotic_list:
            rank_order_list.update({input("enter rank order for " + item + ": "): item})

        final_list = []
        for sorted_order_key in sorted(rank_order_list):
            final_list.append(rank_order_list[sorted_order_key])
        return final_list


if __name__ == '__main__':
    # items = ['a', 'B', '3', 'four', 'v', 'ses']
    comparator = Comparator('a', 'B', '3', 'four', 'v', 'ses')

    # comparator.add_new_items(items)

    comparator.steps_until_quit()
    print(comparator)
