import numpy as np
from utils.utils import get_safe_true_start

class RB:
    """Rb init and assign.

    Attributes:
        rb_avi: an int indicating the total number of available rb units. #TODO is this right?
        rb_size: an int indicating the size of one rb unit.
        bitmap: an int array, storing the assign status for each rb, i indicates rb assigned to User i (i > 0),
           inited to 0.
    """

    def __init__(self, rb_num, rb_size, embb_num):
        self.rb_avi = rb_num
        self.rb_size = rb_size
        self.bitmap = np.zeros(self.rb_avi, dtype=np.int64)
        self.border_bitmap_id = embb_num

    def find_all_avi_rb(self, rb_num_req):
        """Find all continous region of rb units.

        """

        rb_start = 0
        rb_valid_end = 0
        rb_start_list = []
        num_ass_list = []
        while(rb_start < len(self.bitmap)):
            rb_start = get_safe_true_start((self.bitmap[rb_valid_end:]<=self.border_bitmap_id) 
                                            & (self.bitmap[rb_valid_end:]>=0))
            if rb_start is None:
                return rb_start_list, num_ass_list
            else:
                rb_start = rb_start + rb_valid_end
            rb_valid_end = get_safe_true_start(self.bitmap[rb_start:] > self.border_bitmap_id)
            if rb_valid_end is None:
                rb_valid_end = len(self.bitmap)
            else:
                rb_valid_end = rb_valid_end + rb_start 
            current = rb_valid_end - rb_start
            
            if current >= rb_num_req:
                rb_start_list.append(rb_start)
                num_ass_list.append(current)

        return rb_start_list, num_ass_list



    


    