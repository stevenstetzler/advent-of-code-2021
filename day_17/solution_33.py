from typing_extensions import final
import numpy as np
import io
import argparse

def test_velocity(vx, vy, xrange, yrange):
    x, y = 0, 0
    xs, ys = [], []
    while True:
        x += vx
        if vx > 0:
            vx -= 1
        y += vy
        vy -= 1
        xs.append(x)
        ys.append(y)
        if (x <= xrange[1]) and (x >= xrange[0]) and (y <= yrange[1]) and (y >= yrange[0]):
            return True, xs, ys
        else:
            if x > xrange[1] or y < yrange[0]:
                return False, xs, ys

def project_velocity(vx, vy, xrange, yrange):
    x, y = 0, 0
    xs, ys = [], []
    while True:
        x += vx
        if vx > 0:
            vx -= 1
        y += vy
        vy -= 1
        xs.append(x)
        ys.append(y)
        if x >= xrange[1] or y <= yrange[0]:
            return xs, ys

def draw_trajectory(xs, ys, target_xrange, target_yrange):
    xrange = [min([0, min(xs), min(target_xrange)]), max([0, max(xs), max(target_xrange)])]
    xrange = np.arange(xrange[0], xrange[1] + 1)
    yrange = [min([0, min(ys), min(target_yrange)]), max([0, max(ys), max(target_yrange)])]
    yrange = np.arange(yrange[0], yrange[1] + 1)
    points = [(x, y) for x, y in zip(xs, ys)]
    for y in yrange[::-1]:
        for x in xrange:
            if (x == 0) and (y == 0):
                print("S", end="")
            elif (x, y) in points:
                print("#", end="")
            elif (x <= target_xrange[1]) and (x >= target_xrange[0]) and (y <= target_yrange[1]) and (y >= target_yrange[0]):
                print("T", end="")
            else:
                print(".", end="")
        print("")
    print("")

# 1/2 a t^2 + v t + x = target_x
# a = -1 * sign(v)
# t = (-v +- sqrt(v^2 - a*x)) / (a)
def number_of_ticks_until_hit_x(v, x):
    a = -1 * np.sign(v)
    t1 = (-v - np.sqrt(v**2 - a * x)) / a
    t1 = (-v + np.sqrt(v**2 - a * x)) / a

# What sets the upper bound on y?
# in the number of ticks it takes to get there in x,
# I 

# it takes 6 ticks to get there in x
# I have 6 ticks to 

def number_of_ticks_until_hit(vx, xrange):
    i = 0
    x = 0
    _vx = int(vx)
    while True:
        i += 1
        x += vx
        if (x <= xrange[1]) and (x >= xrange[0]):
            # print(x, "in", xrange, "for", _vx, "after", i)
            return i
        if vx == 0:
            return -1
        elif vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        else:
            vx = 0

def number_of_ticks_until_hit_y(vy, yrange):
    i = 0
    x = 0
    _vy = int(vy)
    while True:
        i += 1
        x += vx
        if (x <= yrange[1]) and (x >= yrange[0]):
            # print(x, "in", xrange, "for", _vx, "after", i)
            return i
        if vx == 0:
            return -1
        elif vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        else:
            vx = 0


def acceptable_vx(xrange):
    vxs = []
    for vx in range(0, xrange[1] + 1):
        num_ticks = number_of_ticks_until_hit(vx, xrange)
        if num_ticks != -1:
            vxs.append((vx, num_ticks))
    return vxs

def acceptable_vy(yrange, num_ticks):
    # 1/2 a t^2 + v * t + y = y_target
    # v = ((y_target - y) - 1/2 a t^2) / t
    v1 = ((yrange[1]) / num_ticks) - 0.5 * (-1) * (num_ticks)
    v2 = ((yrange[0]) / num_ticks) - 0.5 * (-1) * (num_ticks)
    if v1 < v2:
        return [v1, v2]
    else:
        return [v2, v1]



# what sets the bounds on the search?
# for x: it is certainly less than xrange[1]
# for x: it is certainly more than 0
# for x: the minimum velocity is one that decays to 0 at xrange[0]
#        which means that v + (v - 1) + (v - 2) + ... = xrange[0]
# for 0: it travels 0 distance
# for 1: it travels 1 + 0 distance
# for 2: it travels 2 + 1 distance
# for v: it travels sum_{1}^{v} distance
# sum_{i = 1}^{v} i = xrange[0]
# sum_{1 = 1}^{v} i = 0.5 * v * (v + 1)
# 0.5 * v * (v + 1) = xrange[0]
# v^2 + v - 2 * xrange[0] = 0
# v = (-1 +- sqrt(1 + 8 * xrange[0])) / 2
# take positive solution and round up unless an integer solution

