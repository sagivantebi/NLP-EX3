from collections import defaultdict
import random


class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)
        self._list_sentence = []

    def add_rule(self, lhs, rhs, weight):
        assert (isinstance(lhs, str))
        assert (isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w, l, r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l, r, w)
        return grammar

    def is_terminal(self, symbol):
        return symbol not in self._rules

    def get_list(self):
        return self._list_sentence

    def gen(self, symbol):
        if self.is_terminal(symbol):
            return symbol
        else:
            expansion = self.random_expansion(symbol)

            return " ".join(self.gen(s) for s in expansion)

    def random_sent(self):
        self._list_sentence = []
        return self.gen("ROOT")

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        # print(self._rules[symbol])
        for r, w in self._rules[symbol]:
            # print("sum= " + str(self._sums[symbol]) + "  | symbol=  " + str(symbol), end=" |")

            # print(" w: " + str(w), end=" | ")
            # print(" p: " + str(p))
            p = p - w
            if p < 0:
                self._list_sentence.append(r)
                return r

        return r


def run_1_3(pcfg):
    with open("grammar1.gen.txt", "w") as f:
        for i in range(10):
            f.write(str(pcfg.random_sent()) + "\n")


def run_2(pcfg):
    with open("Output/OMRI_grammar2.gen.txt", "w") as f:
        for i in range(20):
            f.write(str(pcfg.random_sent()) + "\n")


def build_tree_iterative(list_tree):
    to_return = ""
    stack = []
    depth_stack = 0
    current_depth_node = 0
    for tup in list_tree:
        if len(stack) != 0:
            # if we reached the value level
            current_depth_node = int(stack[-1][1])
            if current_depth_node == int(depth_stack):
                to_return += ("(" + stack.pop()[0])

        # if it's a leaf
        if len(tup) == 1:
            to_return += (" " + str(tup[0]) + ")")

            while stack[-1][0] == ")":
                to_return += (stack.pop()[0])
            depth_stack -= 1
        # if it's a leaf - "chief of staff"
        elif len(tup) == 3:
            to_return += (" " + "chief of staff" + ")")
            while stack[-1][0] == ")":
                to_return += (stack.pop()[0])
            depth_stack -= 1
        # if it has too choices
        else:
            stack.append((")", depth_stack))
            stack.append((tup[1], depth_stack))
            depth_stack += 1
            to_return += (" (" + tup[0] + " ")
    if len(stack) != 0:
        # if we reached the value level
        if stack[-1][1] == depth_stack:
            to_return += (stack.pop()[0])
    return to_return


def run_3_tree(pcfg):
    pcfg.random_sent()

    list_tree = pcfg.get_list()
    to_return = ""
    # print("\n")
    # print(list_tree)
    to_return += "(ROOT "
    to_return += build_tree_iterative(list_tree)
    to_return += ")"
    return to_return


def write_3(pcfg):
    with open("part3.gen.txt", "w") as f:
        for i in range(5):
            f.write(str(run_3_tree(pcfg)) + "\n")


if __name__ == '__main__':
    import sys

    pcfg = PCFG.from_file(sys.argv[1])
    if len(sys.argv) == 3:
        if sys.argv[3] == "-t":
            run_3_tree(pcfg)

    elif len(sys.argv) == 4:
        number_sentences = sys.argv[3]
        if (sys.argv[2] == "-n") and number_sentences.isnumeric():
            for i in range(int(number_sentences)):
                print(pcfg.random_sent())
    else:
        print(pcfg.random_sent())

    # run_1_3(pcfg)
    # run_2(pcfg)

    # print(run_3_tree(pcfg))
    write_3(pcfg)
