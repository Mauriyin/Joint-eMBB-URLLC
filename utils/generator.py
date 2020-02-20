import random

from libs.user import eMBB_User
from libs.user import URLLC_User
from libs.rb import RB
from utils.utils import get_retrans_schedule

def generate(rb_size,
             rb_num,
             embb_num, 
             embb_slot_len, 
             urllc_num,
             urllc_slot_len,
             embb_rb_req,
             embb_rb_size,
             urllc_rb_req,
             urllc_rb_size,
             urllc_slot_start,
             latency=1,
             error_rate=1e-5,
             mcs_error=1e-3,
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
        embb_rb_req: an int list indicating the req number of rb from each eMBB User.
        embb_rb_size: an int list indicating the rb unit size from each eMBB User.
        urllc_rb_req: an int list indicating  the req number of rb from each URLLCUser.
        urllc_rb_size: an int list indicating the rb unit size from each URLLC User.
        urllc_slot_start: an int list indicating the coming time of each URLLC User.
        latency: an int indicating the lantency maximum constriant of the URLLC User.
        error_rate: a float indicating the maximum error rate constriant of the URLLC User.
        mcs_error: a float indicating error rate for each transmission. 
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
    assert len(embb_rb_req) == embb_num == len(embb_rb_size)
    for i in range(embb_num):
        rb_num_req = embb_rb_req[i]
        rb_size = embb_rb_size[i]
        embb_user = eMBB_User(id_current+i, rb_size, rb_num_req, embb_slot_len)
        embb_user.active = 1 # active at the beginning, time slot 0
        embb_users.append(embb_user)

    id_current = embb_num + 1

    # generate urllc, id in sequence, rb_num_req & slot_start in random
    assert len(urllc_rb_req) == urllc_num == len(urllc_rb_size) == len(urllc_slot_start)
    for i in range(urllc_num):
        rb_num_req = urllc_rb_req[i]
        slot_start = urllc_slot_start[i]
        rb_size = urllc_rb_size[i]
        retrans, trans_start = get_retrans_schedule(latency, error_rate, mcs_error)
        assert retrans == len(trans_start)
        trans_start.insert(0, 0)
        for j in range(retrans+1):
            t = trans_start[j]
            urllc_user = URLLC_User(id_current+i+j, rb_size, rb_num_req, urllc_slot_len,
                slot_start+t, retrans, latency, error_rate, mcs_error)
            urllc_user.active = 1
            urllc_users.append(urllc_user)
        id_current = id_current + retrans

    RB_map = RB(rb_num, rb_size, embb_num)

    return embb_users, urllc_users, RB_map, id_total


def generate_urllc(
             urllc_num,
             urllc_slot_len,
             urllc_rb_req,
             urllc_rb_size,
             urllc_slot_start,
             latency=1,
             error_rate=1e-5,
             mcs_error=1e-5,
             id_current,
             ):
    urllc_users = []
    for i in range(urllc_num):
        rb_num_req = urllc_rb_req[i]
        slot_start = urllc_slot_start[i]
        rb_size = urllc_rb_size[i]
        retrans, trans_start = get_retrans_schedule(latency, error_rate, mcs_error)
        assert retrans == len(trans_start)
        trans_start.insert(0, 0)
        for j in range(retrans+1):
            t = trans_start[j]
            urllc_user = URLLC_User(id_current+i+j, rb_size, rb_num_req, urllc_slot_len,
                slot_start+t, retrans, latency, error_rate, mcs_error)
            urllc_user.active = 1
            urllc_users.append(urllc_user)
        id_current = id_current + retrans

    return urllc_users, id_total