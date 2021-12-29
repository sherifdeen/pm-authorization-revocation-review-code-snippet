import networkx as nx
import itertools
import random

TAIL_NODE = 0
HEAD_NODE = 1

def read_rca_graph():
    graph = nx.read_gpickle("../scenario_one_scripts_and_simulations/git_revoke.gpickle")
    return graph

def get_set_of_associations(graph):
    assoc_set = {(u, v) for u, v, keys, weight in graph.edges(data="relation", keys=True) if weight == 'assoc'}
    return assoc_set

def get_set_of_assignments(graph):
    assign_set = {(u, v) for u, v, keys, weight in graph.edges(data="relation", keys=True) if weight == 'assoc'}
    return assign_set

def get_set_of_users(graph):
    users = {node for node in graph.nodes() if graph.nodes[node].get("node_type", None) != None
         and graph.nodes[node]['node_type'] == 'u'}
    return users

def  get_revocation_requests(graph, association_set, users_set):
    """from each association find authorized users and target policy elements"""
    authorized_users = []
    target_pe = []
    revocation_requests = []
    
    for association in association_set:
        user_in_assoc_tail_node_ascenstors = nx.algorithms.dag.ancestors(graph, association[TAIL_NODE]) & users_set
        assoc_head_node_ascenstors =  nx.algorithms.dag.ancestors(graph, association[HEAD_NODE])
        
        if user_in_assoc_tail_node_ascenstors and assoc_head_node_ascenstors:
            authorized_users.append(user_in_assoc_tail_node_ascenstors)
            target_pe.append(assoc_head_node_ascenstors)
            
    """get an authorized user to revoke access to a target policy element """
    for i in range(len(authorized_users)):
        priv_users = list(authorized_users[i])
        """ensure priviledged user is not the target resource"""
        resources = list(target_pe[i] - authorized_users[i] & target_pe[i])
        
        if resources:
            revocation_requests.append(list(itertools.product(priv_users,resources)))
            #revocation_requests.append((random.choice(priv_users), random.choice(resources))) 
    return [request for sublist in revocation_requests for request in sublist]     

def get_constrain_authorization_requests(graph, association_set, users_set):
    """find unauthorized users for each associations"""
    users = []
    resources = []
    authorization_requests = []
    for association in association_set:
        user_in_assoc_tail = nx.algorithms.dag.ancestors(graph, association[TAIL_NODE]) & users_set
        user_in_assochead = nx.algorithms.dag.ancestors(graph, association[HEAD_NODE]) & users_set
        target_resources =  nx.algorithms.dag.ancestors(graph, association[HEAD_NODE])
        
        users_seeking_access = user_in_assochead - user_in_assoc_tail 
        if users_seeking_access and target_resources:
            users.append(users_seeking_access)
            resources.append(target_resources)

    """create a tuple of user and resource to request access on"""
    for i in range(len(users)):
        requestor = users[i]
        target = list(resources[i] - requestor)
        if target:
            authorization_requests.append(list(itertools.product(list(requestor),target)))
            #authorization_requests.append((requestor, random.choice(target))) 
    return [request for sublist in authorization_requests for request in sublist]        
    


def get_sets_of_requests(generated_requests, sizes, number_of_requests_per_size= 200):
    requests_of_sizes = []
    requests_of_a_size = []
    #sizes = [1, 5, 500, 1000]
    for size in sizes:
        for i in range(number_of_requests_per_size):
            if size < len(generated_requests):
                requests_of_a_size.append(random.sample(generated_requests, size))
            else:
                requests_of_a_size.append(random.choices(generated_requests, k=size))
        requests_of_sizes.append(requests_of_a_size)
        requests_of_a_size = []
        
    return requests_of_sizes             
    

graph = read_rca_graph()
user_set = get_set_of_users(graph)
assoc_set = get_set_of_associations(graph)
revocation_requests = get_revocation_requests(graph, assoc_set,user_set)

authorization_requests = get_constrain_authorization_requests(graph, assoc_set, user_set)
#print("graph from pickle = " + str(graph.adj))
#print("association = " + str(assoc_set))
#print("auth_users = " + str(revocation_requests))
#print("authorization = " + str(authorization_requests))

#print("auth_users = " + str(revocation_requests))


