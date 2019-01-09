# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 18:21:25 2019

@author: Ashlin
"""

from random import Random

chutes_ladders={1:38, 4:14, 9:31, 16:6, 21:42, 28:84, 36:44,
                  47:26, 49:11, 51:67, 56:53, 62:19, 64:60,
                  71:91, 80:100, 87:24, 93:73, 95:75, 98:78}

def simulate_game(seed=None,maximum_rolls=6):
    random=Random(seed)
    position=0
    turns=0
    while position<100:
        turns+=1
        dice_roll=random.randint(1,maximum_rolls)
        if position+dice_roll >100:
            continue
        if position+dice_roll<100:
            position+=dice_roll
            position=chutes_ladders.get(position,position)
            # if position has no value in the dictionary just return current value of position
    return turns

simulate_game()
