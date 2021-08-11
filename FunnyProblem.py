import numpy as np
from scipy.sparse.csgraph import breadth_first_order
import math
from scipy.sparse import csr_matrix

def path_augmenting_function(short_path, res_graph): #Function to return the residual graph
    
    initial = 1
    
    edge_cap_weight = 1 #Since capacity of each edge is 1
    
    while initial < len(short_path): #Iterate through the length of each shortest path
    
        first = short_path[initial - 1]
        
        last = short_path[initial]
        
        res_graph[first][last] = res_graph[first][last] - edge_cap_weight #Make this edge 0
        
        res_graph[last][first] = res_graph[last][first] + edge_cap_weight #Make this edge 1
        
        initial = initial + 1
        
    return res_graph #Return the residual graph after augmenting
    
def max_flow_cal(bfsG): #Function that returns maximum flow value and shortest paths
    
    flow_cal = 0   #initialize the flow calculated to zero
    
    super_source = 0

    super_sink = pow(gridsize,2)*2 + 1
    
    different_paths = []  #list to store shortest paths
    
    nodes, predecessor = breadth_first_order(csr_matrix(bfsG), 0, directed=True, return_predecessors=True) #Findout nodes and predecessor by using BFS for the graph
    
    shortest_path = obtain_path(super_sink, predecessor) #takes shortest path obtained from obtain_path function
    
    different_paths.append(shortest_path) # add the shortest path obtained from the above graph
    
    while super_source in shortest_path: #Iterate till we have source in the shortest path
    
        edge_cap_weight = 1 #Since capacity of each edge is 1
        
        flow_cal = flow_cal + edge_cap_weight
        
        bfsG = path_augmenting_function(shortest_path,bfsG) #residual graph returned from path_augmenting_function
        
        nodes, predecessor = breadth_first_order(csr_matrix(bfsG), 0, directed=True, return_predecessors=True) #Findout nodes and predecessor for the residual graph
        
        shortest_path = obtain_path(super_sink, predecessor) # obtain shortest path from residual graph using nodes and predecessor
        
        different_paths.append(shortest_path) # add all the shortest paths after augmenting.
        
    return flow_cal, different_paths  #returns both maximum flow and all the shortest paths with nodes 
    
def obtain_path(sink,predecessor_array): #Function to return shortest path or vertex disjoint path in terms of nodes 

    temporary = [sink]  #list to store nodes 
    
    temp_rev = []
    
    while predecessor_array[sink] != -9999: #Iterates to findout the nodes that were found in the breadth-first search 
    
        temporary.append(predecessor_array[sink]) #adds those nodes to the list
        
        sink = predecessor_array[sink]
        
        temp_rev = temporary[::-1] #Since they are in reverse order we reverse them again to get the actual path
        
    return temp_rev

