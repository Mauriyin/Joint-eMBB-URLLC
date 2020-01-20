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
        self._user_sort()
        for i in self.user_indexes:
            urllc_user = self.users[i]
            if urllc_user.active == 0:
                print("ERROR: Inactive URLLC user is not clear!")
                continue

            # get all the available rb region assigned to embb_user before
            rb_start_list, num_ass_list = self.RB_map.find_all_nofree_rb(urllc_user.rb_num_req)
            if len(rb_start_list) == 0:
                # wait for delay, return unscheduled urllc user list
                print("There is no free rb available")
                return self.users[i:]
                
            # solver
            rb_start, rb_num_ass = self._solver(rb_start_list, num_ass_list, urllc_user)

            # modify status of urllc_user, embb_users and RB_map.bitmap
            urllc_user.rb_num_ass = rb_num_ass
            urllc_user.sche_times += 1
        return []   

    def _solver(self, rb_start_list, num_ass_list, urllc_user):



    def _user_sort(self):
        """Sort based on .

        """

        pass




        

                

    



        