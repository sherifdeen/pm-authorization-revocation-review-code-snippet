import networkx as nx
import itertools
import requestGenerator as gr
from timeit import default_timer as timer
#from generateRequests import HEAD_NODE, TAIL_NODE, get_set_of_associations

SOURCE = 0
TAIL_NODE = 0
TARGET = 1
HEAD_NODE = 1


def is_revocation_request(graph, request):
    association_set = gr.get_set_of_associations(graph)
    for association in association_set:
        tail_ancestors = nx.algorithms.dag.ancestors(graph, association[TAIL_NODE])
        head_ancestors = nx.algorithms.dag.ancestors(graph, association[HEAD_NODE])
        if request[SOURCE] in tail_ancestors and request[TARGET] in head_ancestors:
            return True, association
        
def can_revoke_by_delete_user_assignment(graph, request):
    revocation_approaches = []
    if graph.out_degree(request[SOURCE]) > 1:
        source_nbrs = set(graph.neighbors(request[SOURCE]))
        for node in source_nbrs:
            if node in nx.algorithms.ancestors(graph, request[TARGET]):
                revocation_approaches.append(("deleteAssign", (request[SOURCE], node)))
    return revocation_approaches

def can_revoke_by_delete_attribute_assignment(graph, request):
    revocation_approaches = []
    path_from_source_to_target = nx.algorithms.dag.descendants(
        graph, request[SOURCE]) & nx.algorithms.dag.ancestors(graph, request[TARGET])
    
    pe_neighbors = dict()
    for  pe in path_from_source_to_target:
        if graph.out_degree(pe) > 1:
            pe_neighbors[pe] = set(graph.neighbors(pe))
            #print(pe_neighbors)
            
    for key, value in pe_neighbors.items():
        for node in value:
            if node in nx.algorithms.ancestors(graph,request[TARGET]) and graph.in_degree(node) == 1:
                revocation_approaches.append(("deleteAssign", (key, node)))
    
    return revocation_approaches
            
def can_revoke_by_delete_association(graph, request):
    revocation_approaches = []  
    assoc_set = gr.get_set_of_associations(graph) 
    for association in assoc_set:
        if request[SOURCE] in nx.algorithms.ancestors(
            graph, association[TAIL_NODE]) and request[TARGET] in nx.algorithms.ancestors(
                graph, association[HEAD_NODE]):
                revocation_approaches.append(("deleteAssoc", association))
    
    return revocation_approaches 

def get_cartisian_pdt_of_relations(multiple_list):
    result = []
    for item in itertools.product(*multiple_list):
        result.append(list(item))
    return result


def get_all_revocation_approaches(graph, request):
    possible_revocation_approaches = []
    can_delete_user_assign = can_revoke_by_delete_user_assignment(graph, request)
    can_delete_attribute_assign = can_revoke_by_delete_attribute_assignment(graph, request)
    can_delete_association = can_revoke_by_delete_association(graph, request)
    
    if can_delete_user_assign:
        possible_revocation_approaches.append(can_delete_user_assign)
    if can_delete_attribute_assign:
        possible_revocation_approaches.append(can_delete_attribute_assign) 
    if can_delete_association:
        possible_revocation_approaches.append(can_delete_association)
    if can_delete_user_assign and can_delete_attribute_assign:
        possible_revocation_approaches.append(
            get_cartisian_pdt_of_relations(
                [can_delete_user_assign, can_delete_attribute_assign]
                )
            ) 
    if can_delete_user_assign and can_delete_association:
        possible_revocation_approaches.append(
            get_cartisian_pdt_of_relations(
                [can_delete_user_assign, can_delete_association]
                )
            )
    if can_delete_attribute_assign and can_delete_association:
        possible_revocation_approaches.append(
            get_cartisian_pdt_of_relations(
                [can_delete_attribute_assign, can_delete_association]
                )
            )
    if can_delete_user_assign and can_delete_attribute_assign and can_delete_association:
        possible_revocation_approaches.append(
           get_cartisian_pdt_of_relations(
               [can_delete_user_assign, can_delete_attribute_assign, can_delete_association]
               )
        )
    
    return possible_revocation_approaches
        



'''
counter = 0
for a_list_of_requests in list_of_lists_of_requests:
    if counter % 5 == 0:
        print("Request size of {0}".format(len(a_list_of_requests)))
    for a_tuple_of_request in a_list_of_requests:
        print(len(get_all_revocation_approaches(graph, a_tuple_of_request)))
    counter += 1

for request in revocation_requests:
    ok, association = is_revocation_request(graph, request)
    print("ok = " + str(ok) + " association = " + str(association) + "request = " + str(request))
    if ok:
        print(get_all_revocation_approaches(graph, request))
'''