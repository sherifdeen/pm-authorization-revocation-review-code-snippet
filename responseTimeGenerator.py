import networkx as nx
import itertools
import requestGenerator as gr
import revocationGenerator as revgen
import contrainedAuthorizationGenerator as cag
from timeit import default_timer as timer

graph = gr.read_rca_graph()
assoc_set = gr.get_set_of_associations(graph)
user_set = gr.get_set_of_users(graph)
revocation_requests = gr.get_revocation_requests(graph, assoc_set,user_set)
revocation_triple_nested_list = gr.get_sets_of_requests(revocation_requests, [100, 350, 500, 750, 1000], 20)

authorization_requests = gr.get_constrain_authorization_requests(graph, assoc_set, user_set)
authorization_triple_nested_list = gr.get_sets_of_requests(authorization_requests, [100, 350, 500, 750, 1000], 20)

def revocation_response_time(triple_nested_list):
    for double_nested_lists in triple_nested_list:
        count = 0
        start_timer = timer()
        for each_list_of_requests in double_nested_lists:
            for tuple_request in each_list_of_requests:
                result = revgen.get_all_revocation_approaches(graph, tuple_request)
                count+=1
        end_timer = timer()
        #print("length of {0}".format(len(double_nested_lists)))
        print("count = {0}".format(count))
        print("Average timer for request size of {0} = {1}".format(count / len(double_nested_lists),
            (end_timer - start_timer)/len(double_nested_lists)))
        
def authorization_response_time(triple_nested_list):
    authorization_mode = {"is_generic": False, "deny_set": "ua2", "limit_access_to": 1}

    for double_nested_lists in triple_nested_list:
        count = 0
        start_timer = timer()
        for each_list_of_requests in double_nested_lists:
            for tuple_request in each_list_of_requests:
                ua_sets = cag.get_user_attribute_sets(graph, tuple_request, user_set, assoc_set, authorization_mode)
                relations = cag.generate_relations(tuple_request, ua_sets)
                count+=1
        end_timer = timer()
        #print("length of {0}".format(len(double_nested_lists)))
        print("count = {0}".format(count))
        print("Average timer for request size of {0} = {1}".format(count / len(double_nested_lists),
            (end_timer - start_timer)/len(double_nested_lists)))
    
    

print("================== Average Response Time For Access Revocation ==================")
revocation_response_time(revocation_triple_nested_list)

print("================== Average Response Time For Constrained Authorization ==================")
authorization_response_time(authorization_triple_nested_list)