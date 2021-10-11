def create_candidate(df):
    # Capturing single cancidate in transaction
    # fronzenset function is used to write all possible results.
    can = []
    for transaction in df:
        for t in transaction:
            t = frozenset([t])
            if t not in can:
                can.append(t)
    return can


def create_candidates(freq_item, k):
    can2 = []

    # Generate 2-size candidates.
    if k == 0:
        for a1, a2 in combinations(freq_item, 2):
            item = a1 | a2
            can2.append(item)
    else:
        for a1, a2 in combinations(freq_item, 2):
            # Uniting candidates with k+1 items.
            intersection = a1 & a2
            if len(intersection) == k:
                item = a1 | a2
                if item not in can2:
                    can2.append(item)
    return can2


def create_freq_item(df, ck, min_support):
    # loop through the transaction and item count.
    item_count = {}
    for transaction in df:
        for item in ck:
            if item.issubset(transaction):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1

    n_row = df.shape[0]
    freq_item = []
    item_support = {}
    # filter by min support
    for item in item_count:
        support = item_count[item] / n_row
        if support >= min_support:
            freq_item.append(item)
        item_support[item] = support

    return freq_item, item_support


def apriori_1(df, min_support):
    # the candidate sets for the 1-item is created by createe_candidate function.
    c1 = create_candidate(df)
    freq_item, item_support_dict = create_freq_item(df, c1, min_support)
    freq_items = [freq_item]

    k = 0
    while len(freq_items[k]) > 0:
        freq_item = freq_items[k]
        ck = create_candidates(freq_item, k)
        freq_item, item_support = create_freq_item(df, ck, min_support)
        freq_items.append(freq_item)
        item_support_dict.update(item_support)
        k += 1

    return freq_items, item_support_dict


freq_items, item_support_dict = apriori_1(dataset, min_support = 0.1)
sorted_dict = dict( sorted(item_support_dict.items(),
                           key=lambda item: item[1],
                           reverse=True))