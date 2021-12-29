
import networkx as nx
from itertools import product
import requestGenerator as gr
from timeit import default_timer as timer
import random

SOURCE = 0
TAIL_NODE = 0
TARGET = 1
HEAD_NODE = 1




def get_cartesian_product(rel_type_and_ua_sets):
        relations = []
        for ea_tuple in rel_type_and_ua_sets:
            relation_type, ua_sets = ea_tuple
            edge_and_nodes = {}
            edge_and_nodes[relation_type] = [edge for edge in product(ua_sets[TAIL_NODE], ua_sets[HEAD_NODE]) 
                                    if edge[TAIL_NODE] != edge[HEAD_NODE]]
            relations.append(edge_and_nodes)
        return relations
 

def generate_relations(request, ua_sets):
    ua_1 = ua_sets[0]
    ua_2 = ua_sets[1]
    ua_3 = ua_sets[2]
    ua_4 = ua_sets[3]
    possible_relations = []


    #1. assignment of source user to an element of ua_set ua_1
    if ua_1:
        relations = get_cartesian_product([('assign', [[request[SOURCE]], ua_1])])
        possible_relations.append(relations)


    #2. assignment of elements of ua_2 to ua_1
    if ua_1 and ua_2:
        relations = get_cartesian_product([('assign', [ua_2, ua_1])])
        possible_relations.append(relations)



    #3. assignments from source to an element of ua_3 and ua_3 to ua_1
    if ua_1 and ua_3:
        relations = get_cartesian_product([('assign', [[request[SOURCE]], ua_3]),('assign', [ua_3, ua_1])])
        possible_relations.append(relations)


    #4. associations from ua_2 to ua_4
    if ua_2 and ua_4:
        #ua_2 = ua_2 - ua_4
        relations = get_cartesian_product([('assoc', [ua_2, ua_4])])
        possible_relations.append(relations)


    #5. assign source to ua_3 and assoc from ua_3 to ua_4
    if ua_3 and ua_4:
        relations = get_cartesian_product([('assign', [[request[SOURCE]], ua_3]), ('assoc', [ua_3, ua_4])])
        possible_relations.append(relations)

    #6. assign ua_2 to ua_3 and assoc from ua_3 to ua_4
    if ua_2 and ua_3 and ua_4:
        relations = get_cartesian_product([('assign', [ua_2, ua_3]), ('assoc', [ua_3, ua_4])])
        possible_relations.append(relations)

    #7. assogn source to ua_3, ua_2 to ua_3 and assoc from ua_3 to ua_4
    if ua_2 and ua_3 and ua_4:
        relations = get_cartesian_product([('assign', [[request[SOURCE]], ua_3]), ('assign', [ua_2, ua_3]), ('assoc', [ua_3, ua_4])])
        possible_relations.append(relations)
        
    #8. assign ua_2 to ua_3 and ua_3 to ua_1
    if ua_2 and ua_3 and ua_1:
        relations = get_cartesian_product([('assign', [ua_2, ua_3]), ('assign', [ua_3, ua_1])])
        possible_relations.append(relations)		

    return possible_relations


def find_precondition_assoc(graph, request, assoc_set):

    common_descendants = list(nx.algorithms.dag.descendants(graph, request[SOURCE]) & nx.algorithms.dag.descendants(graph, request[TARGET]) - {'pc'}) + [request[TARGET]]
    precondition_assoc_set = [e for e in assoc_set if e[HEAD_NODE] in common_descendants and request[SOURCE] not in list(nx.algorithms.dag.ancestors(graph, e[TAIL_NODE]))]


    precondition_assoc = random.choice(precondition_assoc_set)

    return precondition_assoc 

def find_ua_set(graph, assoc, request, users):
    #print("request = " + str(request)) # + ", source_target_ref = " + str(source_target_ref))

    ua_sets = []
    #list(nx.algorithms.dag.ancestors(graph, assoc_one[pre_node_index]) - set(users)) + [assoc_one[pre_node_index]] 
    ua_1 = list(nx.algorithms.dag.ancestors(graph, assoc[TAIL_NODE]) - set(users))  + [assoc[TAIL_NODE]]
    #ua_1 = [ a_node for a_node in list(nx.algorithms.dag.ancestors(graph, assoc[TAIL_NODE])) if graph.nodes[a_node]['node_type'] == 'ua'] + [assoc[TAIL_NODE]]
    ua_sets.append(set(ua_1))


    ua_1_descendants = []
    for a_node in ua_1:
        ua_1_descendants += list(nx.algorithms.dag.descendants(graph, a_node))


    ua_2 = list(nx.algorithms.dag.descendants(graph, request[SOURCE]) & nx.algorithms.dag.ancestors(graph, assoc[HEAD_NODE]) - set(ua_1_descendants + ua_1))

    ua_sets.append(set(ua_2))

    ua_2_ancestors = set()
    for a_node in ua_2:
        ua_2_ancestors.update(nx.algorithms.dag.ancestors(graph, a_node))


    ua_3 = list(nx.algorithms.dag.ancestors(graph, assoc[HEAD_NODE]) - ua_2_ancestors - set(ua_1 + ua_2 + list(users) + ua_1_descendants))

    ua_sets.append(set(ua_3))

    ua_4 = list( nx.algorithms.dag.descendants(graph, request[SOURCE]) & nx.algorithms.dag.descendants(graph, request[TARGET]) - {'pc'}) + [request[TARGET]]


    ua_sets.append(set(ua_4))

    return ua_sets

def get_attribute_node_successors(graph, attribute_set):
    list_of_list_of_successors = [list(graph.successors(attribute_node)) for 
                                  attribute_node in attribute_set]
    return [successor_node for sublist in list_of_list_of_successors for successor_node in sublist]

def get_user_attribute_sets(graph, request, user_set, assoc_set, authorization_mode):
    assoc = find_precondition_assoc(graph, request, assoc_set)
    ua_sets = find_ua_set(graph, assoc, request, user_set)
    if authorization_mode["is_generic"]:
        return ua_sets
    ua1, ua2, ua3, ua4 = ua_sets
    if authorization_mode["deny_set"] == "ua2":
        ua2 = set()
        if len(ua3) > authorization_mode["limit_access_to"]:
            ua3 = random.sample(list(ua3), k=authorization_mode["limit_access_to"])
    else:
        ua3 = set()
        if len(ua2) > authorization_mode["limit_access_to"]:
            ua2 = random.sample(list(ua2), k=authorization_mode["limit_access_to"])
    return [ua1, ua2, ua3, ua4]
 



'''
assoc = find_precondition_assoc(graph, a_request, assoc_set)
ua_sets = find_ua_set(graph, assoc, a_request, user_set)
print(ua_sets)
ua1, ua2, ua3, ua4 = ua_sets

#print(get_attribute_node_successors(graph, random.choice(list(ua2))))



relations = generate_relations(a_request, ua_sets) 
print(relations)
'''
