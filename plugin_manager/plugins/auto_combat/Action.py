from enum import IntEnum


class Action(IntEnum):
    nothing = 0
    attack = 100
    kill = 101
    release = 102
    wield = 103
    get_weapon = 104
    retreat = 105