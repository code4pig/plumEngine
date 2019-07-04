# coding=utf8

from __future__ import unicode_literals

from decimal import Decimal, ROUND_HALF_EVEN
import random


def round_to_int(val):
    return int(Decimal(str(val)).quantize(0, ROUND_HALF_EVEN))


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))))
    temp_list = []
    for k, v in named.iteritems():
        if v in enums:
            enums[k] = enums[v]
            temp_list.append(k)
        else:
            enums[k] = v
    reverse = dict((value, key) for key, value in enums.iteritems() if key not in temp_list)
    enums['reverse_mapping'] = reverse
    return type(str('Enum'), (), enums)


def get_random_seed():
    return random.randint(-2000000000, 2000000000)