# for y: v + (v - 1) + (v - 2) ...
# evaluate after the number of ticks for x? 
# what makes x different from y?
# you have to go right to get there in x, and vx tends to 0
# for y, you can go up or down and be positive or negative
# for y: must be at yrange[1] or yrange[0] by time t
# for y: distance = sum_{i = v - t + 1}^{v} = (1/2) * (t) * (2*vy - t - 1)
# (1/2) * (t + 2) * (2*vy - t - 1) = yrange[0]
# vy = (2 * yrange[0]) / (t) + t + 1
# (1/2) * (t + 2) * (2*vy - t - 1) = yrange[1]
# vy = (2 * yrange[1]) / (t) + t + 1
# if vx is 0: t can tend to infinity, have freedom to pick trajectory in y as long as t >= t_x
#   distance traveled in y after time t: (1/2) * (t) * (2*vy - t + 1)
#   (1/2) * (t) * (2*vy - t + 1) = yrange[0]
#   -(1/2) t^2 + (vy + 1/2) t - yrange[0] = 0
#   t^2 - (2*vy + 1) * t + 2 * yrange[0] = 0
#   t = ((2*vy + 1) +- sqrt((2*vy + 1)**2 - 8 * yrange[0]))/2
#   require t >= t_x
#   ((2*vy + 1) +- sqrt(((2*vy + 1))**2 - 8 * yrange[0]))/2 >= t_x
#   ((2*vy + 1)**2 - 8 * yrange[0]) > 0
#   2*vy + 1 > sqrt(8 * yrange[0])
#   vy > (sqrt(8 * yrange[0]) - 1) / 2
# else: y must be in range after t, so solve 
#   distance traveled in y after time t: (1/2) * (t) * (2*vy - t + 1)
#   (1/2) * (t) * (2*vy - t + 1) = yrange[0]
#   vy_min = (yrange[0] / t) + (t - 1) / 2
#   vy_max = (yrange[1] / t) + (t - 1) / 2
#   search [int(vy_min), int(vy_max)]
# how about: for each y in target, find 
# if t > t_x, vy_min goes up, so vy_min is inclusive

# it's got to be that it's due to the overshoot
# at some velocity and for all larger than it, it starts overshooting
# what is that velocity?
# overshooting means that:
# in one tick it traverses greater than yrange[1] - yrange[0] distance
# at y = 0, it will be travelling at velocity -vy
# so -vy must certainly be smaller than yrange[0]!
# or vy < -yrange[0]

# if v = 1

def evaluate_trajectory_x(vx, xmin, xmax):
    x = 0
    i = 0
    in_target_times_and_velocities = []
    while True:
        i += 1
        x += vx
        vx += -1 * np.sign(vx)
        if (x <= xmax) and (x >= xmin):
            in_target_times_and_velocities.append((i, vx))
        # never reaches the target
        if vx == 0:
            break
        # has passed target
        if x > xmax:
            break
    return in_target_times_and_velocities

def evaluate_trajectory_y(vy, ymin, ymax):
    y = 0
    i = 0
    in_target_times_and_velocities = []
    while True:
        i += 1
        y += vy
        vy -= 1
        if (y <= ymax) and (y >= ymin):
            in_target_times_and_velocities.append((i, vy))
        # has passed target
        if y < ymin:
            break
    return in_target_times_and_velocities

