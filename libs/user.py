class Users:
    """Base class for users.
    
    Attributes:
        user_info: a dict with keys of id (an int) and other info.
        rb_size: an int indicating the size of one rb unit.
        rb_num_req: an int indicating the request number of rb from the user.
        rb_num_ass: an int indicating the actual number of assigned rb.
        rb_start: an int indicating the start index of the rb allocation in the rb bitmap.
        sche_times: an int indicating the scheduling times for the user.
        active: a boolean indicating the active status of the user.
    """
    self.user_info = {}
    self.rb_size = 0
    self.rb_num_req = 0
    self.rb_num_ass = 0
    self.rb_start = 0
    self.sche_times = 0
    self.active = 0

    def __init__(self, uid, rb_size, rb_num_req):
        self.user_info['id'] = uid
        self.rb_size = rb_size
        self.rb_num_req = rb_num_req

    def current_status(self):
        if self.active:
            print("Current status of user %d is active:\nRB_size: %d\nRB_num_req: %d\nRB_num_ass: %d\nRB_start is %d\n" 
                %(self.user_info['id'], self.rb_size, self.rb_num_req, self.rb_num_ass, self.rb_start))
        else:
            print("Current status of user %d is inactive:\nRB_size: %d\nRB_num_req: %d\n"
                %(self.user_info['id'], self.rb_size, self.rb_num_req))


class eMBB_User(Users):
    """Class for eMBB users.
    
    Attributes:
        DRC: a float indicating the maximum data rate.
        rate_slot: a float indicating the local average data rate in the current time slot.  #TODO is this right?
        rate_avg: a float indicating the average data rate on the global time slot.
        slot_len: an int indicating the scheduler time slot length for an eMBB User, 
                  the functioning frequency of eMBB User scheduler. #TODO is this right?
        user_info: a dict with keys of id (an int) and other info.
        rb_size: an int indicating the size of one rb unit.
        rb_num_req: an int indicating the request number of rb from the user.
        rb_num_ass: an int indicating the actual number of assigned rb.
        rb_start: an int indicating the start index of the rb allocation in the rb bitmap.
        sche_times: an int indicating the schduled times for the user.
        active: a boolean indicating the active status of the user.
    """
    self.DRC = 0.0
    self.rate_slot = 0.0
    self.rate_avg = 0.0
    self.slot_len = 0
    
    def __init__(self, uid, rb_size, rb_num_req, slot_len):
        Users.__init__(self, uid, rb_size, rb_num_req)
        self.slot_len = slot_len
        self.DRC = (self.rb_size * self.rb_num_req / 1000) / slot_len
    
    def current_status(self): 
        if self.active:
            print("Current eMBB user status of eMBB user %d is active\n" %(self.user_info['id']))
        else:
            print("Current eMBB user status of eMBB user %d is inactive\n" %(self.user_info['id']))
        print("Current RB status of user %d is:\nRB_size: %d\nRB_num_req: %d\nRB_num_ass: %d\nRB_start is %d\n" %(self.user_info['id'], self.rb_size, self.rb_num_req, self.rb_num_ass, self.rb_start))
        print("Current Rate status of user %d is:\nDRC: %f\nslot length: %d\nrate in this slot: %f\naverage rate is %f\n" %(self.user_info['id'], self.DRC, self.slot_len, self.rate_slot, self.rate_avg))


class URLLC_User(Users):
    """Class for URLLC users.
    
    Attributes:
        latency: a float indicating the lantency maximum constriant of the URLLC User.
        error_rate: a float indicating the maximum error rate constriant of the URLLC User.
        slot_len: an int indicating the scheduler time slot length for an URLLC User, 
                  the functioning frequency of URLLC User scheduler. #TODO is this right?
        slot_start: an int indicating the start point on the global time slot of the URLLC User.
        retrans: an int indicating the retransmission times for the URLLC User.
        user_info: a dict with keys of id (an int) and other info.
        rb_size: an int indicating the size of one rb unit.
        rb_num_req: an int indicating the request number of rb from the user.
        rb_num_ass: an int indicating the actual number of assigned rb.
        rb_start: an int indicating the start index of the rb allocation in the rb bitmap.
        sche_times: an int indicating the schduled times for the user.
        active: a boolean indicating the active status of the user.
    """
    self.latency = 0.0
    self.error_rate = 0.0
    self.slot_len = 0
    self.slot_start = 0
    self.retrans = 0

    def __init__(self, uid, rb_size, rb_req, slot_len, slot_start, latency, error_rate):
        Users.__init__(self, uid, rb_size, rb_req)
        self.slot_len = slot_len
        self.slot_start = slot_start
        self.latency = latency
        self.errer_rate = error_rate

    def current_status(self):
        if self.active:
            print("Current URLLC user status of URLLC user %d is active\n" %(self.user_info['id']))
        else:
            print("Current URLLC user status of URLLC user %d is inactive\n" %(self.user_info['id']))
        print("Current RB status of user %d is:\nRB_size: %d\nRB_num_req: %d\nRB_num_ass: %d\nRB_start is %d\n" 
             %(self.user_info['id'], self.rb_size, self.rb_num_req, self.rb_num_ass, self.rb_start))
        print("Current status of URLLC user %d is:\nLatency constraint: %d ms\nmini slot length: %d\nstart in slot: %d\nretransmission times: %d\n"
             %(self.user_info['id'], self.latency, self.slot_len, self.slot_start, self.retrans))
