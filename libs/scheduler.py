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