from collections import defaultdict
from operator import itemgetter

def prune_multi(input, t_r_min = 1, n_max = 0):
    """
    prune bottom and top of list of tokenized strings
    - t_r_min: minimum term frequency
    - n_max: n most frequent words to remove
    """
    t_f_total = defaultdict(int)
    for text in input:
        for token in text:
            t_f_total[token] += 1
    nmax = sorted( t_f_total.iteritems(), key = itemgetter(1), reverse = True)[:n_max]
    stoplist = [elem[0] for elem in nmax]
    output_ls = []
    for text in input:
        output = [token for token in text if t_f_total[token] >= t_r_min and token not in stoplist]
        output_ls.append(output)
    return output_ls
