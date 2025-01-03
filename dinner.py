def find_dislikes(friends: dict)->set[tuple[str]]:
    """Given a dictionary-based adjacency list of String-based nodes,
       returns a set of all edges in the graph (ie. dislikes who can't be invited together).
       
       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A set of edges in the graph represented as tuples
            - An edge should only appear once in the set.
            - Each edge should list node connections in alphabetical order.

       Example
       -------
       >>> friends={'Alice':['Bob'],'Bob':['Alice', 'Eve'],'Eve':['Bob']}
       >>> find_dislikes(friends)
       {('Alice', 'Bob'), ('Bob', 'Eve')}

    """
    ### BEGIN SOLUTION

    returnSet = set()

    for key in friends:
        for friend in friends[key]:
            tempList = []
            tempList.append(friend) 
            tempList.append(key)
            tempList = sorted(tempList)
            returnSet.add(tuple(tempList))

    return returnSet


    ### END SOLUTION

def filter_no_dislikes(friends:dict)->tuple[list[str], dict]:
    '''An optimization that removes friends who are not in any dislikes relationships,
       prior to generating combinations and add them to the invite list.

       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A tuple containing:
            - list of friends not in dislike relations AND 
            - resulting dictionary with these friends removed

       Example
       -------
       >>> friends={'Alice':['Bob'],'Bob':['Alice', 'Eve'],'Cleo':[],'Don':[],'Eve':['Bob']}
       >>> filter_no_dislikes(friends)
       (['Cleo', 'Don'], {'Alice': ['Bob'], 'Bob': ['Alice', 'Eve'], 'Eve': ['Bob']})
    '''
    ### BEGIN SOLUTION

    copy = friends.copy()
    noHate = []
    for key in friends:
        if len(friends[key]) == 0:
            print(noHate)
            noHate.append(key)
            copy.pop(key)
    return (noHate, copy)
        

    ### END SOLUTION

def filter_bad_invites(all_subsets:list, friends:dict)->list[list[str]]:
    '''Removes subsets from all_subsets that contain any pair of friends who
       are in a dislike relationship

       Args:
           all_subsets: a list of all possible friend combinations, each reresented as a list of strings
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A list containing only friend combinations that exclude dislike pairs
      
       Example
       -------
       >>> all_subsets = [[], ['Eve'], ['Bob'], ['Bob', 'Eve'], ['Alice'], ['Alice', 'Eve'], ['Alice', 'Bob'], ['Alice', 'Bob', 'Eve']]
       >>> friends={'Alice':['Bob'],'Bob':['Alice'],'Eve':[]} 
       >>> filter_bad_invites(all_subsets, friends)
       [[], ['Eve'], ['Bob'], ['Bob', 'Eve'], ['Alice'], ['Alice', 'Eve']]
    '''
    ### BEGIN SOLUTION

    dislikeSet = find_dislikes(friends)
    all_subsets_copy = all_subsets.copy()
    deletedList = []
    for relationships in all_subsets:
        for hate in dislikeSet:
            if set(hate).issubset(set(relationships)) and relationships not in deletedList:
                all_subsets_copy.remove(relationships)
                deletedList.append(relationships)
    return all_subsets_copy

    ### END SOLUTION

def invite_to_dinner_optimized(friends:dict)->list[str]:
    '''Finds the combination with the maximum number of guests without storing all subset combinations

       Functions the same as invite_to_dinner_better. However, your solution should not call the 
       function generate_all_subsets. Instead, you should integrate the generation of subsets with the process of
       finding the maximum number of guests so that you can reduce the overall memory footprint of your algorithm.
       
       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A set of friends to invite to dinner which maximizes the number of friends on the list
       
       Example
       -------
       >>> friends={'Alice':['Bob'],'Bob':['Alice', 'Eve'],'Cleo':[],'Don':[],'Eve':['Bob']}
       >>> invite_to_dinner_optimized(friends)
       ['Alice', 'Eve', 'Cleo', 'Don']
    '''
    ### BEGIN SOLUTION

    friend_list = list(friends.keys())
    n = len(friends)
    
    inviteList = []
    counter = 0

    for i in range(2**n):
        num = i  #convert each number in the range to a binary string
        new_subset = []
        for j in range(n): # to_binary_division approach
            if (num % 2 == 1): # 1 indicates the guest is included
                new_subset = [friend_list[n-1-j]] + new_subset 
            num = num // 2
        goodList = filter_bad_invites([new_subset], friends)
        if new_subset in goodList and len(new_subset) > counter:
            counter = len(new_subset)
            inviteList = new_subset
    return inviteList

    ### END SOLUTION


