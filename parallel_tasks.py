def gen_cdf_ranks(cdf_names,total_ranks):
    cdf_ranks = {}
    r = 0
    for cdf in cdf_names:
        cdf_ranks[cdf_names] = r
        r += 1

        if r>(total_ranks):
            r = 0

    return cdf_ranks 