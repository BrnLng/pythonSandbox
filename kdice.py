import random
from pprint import pprint

class Dices:
    """
    a master class for controlling and throwing multiple dice

    inputstr has to say stuff like
        2d4 + d6.fudge + y (TODO: additional fixed, yet to implement) etc
        ex.: d2  = Dice(2) #bean counter
             d4  = Dice(4) #tetrahedronal
             d6  = Dice(6) #the common one
             others: d8, d10, d12, d20 and the rare d24, d36, d100, d120
    """

    def __init__(self, inputstr):
        self._diceset = []
        self._inputhist = inputstr
        initializer = inputstr.split(sep='+')
        for part in initializer:
            self.initialize(part.strip().lower().split(sep='d', maxsplit=1))

    def __str__(self):
        return self._inputhist

    def initialize(self, inputparts):
        howmany, type = inputparts
        if '.' in type:
            type, modification = type.split(sep='.')
            self._diceset.append(Dice(int(type)).transform(option=modification).multi(int(howmany)))
        elif howmany == '':
            self._diceset.append(Dice(int(type)))
        else:
            self._diceset.append(Dice(int(type)).multi(int(howmany)))

        dicesetcopy = list(self._diceset)
        for dice in dicesetcopy: #using just _diceset would make it grow and loop in(de)finetely
            if dice.hasmultiple():
                for i in range(dice.howmany()):
                    self._diceset.append(dice)

    def run(self, times):
        result = {"total": 0}
        handtotal = {}

        for i in range(times):
            handresult = 0
            for dice in self._diceset:
                semiresult = dice.throw()
                handresult += semiresult
                currentresult = result.get(semiresult,0)
                currenttotal = result.get("total")
                result.update({semiresult: currentresult + 1, "total": currenttotal + semiresult})
            handcurrenttotal = handtotal.get(handresult,0)
            handtotal.update({handresult: handcurrenttotal + 1})

        pprint(result, width=4)
        print('-'*12)
        pprint(handtotal, width=4)
        # for k, v in sorted(result.items()):
        #     print('{}: {}'.format(k, v))


class Dice:
    """a dice representation with some transformations and twists
        gets preferably a list with a range of face values

        Values for self transformation after basic range input are:
        Fudge: basic default + calm, calmer, extremist, extremest, good and doog
    """

    def __init__(self, facelist_max, many=1, init=1):
        if isinstance(facelist_max, list):
            self.facelist = facelist_max
        else:
            self.facelist = list(range(init, facelist_max + init))
        self._many = many

    #@property
    def throw(self):
        if self._many == 1 or __name__ == "__main__":
            return random.choice(self.facelist)
        else:
            results = {}
            for i in range(self._many):
                result.update({i: random.choice(self.facelist)})
            return results

    def transform(self, option='fudge'):
        """option(s) available: fudge (default), or fudgy...
        calm, calmer, extremist, extremest, good and doog
        from d6 base:
            basxDice = Dice([-3, -2, -1, 1, 2, 3]) #basic fudge twist =1-6, with filter on 4+ to *-1
            diceA =    Dice([-2, -1, -1, 1, 1, 2]) #basicist todoist = basx with someFilter
            diceB =    Dice([-1, -1,  0, 0, 1, 1]) #neutralist
            diceC =    Dice([-3,  0,  0, 0, 0, 3]) #extremist = A with noiseFilter
            goodDice = Dice([-1,  0,  0, 1, 2, 3])
            doogDice = Dice([-3, -2, -1, 0, 0, 1])
            weirDice = Dice([-3, -3, -3, 3, 3, 3])
        """
        base = len(self.facelist) // 2
        minf = min(self.facelist)
        maxf = max(self.facelist)
        ceiling = maxf + 1
        for face in self.facelist:
            if option == 'calm':
                if face <= base:
                    if face > 1:
                        self.facelist[face-1] = face - 1
                    else:
                        continue
                else:
                    if face < maxf:
                        self.facelist[face-1] = face - maxf
                    else:
                        self.facelist[face-1] = face - ceiling
            elif option == 'calmer':
                if face < base:
                    self.facelist[face-1] = 1
                elif base <= face <= (base + 1):
                    self.facelist[face-1] = 0
                else:
                    self.facelist[face-1] = -1
            elif option == 'extremist':
                if face == minf:
                    self.facelist[face-1] = base
                elif face == maxf:
                    self.facelist[face-1] = -base
                else:
                    self.facelist[face-1] = 0
            elif option == 'extremest':
                if face <= base:
                    self.facelist[face-1] = base
                else:
                    self.facelist[face-1] = -base
            elif option == 'good':
                if face <= base:
                    continue
                else:
                    self.facelist[face-1] = min(0, face - (maxf - 1))
            elif option == 'doog':
                if face == minf:
                    continue
                elif face <= base:
                    self.facelist[face-1] = 0
                else:
                    self.facelist[face-1] = face - ceiling
            else: # option == 'fudge' (default)
                if face <= base:
                    continue
                else:
                    self.facelist[face-1] = face - ceiling # (face * -1) + base # face - max(self.facelist) # seemingly nicer, but cumbersome as calls one more function
        print(self.facelist)
        return self

    def multi(self, howmany):
        self._many = howmany
        return self

    def hasmultiple(self):
        if self._many == 1:
            return False
        return True

    def howmany(self):
        return self._many - 1


# 1-6 = sat+c sat-c dc d dk k -- each dice is a filtred theme read
# basic dice = w wd d dc kc c ~= 1-6 /= 1,2,3 (normal) + 4/-3, 5/-2, 6/-1

if __name__ == "__main__":

    diceset = Dices("d6 + 2d4.fudge")

    diceset.run(10)
    print(diceset)

    import cardsdeck
    dk = cardsdeck.Blackjack()