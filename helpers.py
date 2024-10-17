import itertools

def split_dict_list(dictlist, splitter):
    """ Split a dictionary into a list of dictionaries based on the results of a given function. """
    # sort by key
    dictlist.sort(key=splitter)
    # split by key
    return [list(g) for k, g in itertools.groupby(dictlist, key=splitter)]
