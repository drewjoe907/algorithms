from utils import DirectedGraph

def toposort(g):
    for v in g.vertices:
        v.visited = False
        # v.colour = white
    totalorder = []
    for v in g.vertices:
        if not v.visited:
            visit(v, totalorder, prefix='')
    return totalorder

# The prefix argument isn't necessary for the algorithm,
# but it helps print out a nice (rotated) flame chart.

def visit(v, totalorder, prefix):
    print(f"{prefix}{v}-start")
    v.visited = True
    # v.colour = grey
    for w in v.neighbours:
        if not w.visited:
            visit(w, totalorder, prefix+'| ')
    print(f"{prefix}{v}-end")
    totalorder.insert(0, v)
    # v.colour = black

# # # # Driver Code # # # #
g = DirectedGraph([('a','b'), ('a','c'),
                   ('c','d'), ('c','f'),
                   ('d','b'), ('d','e'), ('d','g'),
                   ('h','f'), ('h','i'),
                   ('i','g')])
totalorder = toposort(g)
print("\nOrder:", ','.join(str(s) for s in totalorder))