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
rb_size = 15
rb_num = 254
embb_num = 3
embb_slot_len = 7
urllc_num = 6
urllc_slot_len = 1
max_sim_time_slot_len = embb_slot_len

embb_rb_req = [100, 50, 120]
embb_rb_size = [60, 120, 30]
urllc_rb_req = [10, 10, 10, 10, 10, 10]
urllc_rb_size = [30, 30, 30, 30, 30, 30]
urllc_slot_start = [1, 2, 3, 4, 5, 6]

#urllc scheduler setting
URLLCSolver = NaiveURLLCSolver
# URLLCSolver = GreedyURLLCSolver

# generate
embb_users, urllc_users, RB_map = generate(
    rb_size,
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
)

global_time = 0
global_timeout_urllc_users = []

# embb_time_slot pfs scheduler
pf_scheduler = PfScheduler(RB_map, embb_users)
pf_scheduler.allocate_resource()

urllc_users.sort(key=lambda x: x.slot_start)
urllc_come_time = np.array([u.slot_start for u in urllc_users])

delay_users = []
timer = []

while (global_time < max_sim_time_slot_len):
    global_time += 1
    indexes = np.where(urllc_come_time == global_time)[0]
    if len(indexes) == 0:
        continue
    urllc_users_list = delay_users + urllc_users.copy(
    )[indexes[0]:indexes[-1] + 1]

    urllc_scheduler = URLLCSolver(RB_map, embb_users, urllc_users_list)

    start = time.time()
    ass_users, delay_users, timeout_users = urllc_scheduler.allocate_resource()
    timer.append(time.time() - start)

    global_timeout_urllc_users.append(timeout_users)

    # urllc leave
    urllc_scheduler.leave(ass_users)

# get_embb_utility miss_list and time cost for all the urllc scheduler
embb_utility = get_embb_utility(embb_users)
total_time_cost = sum(timer)

# visualize (TODO)
for user in embb_users:
    print(user.__dict__.items())
print("\n")
print(RB_map.__dict__.items())

# next embb_time_slot (not show here)
