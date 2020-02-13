import math

def get_embb_utility(embb_users, e_trans=0):
    embb_utility = 0.0
    for i in embb_users:
        weighti = i.DRC
        if i.sche_times:
            embb_utility += weighti * math.log(i.rate_avg)
    return embb_utility
