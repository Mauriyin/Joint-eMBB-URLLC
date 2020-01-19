from libs.scheduler import Scheduler
from utils.utils import get_safe_true_start


class NaiveSolver(Scheduler):
    """Scheduler for URLLC users with naive method.
       
       Assign for the URLLC users within the arriving order.
    
    """

    def __init__(self, RB_map, embb_users, urllc_users, solver):
        Scheduler.__init__(self, RB_map, urllc_users)
        self.embb_users = embb_users
        self.solver = solver

    def allocate_resource(self):
        rb_start = get_safe_true_start(self.RB_map.bitmap==0)
        if rb_start is None:
            print("ERROR: There is no free rb available")
                break
        rb_current = self.RB_map.rb_avi - rb_start
        for i in self.user_indexes:
            urllc_user = self.users[i]
            if urllc_user.active == 0:
                print("ERROR: Inactive URLLC user is not clear!")
                continue
            if rb_current >= urllc_user.rb_num_req:
                # assign to the free rb first
                urllc_user.rb_num_ass = urllc_user.rb_num_req
                urllc_user.sche_times += 1
                urllc_user.rb_start = rb_start
                rb_start += urllc_user.rb_num_ass
                rb_current -= urllc_user.rb_num_req
                self.RB_map.bitmap[rb_start:urllc_user.rb_num_req+rb_start] = int(urllc_user.user_info['id'])
            else:
                # get all the available rb region assigned to embb_user before
                rb_start_list, num_ass_list = self.RB_map.find_all_nofree_rb()
                if len(rb_start_list) == 0:
                    print("ERROR: There is no free rb available")
                    break
                
                # solver: modify status of urllc_user, embb_users and RB_map.bitmap
                self._solver(rb_start_list, num_ass_list, i)

    def _solver(self, rb_start_list, num_ass_list, idx):


        

                

    



        