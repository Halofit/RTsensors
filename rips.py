import itertools
import checks


def plot(S, E, save_name = None, file_format = "pdf"):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    #plot edges
    for e in E:
        plt.plot([e[0][0],e[1][0]], [e[0][1],e[1][1]], [e[0][2],e[1][2]], 'k-')

    #plot points
    for p in S:
        plt.plot([p[0]], [p[1]], [p[2]], 'ro')

    if save_name == None:
        plt.show()
    else:
        plt.savefig("outimg/" + save_name + "." + file_format, bbox_inches='tight')
    plt.close()



def cliques(VG, EG):
    N = {}
    for v in VG:
        N[v] = []
        for e in EG:
            if v == e[0]:
                N[v].append(e[1])
            elif v == e[1]:
                N[v].append(e[0])
    
    C = []
    def BK(R, P, X): #Bron–Kerbosch algorithm
       if len(P) == 0 and len(X) == 0 :
           C.append(tuple(sorted(R)))
       for v in set(P):
           NR = R | set([v])
           NP = P.intersection(N[v])
           NX = X.intersection(N[v])
           BK(NR, NP, NX)
           P.remove(v)
           X.add(v)
    
    BK(set(), set(VG), set())

    C.sort(key=lambda x: -len(x))

    dim = len(C[0]) - 1 #max dim

    R = {}
    while dim >= 0:
        D = set()
        
        for c in C:
            if len(c) == dim+1:
                D.add(c)
        
        if dim+1 in R:
            for s in R[dim+1]:
                D.update(itertools.combinations(s , dim+1))

        R[dim] = list(D)
        dim = dim - 1

    return R

def dist_sq(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]
    return dx**2 + dy**2 + dz**2


def VR(S, epsilon):
    #square the max distance so we work with squared values
    eps = (2*epsilon)**2

    E = []
    for a in S:
        for b in S:
            if a != b and dist_sq(a,b) <= eps:
                E.append( tuple(sorted([a,b])))
    
    DV =  { p: i for i,p in enumerate(S) }
    VG = [DV[p] for p in S]
    EG = [ (DV[e[0]], DV[e[1]]) for e in E]

    final_dictionary =  { v: k for k,v in DV.items() }
    return cliques(VG, EG), final_dictionary


def reduceVR(VR, dic, epsilon):
    eps = (2*epsilon)**2

    edges_to_remove = []
    for e in VR[1]:
        p1 = dic[e[0]]
        p2 = dic[e[1]]

        if dist_sq(p1,p2) > eps:
            edges_to_remove.append(e)
    
    sxs_to_remove = []
    for dim in VR:
        for sx in VR[dim]:
            for e in edges_to_remove:        
                if e[0] in sx and e[1] in sx:
                    sxs_to_remove.append(sx)
    
    for sx in sxs_to_remove:
        dim = len(sx)-1
        VR[dim].remove(sx)
    
    return VR, dic



def vr_search(S, r_start, num_iter = 100, save_plot = False):
    minimum_change = 1e-5

    #find first working solution
    best_solution = None
    best_solution_dictionary = None
    r_max = r_start
    r_min = 0

    while best_solution == None:
        print(r_max)
        CX,DV = VR(S, r_max)

        if checks.is_connected(CX):
            best_solution = CX
            best_solution_dictionary = DV
        else :
            r_min = r_max
            r_max = r_max*1.5

    print("Base r: ", r_max)

    for i in range(0, num_iter):
        r_curr = (r_max + r_min)/2 #pick middle point
        
        #CX, DV = reduceVR(best_solution, best_solution_dictionary, r_curr)
        CX,DV = VR(S, r_curr)

        if checks.is_connected(CX):
            best_solution = CX
            best_solution_dictionary = DV
            r_max = r_curr

            if save_plot:
                EG = [ (DV[e[0]], DV[e[1]]) for e in CX[1]]
                plot(S,EG, save_name = "vr" + str(i), file_format="png")
        else :
            r_min = r_curr
        
        print(i, r_curr, checks.is_connected(CX))



        #exit early if there is very little wiggle room left
        if (r_max - r_min) < minimum_change:
            break
    
    return r_max, best_solution, best_solution_dictionary

