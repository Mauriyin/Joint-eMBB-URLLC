from libs.scheduler import Scheduler
from utils.utils import get_safe_true_start


class NaiveURLLCSolver(Scheduler):
    """Scheduler for URLLC users with naive method.
       
       Assign for the URLLC users within the arriving order, assign the last 
       qualified rb region.
    
    """

    def __init__(self, RB_map, embb_users, urllc_users):
        Scheduler.__init__(self, RB_map, urllc_users)
        self.embb_users = embb_users

    def allocate_resource(self):
        self._user_sort()

        self.delay_users = []
        self.timeout_users = []
        for i in self.user_indexes:
            urllc_user = self.users[i]
            if self.ddl_list[i] < 0:
                print("URLLC user %d is time out" %(urllc_user.user_info['id']))
                self.timeout_users.append(urllc_user)
                continue
            if urllc_user.active == 0:
                print("ERROR: Inactive URLLC user is not clear!")
                continue
            
            # get all the available rb region assigned to embb_user before
            rb_start_list, num_ass_list = self.RB_map.find_all_nofree_rb(urllc_user.rb_num_req)

            if len(rb_start_list) == 0:
                # wait for delay, return unscheduled urllc user list
                print("There is no free rb available for URLLC user %d" %(urllc_user.user_info['id']))
                urllc_user.delay += 1
                self.delay_users.append(urllc_user)
                continue
                
            # solver
            rb_start, rb_num_ass = self._solver(rb_start_list, num_ass_list)

            self._update(rb_start, rb_num_ass, urllc_user)

        return self.delay_users, self.timeout_users

    def _solver(self, rb_start_list, num_ass_list):
        """Naive solver.
           Assign the last suitable and available rb region.
           Return the rb_bitmap start point and corresponding assigned rb unit number.

        """
        rb_start = rb_start_list[-1]
        rb_num_ass = num_ass_list[-1]
        return rb_start, rb_num_ass

    def _update(self, rb_start, rb_num_ass, urllc_user):
        """Update status.
           modify status of urllc_user.
           modify rate_avg of embb_users and RB_map.bitmap.

        """
        urllc_user.rb_start = rb_start
        urllc_user.rb_num_ass = rb_num_ass
        urllc_user.sche_times += 1
        for k in range(rb_num_ass):
            if self.RB_map.bitmap[rb_start+k] > 0:
                embb_user = self.embb_users[self.RB_map.bitmap[rb_start+k]-1]
                if embb_user.active == 0:
                    print ("ERROR: Inactive embb user is not clear!")
                else:
                    embb_user.rate_avg = (embb_user.rate_avg * embb_user.sche_times - 1) / embb_user.sche_times
            self.RB_map.bitmap[rb_start+k] = int(urllc_user.user_info['id'])
    
    def _user_sort(self):
        """Sort based on ddl = latency-delay.
           Assign rb to users with less ddl.
        """

        self.ddl_list = []
        for i in self.users:
            ddl = i.latency - i.delay
            self.ddl_list.append(ddl)
        self.user_indexes = [index for index, value in sorted(list(enumerate(self.ddl_list)),key=lambda x:x[1])]




        

                

    



        