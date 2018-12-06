import string
from itertools import chain
import re
from operator import itemgetter

lower_upper = (
    ''.join(c) for c in zip(string.ascii_lowercase, string.ascii_uppercase)
)
upper_lower = (
    ''.join(c) for c in zip(string.ascii_uppercase, string.ascii_lowercase)
)
opposites = chain(upper_lower, lower_upper)

pattern = re.compile("|".join(opposites))


def reaction(polymer: str) -> str:
    """
    Chain reaction annihilates opposite units.

    >>> reaction("Aa")
    ''
    >>> reaction("abBA")
    ''
    >>> reaction("abAB")
    'abAB'
    >>> reaction("aabAAB")
    'aabAAB'
    >>> reaction("dabAcCaCBAcCcaDA")
    'dabCBAcaDA'
    """
    old_polymer = polymer
    while True:
        polymer = re.sub(pattern, "", polymer)

        if polymer == old_polymer:
            return polymer

        old_polymer = polymer


with open("./input_d05.txt") as handle:
    polymer = handle.read()

# remove the EOL
polymer = polymer[:-1]

print(len(polymer))
reduced_polymer = reaction(polymer)
print(len(reduced_polymer))


# part 2
# recharge the generator
lower_upper = (
    ''.join(c) for c in zip(string.ascii_lowercase, string.ascii_uppercase)
)

# store the values inside
res = {}
for op in lower_upper:
    op_patt = re.compile(f"[{op}]")
    mod_polymer = re.sub(op_patt, "", polymer)
    res[op] = len(reaction(mod_polymer))

print(min(list(res.items()), key=itemgetter(1)))
