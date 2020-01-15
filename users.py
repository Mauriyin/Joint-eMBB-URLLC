class Users:
    id = 0
    rb_size = 0
    rb_num_req = 0
    rb_num_ass = 0
    rb_start = 0
    sche_times = 0
    Active = 0

    def __init__(self, uid, size, req):
        self.id = uid
        self.rb_size = size
        self.rb_num_req = req

    def current_status(self):
        print("Current status of user %d is:\nRB_size: %d\nRB_num_req: %d\nRB_num_ass: %d\nRB_start is %d\n" %(self.id, self.rb_size, self.rb_num_req, self.rb_num_ass, self.rb_start))


class eMBB_User(Users):
    DRC = 0.0
    rate_slot = 0.0
    rate_avg = 0.0
    slot_len = 0
    

    def __init__(self,  uid, size, req, slot_len):
        Users.__init__(self, uid, size, req)
        self.slot_len = slot_len
        self.DRC = (self.rb_size * self.rb_num_req / 1000) / slot_len
    
    def current_status(self):
        print("Current RB status of user %d is:\nRB_size: %d\nRB_num_req: %d\nRB_num_ass: %d\nRB_start is %d\n" %(self.id, self.rb_size, self.rb_num_req, self.rb_num_ass, self.rb_start))
        print("Current Rate status of user %d is:\nDRC: %f\nslot length: %d\nrate in this slot: %f\naverage rate is %f\n" %(self.id, self.DRC, self.slot_len, self.rate_slot, self.rate_avg))

class URLLC_User(Users):
    latency = 0.0
    errer_rate = 0.0
    slot_len = 0
    slot_start = 0
    retrans = 0

    def __init__(self,  uid, size, req, slot_len, slot_start, latency, error_rate):
        Users.__init__(self, uid, size, req)
        self.slot_len = slot_len
        self.slot_start = slot_start
        self.latency = latency
        self.errer_rate = error_rate

    def current_status(self):
        print("Current RB status of user %d is:\nRB_size: %d\nRB_num_req: %d\nRB_num_ass: %d\nRB_start is %d\n" %(self.id, self.rb_size, self.rb_num_req, self.rb_num_ass, self.rb_start))
        print("Current status of URLLC user %d is:\nLatency constraint: %d ms\nmini slot length: %d\nstart in slot: %d\nretransmission times: %d\n" %(self.id, self.latency, self.slot_len, self.slot_start, self.retrans))

class Scheduler():
    rb_avi = 0
    user_num = 0
    user_info = []
    user_que = []
    bitmap = []
    user_sort = []
    def __init__(self, rb, unum, uinfo, uqueue):
        self.rb_avi = rb
        self.user_num = unum
        self.user_info = uinfo
        self.user_que = uqueue
    
    def user_select(self):
        self.user_sort = self.user_info['id']
        if self.user_sort.size < user_num:
            print ("ERROR: user info is not enough!")
        elif self.user_sort.size > user_num:
            print ("ERROR: Inactive user is not clear!")
    
    def allocate_resource(self):
        self.rb_avi = 8

class PfScheduler(Scheduler):
    rb_avi = 0
    user_num = 0
    pf_win = 100
    user_info = []
    user_que = []
    bitmap = []
    user_sort = []

    def __init__(self, rb, unum, uinfo, uqueue):
        self.rb_avi = rb
        self.user_num = unum
        self.user_info = uinfo
        self.user_que = uqueue
    
    def user_select(self):
        pf_weight = []
        for i in self.user_que:
            weighti = (i.DRC)/(0.01*(i.DRC) + 0.99*(i.rate_avg))
            pf_weight.append(weighti)
        self.user_sort = [index for index,value in sorted(list(enumerate(pf_weight)),key=lambda x:x[1],reverse = True)]
    
    def allocate_resource(self):
        rb_current = self.rb_avi
        rb_start = 0
        for i in self.user_sort:
            if rb_current >= self.user_que[i].rb_num_req:
                self.user_que[i].rb_num_ass = self.user_que[i].rb_num_req
                self.user_que[i].rate_avg = (self.user_que[i].rate_avg * self.user_que[i].sche_times + self.user_que[i].DRC) / (self.user_que[i].sche_times + 1)
                self.user_que[i].sche_times += 1
                self.user_que[i].rb_start = rb_start
                rb_start += self.user_que[i].rb_num_ass
                rb_current -= self.user_que[i].rb_num_req
            else:
                self.user_que[i].rb_num_ass = rb_current
                self.user_que[i].rate_avg = (self.user_que[i].rate_avg * self.user_que[i].sche_times + (rb_current * self.user_que[i].rb_size / 1000) / self.user_que[i].slot_len) / (self.user_que[i].sche_times + 1)
                self.user_que[i].sche_times += 1
                self.user_que[i].rb_start = rb_start
                break


                