from utils import PriorityQueue, DisjointSet

def prim(g, s):
    for v in g.vertices:
        v.distance = float('inf')
        v.in_tree = False
    s.come_from = None
    s.distance = 0
    toexplore = PriorityQueue([s], sortkey=lambda v: v.distance)

    while not toexplore.is_empty():
        v = toexplore.popmin()
        v.in_tree = True
        for (w, edgeweight) in v.neighbours:
            if (not w.in_tree) and edgeweight < w.distance:
                w.distance = edgeweight
                w.come_from = v
                if w in toexplore:
                    toexplore.decreasekey(w)
                else:
                    toexplore.push(w)

def kruskal(g):
    tree_edges = []
    partition = DisjointSet()
    for v in g.vertices:
        partition.add_singleton(v)
    edges = sorted(g.edges, key = lambda e: e[2])

    for (u,v,edgeweight) in edges:
        p = partition.get_set_with(u)
        q = partition.get_set_with(v)
        if p != q:
            tree_edges.append((u,v))
            partition.merge(p, q)
    return tree_edges


# # # # Driver Code # # # #

g = UndirectedGraph([('0','2',26), ('0','4',38), ('0','6',58), ('0','7',16),
                     ('1','2',36), ('1','3',29), ('1','5',32), ('1','7',19),
                     ('2','3',17), ('2','6',40), ('2','7',34),
                     ('3','6',52),
                     ('4','5',35), ('4','6',93), ('4','7',37),
                     ('5','7',28)])

G = nx.Graph()
G.add_edges_from([(v1.id, v2.id, {'weight':w}) for v1,v2,w in g.edges])

fig,ax = plt.subplots(figsize=(10,10))
pos = nx.spring_layout(G)
for v1,v2,w in g.edges:
    _w = w / 100
    nx.draw_networkx_edges(G, pos, edgelist=[(v1.id,v2.id)], width=(0.1+0.9*_w)*3, alpha=.5, edge_color=str(1-(0.1+0.9*_w)))

nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue')
nx.draw_networkx_labels(G, pos)

plt.show()


prim(g, g.vertex['2'])

tree_edges = [(v.come_from, v) for v in g.vertices if v.come_from is not None]
', '.join(f'{u}-{v}' for u,v in tree_edges)


tree_edges2 = kruskal(g)
', '.join(f'{u}-{v}' for u,v in tree_edges2)