def _get_succesful_trajectories(xrange, yrange):
    trajectories = []
    # sum_{1 = 1}^{v} i = 0.5 * v * (v + 1)
    # 0.5 * v * (v + 1) = xrange[0]
    # v^2 + v - 2 * xrange[0] = 0
    # v = (-1 +- sqrt(1 + 8 * xrange[0])) / 2
    vx_min = (-1 + np.sqrt(1 + 8 * xrange[0])) / 2
    # take positive solution and round up unless an integer solution
    if (vx_min - int(vx_min)) > 0.0:
        vx_min = int(vx_min) + 1
    vx_max = xrange[1]

    # print("vx range", vx_min, vx_max + 1)
    vxs = np.arange(vx_min, vx_max)
    for vx in vxs:
        in_target_times_and_velocities_x = evaluate_trajectory_x(vx, xrange[0], xrange[1])
        if len(in_target_times_and_velocities_x) == 0:
            # print(vx, "no trajectories")
            continue

        for t, final_vx in in_target_times_and_velocities_x:
            # print(vx, final_vx)
            if final_vx == 0:
                # print(vx, "drift trajectory")
                # for vx = 0 at target:
                #   require that vy < -yrange[0]
                #   require that vy > (yrange[0] / t) + (t - 1) / 2
                vy_min = int((yrange[0] / t) + (t - 1) / 2)
                vy_max = -yrange[0]
                # if vx is 0: t can tend to infinity, then solve kinematic in y and ensure ty > t
            else:
                # for vx != 0 at target:
                #   require that vy < (yrange[1] / t) + (t - 1) / 2
                #   require that vy > (yrange[0] / t) + (t - 1) / 2
                vy_min = int((yrange[0] / t) + (t - 1) / 2)
                vy_max = int((yrange[1] / t) + (t - 1) / 2) + 1

            # print(vx, "vy range", vy_min, vy_max)
            vys = np.arange(vy_min, vy_max + 1)
            for vy in vys:
                # properly handle overlap in trajectories
                # can get inconsistent times of hits
                in_target_times_and_velocities_y = evaluate_trajectory_y(vy, yrange[0], yrange[1])
                # hit = evaluate_trajectory_y(vy, t, yrange[0], yrange[1])
                if len(in_target_times_and_velocities_y) == 0:
                    # print(vy, "no trajectories in y")
                    continue
                for t_y, _vy in in_target_times_and_velocities_y:
                    # if final_vx != 0 and t != t_y:
                    #     continue
                    trajectories.append((vx, vy, final_vx, t, t_y))
    
    return trajectories

def get_succesful_trajectories(xrange, yrange):
    # minimum x velocity is set by reaching 0 velocity at the left
    # edge of the target zone
    # distance traveled in x: sum_{1 = 1}^{v} i = 0.5 * v * (v + 1)
    # 0.5 * v * (v + 1) = xrange[0]
    # v^2 + v - 2 * xrange[0] = 0
    # v = (-1 +- sqrt(1 + 8 * xrange[0])) / 2
    # take positive solution
    vx_min = (-1 + np.sqrt(1 + 8 * xrange[0])) / 2
    # and round down for an inclusive lower bound
    vx_min = int(vx_min)
    # maximum x velocity is set by hitting the right edge after 1 tick
    vx_max = xrange[1]

    # minimum y velocity is set by hitting the bottom edge after 1 tick
    vy_min = yrange[0] - 1
    # maximum y velocity is set by overshooting the bottom edge 1 tick before
    # the target
    # this is found by realizing that when shooting upward, 
    # vy = -vy_init at y = 0 on the way down
    # so vy_init should certainly be less than -yrange[0]
    vy_max = -yrange[0] + 1

    trajectories = []
    for vx in np.arange(vx_min, vx_max + 1):
        for vy in np.arange(vy_min, vy_max + 1):
            hit, xs, ys = test_velocity(vx, vy, xrange, yrange)
            if hit:
                trajectories.append((vx, vy, xs, ys))
    return trajectories

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--verbose", action="store_true")

    args, _ = parser.parse_known_args()
    test = args.test
    verbose = args.verbose

    if test:
        infile = "test_input"
    else:
        infile = "input"
    
    with open(infile, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]

    xrange, yrange = lines[0].split(" ")[2:]
    xrange = list(map(int, xrange.split(",")[0].split("=")[1].split("..")))
    yrange = list(map(int, yrange.split("=")[1].split("..")))


    trajectories = get_succesful_trajectories(xrange, yrange)

    highest_trajectory = None
    max_y = -np.inf
    for vx, vy, xs, ys in trajectories:
        if max(ys) > max_y:
            highest_trajectory = (vx, vy, xs, ys)
            max_y = max(ys)

    vx, vy, xs, ys = highest_trajectory
    if verbose:
        draw_trajectory(xs, ys, xrange, yrange)

    print(f"vx, vy = {vx,vy} max-y = {max_y}")

if __name__ == "__main__":
    main()
