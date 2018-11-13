"""
COMS W4701 Artificial Intelligence - Homework 0

In this assignment you will implement a few simple functions reviewing
basic Python operations and data structures.

@author: Yu Liu (yl3957)
"""


def manip_list(list1, list2):
    print(list1[-1])
    list1.pop()
    list2[1] = list1[0]
    print(list1 + list2)
    return [list1, list2]


def manip_tuple(obj1, obj2):
    tup = (obj1, obj2)
    tup[0] = 1


def manip_set(list1, list2, obj):
    set1 = set(list1)
    set2 = set(list2)
    set1.add(obj)
    print(obj in set2)
    print(set1.difference(set2).union(set2.difference(set1)))
    print(set1.union(set2))
    print(set1.intersection(set2))
    set1.remove(obj)


def manip_dict(tuple1, tuple2, obj):
    dic = dict(zip(tuple1, tuple2))
    print(dic[obj])
    dic.pop(obj)
    print(len(dic))
    dic[obj] = 0
    return dic.items()


if __name__ == "__main__":
    print(manip_list(["artificial", "intelligence", "rocks"], [4701, "is", "fun"]))

    try:
        manip_tuple("oh", "no")
    except TypeError:
        print("Can't modify a tuple!")

    manip_set(["sets", "have", "no", "duplicates"], ["sets", "operations", "are", "useful"], "yeah!")

    print(manip_dict(("list", "tuple", "set"), ("ordered, mutable", "ordered, immutable", "non-ordered, mutable"), "tuple"))

