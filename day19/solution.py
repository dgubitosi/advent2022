
import re

blueprints = list()
filename = 'test.txt'
with open(filename) as f:
    for line in f:
        blueprints.append(list(map(int, re.findall('\d+', line))))

def build(time, target, costs, robots, resources, max_geodes = 0):

    _ore = max(costs[0], costs[1], costs[2], costs[4])
    _clay = costs[3]
    _obsidian = costs[5]

    # stop making ore robots
    if target == 0 and robots[0] >= _ore:
        return max_geodes
    # stop making clay robots
    elif target == 1 and robots[1] >= _clay:
        return max_geodes
    # stop making obsidian robots
    elif target == 2 and robots[2] >= _obsidian:
        return max_geodes
    # we always make geode robots if possible
    #elif target == 3 and (resources[2] == 0):
    #    return max_geodes

    # collect and build
    while time:
        resources = [sum(i) for i in zip(robots, resources)]
        print(time, robots, resources)
        time -= 1
        _robots = robots[:]
        _resources = resources[:]
        # build ore robot
        if target == 0 and resources[0] >= costs[0]:
            _robots[0] += 1
            _resources[0] -= costs[0]
            for _target in range(4):
                build(time, _target, costs, _robots, _resources, max_geodes = max(max_geodes, resources[-1]))
        # build clay robot
        elif target == 1 and resources[0] >= costs[1]:
            _robots[1] += 1
            _resources[0] -= costs[1]
            for _target in range(4):
                build(time, _target, costs, _robots, _resources, max_geodes = max(max_geodes, resources[-1]))
        # build obisidian robot
        elif target == 2 and resources[0] >= costs[2] and resources[1] >= costs[3]:
            _robots[2] += 1
            _resources[0] -= costs[2]
            _resources[1] -= costs[3]
            for _target in range(4):
                build(time, _target, costs, _robots, _resources, max_geodes = max(max_geodes, resources[-1]))
        # build geode reobot
        elif target == 3 and resources[0] >= costs[4] and resources[2] >= costs[5]:
            _robots[3] += 1
            _resources[0] -= costs[4]
            _resources[2] -= costs[5]
            for _target in range(4):
                build(time, _target, costs, _robots, _resources, max_geodes = max(max_geodes, resources[-1]))

    return max_geodes

# blueprint = [ number, 
# ore_robot_ore_cost, clay_robot_ore_cost, 
# obisidian_robot_ore_cost, obisidian_robot_clay_cost
# geode_robot_ore_cost, geode_robot_obisidan_cost ]

geodes = 0
for b in blueprints:
    n = b[0]
    costs = b[1:]
    # ore, clay, obsidian, geode
    # one ore robot to start
    robots = [ 1, 0, 0, 0 ]
    # and no resources
    resources = [ 0, 0, 0, 0 ]
    # start trying to build an ore robot first
    geodes = build(24, 0, costs, robots, resources)
    print(n, geodes)

