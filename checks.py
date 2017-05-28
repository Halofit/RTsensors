

def is_connected(CX):
    S = CX[0]
    E = CX[1]

    #compute neighbours
    neigh = {}
    for v in S:
        neigh[v] = set()
    for e in E:
        neigh[e[0]].add(e[1])
        neigh[e[1]].add(e[0])
    
    marked = set()

    def dfs_rec(v):
        if v in marked:
            return
        marked.add(v)
        for n in neigh[v]:
            dfs_rec(n)

    dfs_rec(S[0])

    #if we reached all vertices
    #the structure is connected
    return len(marked) == len(set(S))

def is_sphere(CX):
    euler = 0
    for dim in CX:
        euler += len(CX[dim])* ((-1)**dim )

        
    #TODO : we need to check the first betty number as well apparently (according to assistant)
    betty_1 = 0

    return betty_1 == 0 and euler == 2
