def get_safe_true_start(bool_array):
    if bool_array.sum() == 0:
        return None
    return bool_array.argmax()

def get_retrans_schedule(latency, error_rate, mcs_error):
    retrans = 1
    retrans_start = []
    for i in range(retrans):
        retrans_start.append(8)
    return retrans, retrans_start

    