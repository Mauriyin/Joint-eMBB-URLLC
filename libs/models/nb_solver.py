from libs.models.naive_solver import NaiveURLLCSolver
from utils.metrics import get_embb_utility
import matlab
import matlab.engine


class CccpURLLCSolver(NaiveURLLCSolver):
    """Scheduler for URLLC users with cccp algorithm.
       Assign for the URLLC users within the arriving order, 
       calculate the embb utility for each possible assignment plan 
       and choose the optimal one for the current urllc user.
    
    """
    def __init__(self, RB_map, embb_users, urllc_users, engine):
        NaiveURLLCSolver.__init__(self, RB_map, embb_users, urllc_users)
        self.engine = engine

    def allocate_resource(self):
        #engine = matlab.engine.start_matlab()
        self.ass_users = []
        self.delay_users = []
        self.timeout_users = []
        # NOTICE: all users should be active
        embb_num = []
        embb_num.append(len(self.embb_users))
        total_RB = []
        total_RB.append(self.RB_map.rb_avi)
        y_start_end = []
        embb_rate = []
        embb_rb_ass = []
        drc = []
        urllc_num = []
        urllc_num.append(len(self.users))
        urllc_rb_perusr = []

        for users in self.embb_users:
            start_rb = int(users.__dict__['rb_start']) + 1
            end_rb = start_rb + int(users.__dict__['rb_num_ass']) - 1
            y_start_end.append(start_rb)
            y_start_end.append(end_rb)
            embb_rate.append(float(users.__dict__['rate_cur']))
            embb_rb_ass.append(int(users.__dict__['rb_num_ass']) * 7)
            drc.append(float(users.__dict__['DRC']))

        for users in self.users:
            rb_req = int(users.__dict__['rb_num_req'])
            urllc_rb_perusr.append(rb_req)

        print(embb_num)
        print(total_RB)
        print(y_start_end)
        print(embb_rate)
        print(embb_rb_ass)
        print(drc)
        print(urllc_num)
        print(urllc_rb_perusr)
        current_rate = self.engine.dc_main(matlab.double(embb_num),
                                           matlab.double(total_RB),
                                           matlab.double(y_start_end),
                                           matlab.double(embb_rate),
                                           matlab.double(embb_rb_ass),
                                           matlab.double(urllc_num),
                                           matlab.double(urllc_rb_perusr),
                                           matlab.double(drc))
        c = []
        for _ in range(current_rate.size[1]):
            c.append(current_rate._data[_ * current_rate.size[0]:_ *
                                        current_rate.size[0] +
                                        current_rate.size[0]].tolist())
        for i in range(len(self.embb_users)):
            embb_user = self.embb_users[i]
            if embb_user.sche_times:
                if embb_user.sche_times > 1:
                    embb_user.rate_avg = (
                        embb_user.rate_avg * (embb_user.sche_times) -
                        embb_user.rate_cur) / (embb_user.sche_times - 1)
                embb_user.rate_cur = float(c[0][i])
                embb_user.rate_avg = (
                    embb_user.rate_avg * (embb_user.sche_times - 1) +
                    embb_user.rate_cur) / (embb_user.sche_times)
        return self.ass_users, self.delay_users, self.timeout_users
