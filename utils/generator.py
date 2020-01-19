import random

from libs.user import eMBB_User
from libs.user import URLLC_User
from libs.rb import RB

def generate(
             rb_size,
             rb_num,
             embb_num, 
             embb_slot_len, 
             urllc_num,
             urllc_slot_len,
             latency,
             error_rate,
             ):
    """Generate the simulation input of eMBB Users and URLLC Users, 
       as well as initializing RB status.

       URLLC Users id after all the eMBB Users, all the id values greater than 0.
       eMBB Users come at the beginning of the global time slot, URLLC Users come at 
       random points of the global time slot.

    Args:
        rb_size: an int indicating the size of one rb unit.
        rb_num: an int indicating the total number of rb units. #TODO is this right?
        embb_num: an int indicating the total number of coming eMBB Users.
        embb_slot_len: an int indicating the scheduler time slot length for an eMBB User, 
            the functioning frequency of eMBB User scheduler. #TODO is this right?
        urllc_num: an int indicating the total number of coming URLLC Users.
        urllc_slot_len: an int indicating the scheduler time slot length for an URLLC User, 
            the functioning frequency of URLLC User scheduler. #TODO is this right?
        latency: a float indicating the lantency maximum constriant of the URLLC User.
        error_rate: a float indicating the maximum error rate constriant of the URLLC User.
        
    Return:
        RB_map: a RB instance indicating the status of rb units.
        embb_users: a list of eMBB_User instances indicating the information of coming eMBB Users 
            without assignment.
        urllc_users: a list of URLLC_User instances indicating the information of coming unallocated URLLC Users 
            without assignment.
    """

    random.seed()
    
    embb_users = []
    urllc_users = []
    id_current = 1
    slot_len = max(embb_slot_len, urllc_slot_len)
    # generate embb, id in sequence, rb_num_req in random
    embb_upper = int(rb_avi / 5)
    assert embb_upper >=0
    for i in range(embb_num):
        rb_num_req = random.randint(0, embb_upper)
        embb_user = eMBB_User(id_current+i, rb_size, rb_num_req, embb_slot_len)
        embb_user.active = 1 # active at the beginning, time slot 0
        embb_users.append(embb_user)

    id_current = embb_num + 1

    # generate urllc, id in sequence, rb_num_req & slot_start in random
    urllc_upper = int(rb_avi / 3)
    assert urllc_upper >=0
    for i in range(urllc_num):
        rb_num_req = random.randint(0, urllc_upper)
        slot_start = random.randint(1, slot_len)
        urllc_user = URLLC_User(id_current+i, rb_size, rb_num_req, urllc_slot_len,
            slot_start, latency, error_rate)
        urllc_users.append(urllc_user)

    RB_map = RB(rb_num, rb_size, embb_num)

    return embb_users, urllc_users, RB_map




