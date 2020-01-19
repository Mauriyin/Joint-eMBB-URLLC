def get_safe_true_start(bool_array):
    if bool_array.sum() == 0:
        return None
    return bool_array.argmax()
    