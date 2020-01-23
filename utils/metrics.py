import math

def get_embb_utility(embb_users, e_trans=0):
    embb_utility = 0.0
    for i in embb_users:
        weighti = i.DRC / (0.01 * i.DRC + 0.99 * i.rate_avg)
        if i.sche_times:
            embb_utility += weighti * math.log((i.rate_avg * i.sche_times - e_trans) / i.sche_times)
    return embb_utility
