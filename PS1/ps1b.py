###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================


# Problem 1
memo = {}
def dp_make_weight(egg_weights, target_weight):
    if target_weight in egg_weights:
        return 1
    egg_list = []
    for egg in egg_weights:
        new_weight = target_weight - egg
        if new_weight in memo:
            egg_list.append(memo[new_weight])
        elif new_weight >= 0:
            egg_list.append(dp_make_weight(egg_weights, new_weight))
    min_count = min(egg_list) + 1
    memo[target_weight] = min_count
    return min_count

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    egg_weights2 = (1, 3, 2)
    n2 = 10
    n = 99
    # print("Egg weights = (1, 5, 10, 25)")
    # print("n = 99")
    # print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print(dp_make_weight(egg_weights2, n2))
    #print(test(4))