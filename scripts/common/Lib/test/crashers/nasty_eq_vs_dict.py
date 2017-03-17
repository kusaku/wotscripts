# Embedded file name: scripts/common/Lib/test/crashers/nasty_eq_vs_dict.py


class Yuck:

    def __init__(self):
        self.i = 0

    def make_dangerous(self):
        self.i = 1

    def __hash__(self):
        return 12

    def __eq__(self, other):
        if self.i == 0:
            pass
        elif self.i == 1:
            self.__fill_dict(6)
            self.i = 2
        else:
            self.__fill_dict(4)
            self.i = 1
        return 1

    def __fill_dict(self, n):
        self.i = 0
        dict.clear()
        for i in range(n):
            dict[i] = i

        dict[self] = 'OK!'


y = Yuck()
dict = {y: 'OK!'}
z = Yuck()
y.make_dangerous()
print dict[z]