from libs.models.naive_solver import NaiveURLLCSolver
from from utils.metrics import get_embb_utility

class GreedyURLLCSolver(NaiveURLLCSolver):
    """Scheduler for URLLC users with greedy algorithm.
       Assign for the URLLC users within the arriving order, calculate the embb utility for 
       each possible assignment plan and choose the optimal one for the current urllc user.
    
    """

    def __init__(self, RB_map, embb_users, urllc_users):
        NaiveURLLCSolver.__init__(self, RB_map, embb_users, urllc_users)
    
    def _solver(self, rb_start_list, num_ass_list):
        """Greedy solver.
           Calculate the embb utility for each possible assignment plan and choose the optimal one.

        """
        rb_start_final = rb_start_list[-1]
        rb_num_ass_final = num_ass_list[-1]
        max_utility = 0

        for i in range(len(rb_start_list)):
            embb_user_list = self.embb_users.copy()
            rb_start = rb_start_list[i]
            rb_num_ass = num_ass_list[i]
            for k in range(rb_num_ass):
                if self.RB_map.bitmap[rb_start+k] > 0:
                    embb_user = embb_user_list[self.RB_map.bitmap[rb_start+k]-1]
                    if embb_user.active == 0:
                        print ("ERROR: Inactive embb user is not clear!")
                    else:
                        embb_user.rate_avg = (embb_user.rate_avg * embb_user.sche_times - 1) / embb_user.sche_times

            if get_embb_utility(embb_user_list) >= max_utility:
                rb_start_final = rb_start
                rb_num_ass_final = rb_num_ass
                max_utility = get_embb_utility(embb_user_list)

        return rb_start_final, rb_num_ass_final