def generate_all_subsets(friends: dict)->list[list[str]]:
    '''Converts each number from 0 to 2^n - 1 into binary and uses the binary representation
       to determine the combination of guests and returns all possible combinations
      
       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A list of all possible subsets of friends to invite, represented as lists of strings
       
       Example
       -------
       >>> friends={'Alice':['Bob'],'Bob':['Alice', 'Eve'],'Eve':['Bob']}
       >>> generate_all_subsets(friends)
       [[], ['Eve'], ['Bob'], ['Bob', 'Eve'], ['Alice'], ['Alice', 'Eve'], ['Alice', 'Bob'], ['Alice', 'Bob', 'Eve']]
    '''
    friend_list = list(friends.keys())
    n = len(friends)
    
    all_subsets = []

    for i in range(2**n):
        num = i  #convert each number in the range to a binary string
        new_subset = []
        for j in range(n): # to_binary_division approach
            if (num % 2 == 1): # 1 indicates the guest is included
                new_subset = [friend_list[n-1-j]] + new_subset 
            num = num // 2
        all_subsets.append(new_subset)

    return all_subsets

def invite_to_dinner_slow(friends: dict)-> list[str]:
    '''Finds the invite combo with the maximum number of guests via the exhaustive approach:
            1. Generate every possible combination of guests
            2. Filter out the combinations that include dislike relationships
            3. Find the combination which give you the maximum number of invites

       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A list of friends to invite to dinner which maximizes the number of friends on the list
       
       Example
       -------
       >>> riends={'Alice':['Bob'],'Bob':['Alice', 'Eve'],'Cleo':[],'Don':[],'Eve':['Bob']}
       >>> invite_to_dinner_slow(friends)
       ['Alice', 'Cleo', 'Don', 'Eve']
    '''
    all_subsets = generate_all_subsets(friends)
    only_good_subsets = filter_bad_invites(all_subsets, friends)

    #find the subset which maximizes number of invites
    invite_list = []
    for i in only_good_subsets:
        if len(i) > len(invite_list):
            invite_list = i

    return invite_list

def invite_to_dinner_better(friends: dict)-> list[str]:
    '''Finds the invite combo with the maximum number of guests
       
       Args:
           friends: dictionary-based adjacency matrix representing friend relations
       
       Returns:
           A list of friends to invite to dinner which maximizes the number of friends on the list
       
       Example
       -------
       >>> friends={'Alice':['Bob'],'Bob':['Alice', 'Eve'],'Cleo':[],'Don':[],'Eve':['Bob']}
       >>> invite_to_dinner_better(friends)
       ['Alice', 'Eve', 'Cleo', 'Don']
    '''
    definite_invites, problem_friends = filter_no_dislikes(friends)
    fewer_subsets = generate_all_subsets(problem_friends) #smaller graph
    only_good_subsets = filter_bad_invites(fewer_subsets, problem_friends)

    #find the subset which maximizes number of invites
    invite_list = []
    for i in only_good_subsets:
        if len(i) > len(invite_list):
            invite_list = i

    #recombine with definite invites in Pythonic fashion
    invite_list += definite_invites

    return invite_list

if __name__ == "__main__":
    friends={
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Cleo':[],
        'Don':[],
        'Eve':['Bob']
    }
    
    print(invite_to_dinner_slow(friends))
    print("-----")
    print(invite_to_dinner_better(friends))
    print("-----")
    print(invite_to_dinner_optimized(friends))
    print("-----")

    
    # friends_2={
    #     'Alice':['Bob'],
    #     'Bob':['Alice', 'Eve'],
    #     'Eve':['Bob']
    # }
    # print(invite_to_dinner_slow(friends_2))
    # print(invite_to_dinner_better(friends_2))
    # print(invite_to_dinner_optimized(friends_2))

    # friends_3={
    #     'Asa':[], 
    #     'Bear':['Cate'],
    #     'Cate':['Bear', 'Dave'],
    #     'Dave':['Cate','Eve'], 
    #     'Eve':['Dave'], 
    #     'Finn':['Ginny', 'Haruki', 'Ivan'], 
    #     'Ginny':['Finn','Haruki'], 
    #     'Haruki':['Ginny', 'Finn'], 
    #     'Ivan':['Finn']
    # }
    # print("__poopybutts__")
    # print(find_dislikes(friends_3))
    # print("__poopybutts__")
    # print(filter_no_dislikes(friends_3))
    # print("__poopy__")
    # print(invite_to_dinner_slow(friends_3))
    # print("__poopy__")
    # print(invite_to_dinner_better(friends_3))
    # print("__poopy__")
    # print(invite_to_dinner_optimized(friends_3))


    
