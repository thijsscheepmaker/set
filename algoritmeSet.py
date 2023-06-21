import random as rng

class SetGame:

    def is_set(deck):
        for i in range(3):
            if deck[0][i] == deck[1][i] == deck[2][i]:
                return print("yes")
            elif deck[0][i] != deck[1][i] != deck[2][i]:
                return print("yes")
            else: return print("no")
        return
    
    def all_sets(self):
        sets = []
        for i in range (12):
            for j in range(i,11):
                for k in range(3):
                    if deck[i][i] == deck[j][i] == deck[j+1][i]:
                        sets.append([i, j, j+1])
                    elif deck[0][i] != deck[1][i] != deck[2][i]:
                        sets.append([i, j, j+1])
                    else: pass
        return sets
    
deck = [["green", "diamond", "empty", 1], ["green", "oval", "shaded", 2], ["green", "squiggle", "shaded", 2]]

SetGame.is_set(deck)