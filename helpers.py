import itertools

def split_dict_list(dictlist, splitter, sortkey=None):
    """ Split a dictionary into a list of dictionaries based on the results of a given function. """
    # sort by key
    dictlist.sort(key=splitter)
    # split by key
    split = [list(g) for k, g in itertools.groupby(dictlist, key=splitter)]

    if sortkey:
        # sort each sublist by sortkey
        split = [sorted(sublist, key=sortkey) for sublist in split]

    return split
