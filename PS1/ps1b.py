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
    egg_counts = []
    for egg_weight in egg_weights:
        reduced_weight = target_weight - egg_weight
        if(reduced_weight in memo):
            egg_counts.append(memo[reduced_weight])
        elif reduced_weight >= 0:
            egg_counts.append(dp_make_weight(egg_weights, reduced_weight))
    memo[target_weight]=min(egg_counts)+1
    return min(egg_counts)+1
"""
preoder traversal, depth first
we iterate over the egg_list and withing the iteration we check if the target weight reduced by the current egg_weight is still more than 0
if yes we step into the recursion by calling the function with the reduced weight
that's how we end up with the leftmost node
we step out of the recursion if the reduced weight is the same value as one of the egg_weights, that's when we return 1 because at this point it would only need
one more egg to reach the target weight.
After returning something for the first time we continue with the top element in the call stack which means that we look at the second element in the egg_weight list
Once we looped for the first time over the entire list we look at the elements in the egg_counts list
We select the smalles value because that's the minimum amount of eggs we need to reach the target_weight from the current egg_weight.
To optimize the algorithm we save the minimum amount with the current egg_weight to the memo and return the minimum amount.
We now know the minimum amount of eggs for the bottom most left node. We repeat this process, walking form the bootom left side of the tree back to the root.
While iterating over the list before we step into the recursion we check the memo and see if we already calculated the minimum amount of eggs we need
for the current egg_weight, if we already did it, we saved it to the memo which means that we can look it up and add the min amount to the egg_list and continue in 
the for loop opposed to stepping into the recursion and going to the bottom of the tree again. If we reached the root we looked at the entire left subtree. 
Now we repeat this for all subtrees and receive in the end a list with the most efficient path for each subtree. As always we return the min of the list and 
receive our total min amount of eggs.
"""

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 25, 24, 6)
    print(dp_make_weight(egg_weights, 55))