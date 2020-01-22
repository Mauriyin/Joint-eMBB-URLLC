import time
import numpy as np

import _init_paths
from libs.scheduler import PfScheduler
from libs.models.naive_solver import NaiveURLLCSolver
from libs.models.greedy_solver import GreedyURLLCSolver
from utils.generator import generate
from utils.metrics import get_embb_utility
# from utils.visualization import draw_matrix

# parameter setting
rb_num = 5
embb_num = 5
embb_slot_len = 7
urllc_num = 7
urllc_slot_len = 1
max_sim_time_slot_len = 20

#urllc scheduler setting
URLLCSolver = NaiveURLLCSolver
# URLLCSolver = GreedyURLLCSolver

# generate
embb_users, urllc_users, RB_map = generate(rb_size,
    rb_num,
    embb_num, 
    embb_slot_len, 
    urllc_num,
    urllc_slot_len,
    latency=1,
    error_rate=1e-5,
    mcs_error=1e-3,
)

global_time = 0
global_timeout_urllc_users = []
delay_users = []

# embb_time_slot pfs scheduler
pf_scheduler = PfScheduler(RB_map, embb_users)
pf_scheduler.allocate_resource()

# urllc_time_slot get urllc_active_come_list, setting urllc come from global_time=1 and later
urllc_users.sort(key=lambda x:x.slot_start)
urllc_come_time = np.array([u.slot_start for u in urllc_users])

timer = []
# urllc scheduler loop for all the urllc_time_slot without considering embb user rescheduling
while(global_time <= max_sim_time_slot_len):
    global_time += 1
    current_slot_time = global_time % embb_slot_len
    indexes = np.where(urllc_come_time==current_slot_time)[0]
    if len(indexes) == 0:
        continue
    urllc_users_list = delay_users + urllc_users.copy()[indexes[0]:indexes[-1]+1]
    
    urllc_scheduler = URLLCSolver(RB_map, embb_users, urllc_users_list)

    start = time.time()
    delay_users, timeout_users = urllc_scheduler.allocate_resource()
    timer.append(time.time() - start)

    global_timeout_urllc_users.append(timeout_users)
    
# get_embb_utility miss_list and time cost for all the urllc scheduler within the embb_time_slot
embb_utility = get_embb_utility(embb_users)
global_timeout_urllc_users = set(global_timeout_urllc_users)
total_time_cost = sum(timer)

# visualize (TODO)

# next embb_time_slot (not show here)



