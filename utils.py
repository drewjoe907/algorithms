import heapq, collections

### Graphs, vertices, edges
# This `DirectedGraph` class uses the adjacency list representation: a list of vertices, and each
# vertex contains a list of its neighbours. This code also uses some cunning Python tricks...

# * We define a class `DirectedGraph`. We also define another class `Vertex`, within
# `DirectedGraph`. Every Python name lives somewhere. If
# there has to be a class `Vertex`, it has to belong somewhere, and if (as in this case)
# we don't expect that other functions will create new `Vertex` objects, it makes sense
# to put it inside `DirectedGraph`. Python doesn't have access modifiers like public or
# private, and other code can still refer to it as `DirectedGraph.Vertex`; Python's
# attitude is "we're all adults here".

# * The function name `__init__` denotes the constructor. The first argument is the object
# that is in the process of being constructed.

# * Another magic function is `__str__`. This function is invoked whenever you call `print(g)`.
# It's helpful for debugging to print out something informative.

# * I want to allow vertices to have custom attributes, e.g. breadth first search uses `v.seen`,
# Dijkstra's algorithm uses `v.distance`. Python allows 'monkey patching', i.e. adding attributes
# to an object after it has been created. You don't need to declare all member variables
# in advance. Internally, Python sees each object as just an arbitrary dictionary. There is a
# convention that one should declare all member variables in the constructor, but this is only for
# readabilty, not a requirement of the language.

# * This class distinguishes between vertex ids and vertex objects. Vertex ids are passed in when the
# graph is created, e.g. `DirectedGraph([('a','b'), ('b','c'), ('b','a')])`, where `a` etc. are vertex
# ids. Then, `Vertex` objects are created, one for each vertex id, and it is those objects which
# have neighbours and other attributes like `seen` or `distance`.

# * For some graphs we want to store e.g. a weight for each edge. For other graphs, there is nothing
# to store. This class permits either. The special syntax `*label` means 0 or 1 or more values.

class DirectedGraph:
    '''A directed graph, where edges is a list of (start_vertex, end_vertex, *label)'''
    def __init__(self, edges):
        src,dst = zip(*[e[:2] for e in edges])
        self.vertex = {k: DirectedGraph.Vertex(k) for k in set(src+dst)}
        for u,v,*label in edges:
            vv = self.vertex[v]
            self.vertex[u].neighbours.append((vv,*label) if len(label)>0 else vv)
        self.vertices = self.vertex.values()
        self.edges = [(self.vertex[u], self.vertex[v], *label) for u,v,*label in edges]

    class Vertex:
        def __init__(self, id_):
            self.id = id_
            self.neighbours = []
        # By providing these two magic methods, vertex objects will print out
        # nicely. Python has a whole list of magic methods that one can override:
        # https://docs.python.org/3/reference/datamodel.html#basic-customization
        def __str__(self):
            return str(self.id)
        def __repr__(self):
            return f"v[{repr(self.id)}]"


class UndirectedGraph(DirectedGraph):
    def __init__(self, edges):
        e1 = set(e[:2] for e in edges)
        e2 = set(e[1::-1] for e in edges)
        if (e1 & e2): raise ValueError("Both directions present")
        edges2 = edges + [(v,u,*a) for u,v,*a in edges]
        super().__init__(edges2)
        self.edges = [(self.vertex[u], self.vertex[v], *label) for u,v,*label in edges]



# The graph algorithms we study make use of a `Queue`, a `Stack`, and a
# `PriorityQueue`. Here they are, as simple interfaces on top of built-in
# Python functions and classes.


# A Python convention is that, if x is a container object like a list or a dequeue, you can test if
# it's non-empty with just "if x". Under the hood, the dequeue class has a built-in function for
# coercing it to a boolean, and whenever you write "if <expr>" it will coerce expr to boolean.
# It would be better Python style to not even include the is_empty() functions here, but I'm
# keeping it to make the pseudocode in notes more understandable.

class Queue(collections.deque):
    def pushright(self, x): self.append(x)
    # popleft is already implemented
    def is_empty(self): return not bool(self)
    def __str__(self): return '['+','.join(str(s) for s in self)+']'

class Stack(collections.deque):
    def pushright(self, x): self.append(x)
    def popright(self): return self.pop()
    def is_empty(self): return not bool(self)
    def __str__(self): return '['+','.join(str(s) for s in self)+']'

# Python has a built-in package heapq, that implements a binary heap and supports push, pop, and heapify.
# It piggy-backs on a regular Python list: it simply provides those methods as free-standing functions,
# not as methods of a class. It does NOT provide decreasekey, so I've implemented it here with a
# nasty hack.

class PriorityQueue:
    def __init__(self, xs, sortkey):
        self.key = sortkey
        self.kxs = [(sortkey(x),i,x) for i,x in enumerate(xs)]
        heapq.heapify(self.kxs)
        self.counter = len(xs)
    def __str__(self):
        return '['+','.join(str(x) for _,_,x in self.kxs)+']'
    def __contains__(self, x):
        return x in (y for _,_,y in self.kxs)
    def is_empty(self):
        return not bool(self.kxs)
    def push(self, x):
        heapq.heappush(self.kxs, (self.key(x), self.counter, x))
        self.counter = self.counter + 1
    def popmin(self):
        try:
            _,_,x = heapq.heappop(self.kxs)
        except IndexError:
            raise IndexError("pop from an empty queue")
        return x
    def decreasekey(self, x):
        k = self.key(x)
        for i,(k2,c2,x2) in enumerate(self.kxs):
            if x2 == x:
                if k2 <= k:
                    raise IndexError(k)
                self.kxs[i] = (k,c2,x)
                heapq.heapify(self.kxs)
                return
        raise KeyError(x)


# This implementation of DisjointSets is given in lecture notes.

class DisjointSet:
    class DSNode:
        def __init__(self, k):
            self.k = k
            self.parent = self
            self.next = None
            self.rank = 1
    def __init__(self, ks=[]):
        self._nodes = {k:DisjointSet.DSNode(k) for k in ks}
    def add_singleton(self, k):
        self._nodes[k] = DisjointSet.DSNode(k)
    def get_set_with(self, k):
        n = self._nodes[k]
        # path compression heuristic
        while n != n.parent:
            n = n.parent
        return n
    def merge(self, n1, n2):
        if n1 == n2:
            return
        # weighted union heuristic
        m1,m2 = (n1,n2) if n1.rank >= n2.rank else (n2,n1)
        m1.rank = m1.rank + m2.rank
        n = m2
        while True:
            n.parent = m1
            if n.next is None:
                n.next = m1.next
                break
            else:
                n = n.next
        m1.next = m2
        m1.parent = m1
    def __iter__(self):
        for v in self._nodes.iteritems():
            yield v
