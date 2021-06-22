from utils import DirectedGraph
'''
    start with flow = 0
    while True:
        bfs(g, s, t):
            return augmenting path
        if augmenting_path:
            add as much flow along it as possible
        else:
            break

'''
def ford_fulkerson(g, s, t):
    # let f be a flow, initially empty
    for (u, v, c, f, l) in g.edges:
        f = 0

    def find_augmenting_path():
        # define a residual graph h on the same vertices as g
        h = DirectedGraph([(u.id, v.id, c, f, l) for u,v,c,f,l in g.edges])
        for edge in g.edges:
            if f < c: edge.l = "inc"
            if f > 0: edge.l = "dec"
        while breadth_first():
            if edge.l: path = [] + f
            else: break

    while True:
        p = find_augmenting_path()
        if p is None:
            break # give up - can't find augementing path
        else:
            



        


