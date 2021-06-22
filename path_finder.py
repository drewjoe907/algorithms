from utils import DirectedGraph, PriorityQueue, Stack
import math
import numpy as np

# Depth First Search Algorithm using Stack Data Structure
def dfs(g, s):
    # the first loop iterates over every vertex v: O(V)
    for v in g.vertices:
        v.seen = False

    # initiating the stack costs O(1)
    toexplore = Stack([s])
    # toggling .seen costs O(1)
    s.seen = True
    
    ''' the while test runs for every vertex v that we 
        visit; the .seen flag ensures we visit each 
        vertex atleast once - costs O(V) '''
    while not toexplore.is_empty():
        print(f'toexplore={toexplore}', end=' ... ')
        v = toexplore.popright()
        print(f'visiting {v}')
        for w in v.neighbours:
            if not w.seen:
                print(f'  new neighbour {w}')

                ''' the final .pushright & 
                    .seen toggle are run 
                    for every edge e we
                    visit, there are e
                    edges, so the cost is
                    O(E) '''
                toexplore.pushright(w)
                w.seen = True
            else:
                print(f'  seen neighbour {w}')

''' total runtime of dfs(): O(V + E) '''

# Visit all the vertices in graph g reachable from vertex s
def breadth_first_search(g, s):
    # O(V)
    for v in g.vertices:
        v.seen = False

    # just like depth first on a stack: O(1)
    toexplore = Queue([s])
    s.seen = True
    
    # at most once per vertex: O(V)
    while not toexplore.is_empty():
        v = toexplore.popleft()
        for w in v.neighbours:
            if not w.seen:
                # run for every edge e we visit: O(E)
                toexplore.pushright(w)
                w.seen = True  
''' total run time of breadth_first_search(): O(V + E) '''

# Algorithm which uses Breadth First Search to find & return a shortest path
def bfs_path(g, s, t):
    for v in g.vertices:
        v.seen = False
        v.come_from = None
    s.seen = True
    toexplore = Queue([s])
    
    # Traverse the graph, visiting everything reachable from s
    while not toexplore.is_empty():
        v = toexplore.popleft()
        for w in v.neighbours:
            if not w.seen:
                toexplore.pushright(w)
                w.seen = True
                w.come_from = v

    # Reconstruct the full path from s to t, working backwards
    if t.come_from is None:
        return None
    else:
        path = [t]
        while path[0].come_from != s:
            path.insert(0,s)
            return path 



def dijkstra(g, s):
    for v in g.vertices:
        v.distance = float('inf')
    s.distance = 0
    toexplore = PriorityQueue([s], sortkey = lambda v: v.distance)

    while not toexplore.is_empty():
        v = toexplore.popmin()
        # assert: v.distance is the true shortest distance from s to v
        # assert: v is never put back into toexplore
        for (w,edgecost) in v.neighbours:
            dist_w = v.distance + edgecost
            if dist_w < w.distance:
                w.distance = dist_w
                if w in toexplore:
                    toexplore.decreasekey(w)
                else:
                    toexplore.push(w)

def bellman_ford(g, s):
    for v in g.vertices:
        v.minweight = float("inf")
    s.minweight = 0

    for _ in range(len(g.vertices) - 1):
        # relax all the edges
        for (u, v, c) in g.edges:
            v.minweight = min(u.minweight + c, v.minweight)

            # Assert v.minweight >= true minweight for s to v

    for (u, v, c) in g.edges:
        if u.minweight + c < v.minweight:
            print("Negative Cycle Detected")
            return


def johnson(g):

    # STEP 1. Build an augmented graph, with an extra node s (s is the source), and compute the d_v
    s = '_s'
    augmented = DirectedGraph([(v.id, w.id, c) for v,w,c in g.edges] + [(s, v.id, 0) for v in g.vertices])
    # print(f"the augmented graph looks like this: {augmented.edges} ")

    bellman_ford(augmented, augmented.vertex[s])  # sets v.minweight for every vertex v
    # print(f"d_v[e] = {augmented.vertex['e'].minweight}") # d_v[e] = -3
    
    # STEP 2. Define a helper graph, like the original 
    # but with edge weight u->v given by d_u + w(u->v) - d_v
    # In the helper graph, all edges should have weight >= 0.
    helper = DirectedGraph([(v.id, w.id, augmented.vertex[v.id].minweight + c - augmented.vertex[w.id].minweight)
                         for v,w,c in g.edges])

    # print(f"these are the edges & weights in the helper graph: {helper.edges} ")
    assert min(c for v,w,c in helper.edges) >= 0, "Helper graph should have all edge weights >= 0"
    
    weight_prime = {(u.id,v.id):w for u,v,w in helper.edges}
    # print(f"weight'(d→e) = {weight_prime[('d','e')]}") # weight' (d -> e) = 7

    # STEP 3. Run Disjktra, starting from every vertex in the helper graph, to get a matrix of distances.
    n = len(g.vertices)
    dist = np.full((n,n), np.inf)
    vertex_ids = [v.id for v in g.vertices]
    vi = {vid:i for i,vid in enumerate(sorted(vertex_ids))}

    for vid in vertex_ids:
        dijkstra(helper, helper.vertex[vid])
        for wid in vertex_ids:
            dist[vi[vid], vi[wid]] = helper.vertex[wid].distance

    # STEP 4. Wrap up
    d = np.zeros(n)
    for vid in vertex_ids:
        d[vi[vid]] = augmented.vertex[vid].minweight
    result = dist - d[:,np.newaxis] + d[np.newaxis,:]
    return result






def main():
    g = DirectedGraph([('s','t',2), ('s','v',3), ('t','u',2), ('u','v',1), ('v','t',4)])
    dijkstra(g, g.vertex['s'])
    bellman_ford(g, g.vertex['s'])


    all_to_all_graph = DirectedGraph([('a','b',2), ('a','c',1), ('a','d',3), ('b','c',-2), ('c','e',-1), ('d','c',-2), ('d','e',4)])
    johnson_result = johnson(all_to_all_graph)


    for v in g.vertices:
        print(f"distance by dijkstras from s to {v} is {v.distance}")
        pass

    for v in g.vertices:
        print(f"distance by bellman_ford from s to {v} is {v.minweight} ")
        pass
    
    print(f"the result of johnson's algorithm on the all_to_all_graph is {johnson_result} ")

if __name__ == "__main__":
    main()