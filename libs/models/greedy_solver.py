from libs.models.naive_solver import NaiveURLLCSolver
from utils.metrics import get_embb_utility
from copy import deepcopy


class GreedyURLLCSolver(NaiveURLLCSolver):
    """Scheduler for URLLC users with greedy algorithm.
       Assign for the URLLC users within the arriving order, 
       calculate the embb utility for each possible assignment plan 
       and choose the optimal one for the current urllc user.
    
    """
    def __init__(self, RB_map, embb_users, urllc_users):
        NaiveURLLCSolver.__init__(self, RB_map, embb_users, urllc_users)

    def _solver(self, rb_start_list, num_ass_list, num_req):
        """Greedy solver.
           Calculate the embb utility for each possible assignment plan 
           and choose the optimal one.

        """
        rb_start_final = rb_start_list[-1]
        rb_num_ass_final = num_ass_list[-1]
        max_utility = 0

        for i in range(len(rb_start_list)):
            rb_start = rb_start_list[i]
            rb_num_avi = num_ass_list[i]
            for k in range(rb_num_avi - num_req):
                embb_user_lists = deepcopy(self.embb_users)
                #Calculate the replace block on current setting
                for j in range(num_req):
                    if self.RB_map.bitmap[rb_start + j] > 0:
                        embb_user = embb_user_lists[
                            self.RB_map.bitmap[rb_start + j] - 1]
                        if embb_user.active == 0 or int(
                                embb_user.user_info['id']
                        ) != self.RB_map.bitmap[rb_start + j]:
                            print("ERROR: embb user mismatched!")
                        else:
                            embb_user.replace_num += 1
                #update throughput
                for embb_user in embb_user_lists:
                    #print("The list:")
                    #print(embb_user.__dict__.items())
                    if embb_user.sche_times > 1:
                        embb_user.rate_avg = (
                            embb_user.rate_avg * (embb_user.sche_times) -
                            embb_user.rate_cur) / (embb_user.sche_times - 1)
                    embb_user.rate_cur = (embb_user.rate_cur * (
                        (embb_user.rb_num_ass) * 7 - embb_user.replace_num)
                                          ) / ((embb_user.rb_num_ass) * 7)
                    #print(embb_user.rate_cur)
                    embb_user.rate_avg = (
                        embb_user.rate_avg * (embb_user.sche_times - 1) +
                        embb_user.rate_cur) / (embb_user.sche_times)

                if get_embb_utility(embb_user_lists) >= max_utility:
                    rb_start_final = rb_start
                    rb_num_ass_final = num_req
                    max_utility = get_embb_utility(embb_user_lists)
                rb_start += 1

        return rb_start_final, rb_num_ass_final