def funny_problem(first_points):  #Function to return maximum flow and vertices in vertex-disjoint paths
    
    mid_value = pow(gridsize,2)
    
    split_vertices = pow(gridsize,2)*2
    
    nodes_count = split_vertices + 2  #Total number of nodes 
    
    convert_to_graph = np.zeros((nodes_count, nodes_count), dtype=np.int64)#initializing graph with all zeros
    
    for point in first_points:  # For making the value of edges from super source to Vin 1
    
        convert_to_graph[0][(point[0] - 1) * 2 * gridsize + (2 * (point[1] - 1)) + 1] = 1

    loops = 1
    
    while loops < split_vertices:       # For making the value of Vin, Vout edge to 1
    
        convert_to_graph[loops][loops + 1] = 1
        
        loops = loops + 2
    
    split_it = 2
        
    while split_it < (split_vertices + 1) :  # iterating through the loop to set all the edge values of neighbours for each vertex in all the four directions to 1
    
        if split_it % (2 * gridsize) != 0:    #For the ones on right side
        
            convert_to_graph[split_it][split_it + 1] = 1
            
        if (split_it - 2) % (2 * gridsize) != 0:   #For the ones on left side
        
            convert_to_graph[split_it][split_it - 3] = 1
            
        if split_it - (2 * gridsize) > 0:     #For the ones up
        
            convert_to_graph[split_it][split_it - (2 * gridsize) - 1] = 1
            
        if split_it + (2 * gridsize) < split_vertices + 1:   #For the ones down
        
            convert_to_graph[split_it][split_it + (2 * gridsize) - 1] = 1
            
        split_it = split_it + 2
    
    loops = 0
    
    while loops < gridsize: #For making the edge values from sides to the destination in the grid 1 and the edge values from left to right in the grid to 1
        
        convert_to_graph[2 * gridsize * (loops + 1)][nodes_count - 1] = 1
        
        convert_to_graph[loops * 2 * gridsize + 2][nodes_count - 1] = 1
        
        loops = loops + 1
    
    loops = 1 
    
    while loops < (gridsize + 1): # For making the value of edges from sides of the grid to the destination and value of edges from up to down in the grid 1
        
        convert_to_graph[2 * (gridsize - 1) * gridsize + 2 * loops][nodes_count - 1] = 1
        
        convert_to_graph[2 * loops][nodes_count - 1] = 1
        
        loops = loops + 1

    maximum_flow_value, routes = max_flow_cal(convert_to_graph) #function call to get maximum flow value and shortest path with nodes
    
    vertices = [] #creating a list for storing the vertices 
    
    loopit = 0
    
    while loopit <(len(routes)):   #traversing through all the diferrent paths
    
        vertex = []  
        
        route = routes[loopit]   #tracking each vertex-disjoint path
        
        looper = 1
        while  looper <(len(route)): #traversing through all the nodes in each shortest path
        
            if(looper+1<len(route)): # since we are incrementing j by 2 at the end of the loop, this makes sure that list does not go out of index
            
                vertex.append([math.ceil(route[looper+1]/(2*gridsize)),math.ceil((route[looper]%(2*gridsize))/2)]) # Finding out vertices from nodes
            
            looper = looper + 2  # incrementing looper by 2
            
        vertices.append(vertex) # Add each x and y coordinate to the list of vertices
        
        loopit = loopit + 1  # incrementing loopit by 1
            
    return maximum_flow_value, vertices #return the maximum flow value and vertices 
    
if __name__ == '__main__':

    file_lines = []
    
    start_points = []
    
    file_path = open("SampleTestCases\sample_test_case_1.txt", 'r')     # input file given here
    
    while True:
    
        line = file_path.readline()
        
        file_lines.append(line)
        
        if not line:
        
            break
            
    file_path.close()
    
    gridsize, no_start_vertices = file_lines[0].split(',')  # this step will give us the size nxn and m value 
    
    gridsize = int(gridsize)
    
    no_start_vertices = int(no_start_vertices)
    
    line_look = 0
    
    while line_look < no_start_vertices:        # to traverse all the start vertices in input file
    
        x_coordinate,y_coordinate = file_lines[line_look+1].split(',')
        
        x_coordinate = x_coordinate.replace('(','')
        
        y_coordinate = y_coordinate.replace(')', '')
        
        start_points.append((int(x_coordinate),int(y_coordinate))) # adding each start vertex to a list
        
        line_look+=1
        
    flow_at_last,vertices = funny_problem(start_points) #final maximum flow and list of vertex-disjoint paths from start vertices to the boundary
    
    if not (flow_at_last==len(start_points)):   #condition to figure out if there exists m vertex-disjoint paths or not
    
        print("NO, A SOLUTION DOES NOT EXIST")
            
    else:
        
        print("(i) YES, A SOLUTION EXISTS")
        
        print("(ii) A set of vertex-disjoint paths is:")
        
        travel = 0
        
        while travel < no_start_vertices:           #loop to iterate through different start vertices and print the vertex disjoint paths
                
            print("PATH from ", vertices[travel][0], ':' , end = " ")
                
            print(*vertices[travel], sep = '->')
            
            travel=travel+1
       
