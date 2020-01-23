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
        self.ass_users = []
        self.delay_users = []
        self.timeout_users = []
        for i in self.user_indexes:
            urllc_user = self.users[i]
            if self.ddl_list[i] < 0:
                urllc_user.miss += 1
                if urllc_user.miss == urllc_user.retrans + 1:
                    print("URLLC user %d is time out" %(urllc_user.user_info['id']))
                    self.timeout_users.append(urllc_user)
                elif urllc_user.miss > urllc_user.retrans + 1:
                    print("URLLC user %d error trans" %(urllc_user.user_info['id']))
                continue
            if urllc_user.active == 0:
                print("ERROR: Inactive URLLC user is not clear!")
                continue
            
            # get all the available rb region assigned to embb_user before
            rb_start_list, num_ass_list = self.RB_map.find_all_avi_rb(urllc_user.rb_num_req)

            if len(rb_start_list) == 0:
                # wait for delay, return unscheduled urllc user list
                print("There is no free rb available for URLLC user %d" %(urllc_user.user_info['id']))
                urllc_user.delay += 1
                self.delay_users.append(urllc_user)
                continue
                
            # solver
            rb_start, rb_num_ass = self._solver(rb_start_list, num_ass_list)

            self.ass_users.append(self._update(rb_start, rb_num_ass, urllc_user))

        for embb_user in self.embb_users:
            # cal avg???? TODO
            if embb_user.sche_times:
                embb_user.rate_avg = (embb_user.rate_avg * (embb_user.rb_num_ass - embb_user.replace_num)) / embb_user.rb_num_ass
                
        return self.ass_users, self.delay_users, self.timeout_users
    
    def leave(self, urllc_user_list):
        """Assigned URLLC user leave after the urllc time slot.
           Recover bitmap and embb status.

        """
        for urllc_user in urllc_user_list:
            rb_start = urllc_user.rb_start
            rb_num_ass = urllc_user.rb_num_ass
            assert len(urllc_user.ori_embb) > 0
            for k in range(rb_num_ass):
                id = urllc_user.ori_embb[k]
                if id > 0 and id <= len(self.embb_users):
                    self.embb_users[id-1].replace_num = max(0, self.embb_users[id-1].replace_num-1)
                self.RB_map.bitmap[rb_start+k] = id

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
        rb_num_ass = min(rb_num_ass, urllc_user.rb_num_req)
        urllc_user.rb_start = rb_start
        urllc_user.rb_num_ass = rb_num_ass
        urllc_user.ori_embb = []
        urllc_user.sche_times += 1
        for k in range(rb_num_ass):
            if self.RB_map.bitmap[rb_start+k] > 0:
                embb_user = self.embb_users[self.RB_map.bitmap[rb_start+k]-1]
                if embb_user.active == 0 or int(embb_user.user_info['id']) != self.RB_map.bitmap[rb_start+k]:
                    print ("ERROR: embb user mismatched!")
                else:
                    embb_user.replace_num += 1
            urllc_user.ori_embb.append(self.RB_map.bitmap[rb_start+k])
            self.RB_map.bitmap[rb_start+k] = int(urllc_user.user_info['id'])
        assert len(urllc_user.ori_embb) == rb_num_ass

        return urllc_user

    def _user_sort(self):
        """Sort based on ddl = latency-delay.
           Assign rb to users with less ddl.
        """

        self.ddl_list = []
        for i in self.users:
            ddl = i.latency - i.delay
            self.ddl_list.append(ddl)
        self.user_indexes = [index for index, value in sorted(list(enumerate(self.ddl_list)),key=lambda x:x[1])]




        

                

    



        