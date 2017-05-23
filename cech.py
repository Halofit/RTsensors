import itertools

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

    return cliques(VG, EG), DV
    
def explicit(R): 
    R = list(R)
    if len(R) > 3:
        raise Exception("Explicit computation is only implemented for 3 points or less.")
    if len(R) == 3: 
        #barycentric magic:
        a = dist_sq(R[2],R[1])
        b = dist_sq(R[0],R[2])
        c = dist_sq(R[1],R[0])

        alfa = a * (b + c - a) 
        beta = b * (c + a - b) 
        gama = c * (a + b - c) 

        norm = alfa + beta + gama

        alfa = alfa / norm 
        beta = beta / norm 
        gama = gama / norm 

        x0 = alfa*R[0][0] + beta*R[1][0] + gama*R[2][0]
        y0 = alfa*R[0][1] + beta*R[1][1] + gama*R[2][1]
        z0 = alfa*R[0][2] + beta*R[1][2] + gama*R[2][2]
        
        c = (x0,y0,z0)
        return (c, dist_sq(c, R[0]))

    elif len(R) == 2: #two points, diametrically opposed
        x1 = R[0][0]
        x2 = R[1][0]
        y1 = R[0][1]
        y2 = R[1][1]
        y1 = R[0][2]
        y2 = R[1][2]
        c = ( (x1+x2) / 2, (y1+y2) / 2, (z1+z2) / 2 )
        return (c , dist_sq(c, R[0]))
    elif len(R) == 1 :
        return(R[0], 0)
    else:
        raise Exception("Bounding cirlce must contain at least 1 point", R)

def inside(p, Ball):
    return dist_sq(p, Ball[0]) <= Ball[1]

def mb(P,R): #interior points, boundary
    if len(P) == 0 or len(R) == 3 :
        D = explicit(R)
    elif len(P) == 1 and len(R) == 0:
        D = explicit(P)
    else:
        P = set(P)
        p = P.pop()
        D = mb(P, R)
        if not inside(p, D):
            D = mb(P, R + [p])
    return D


def Cech(S, epsilon):
    vr,dic = VR(S, epsilon)
    #print(vr)
    c = {}
    
    dicR = {dic[k]:k for k in dic}
    
    for dim in vr:
        if dim < 2:
            c[dim] = vr[dim]
        else:
            c[dim] = []
            for sx in vr[dim]:
                P = {dicR[v] for v in sx}

                B = mb(P, [])
                if B[1] <= epsilon**2:
                    c[dim].append(sx)
                else:
                    #print("Reject: {}, Ball: {}, eps: {}".format(P, B, epsilon**2))
                    pass
    return c

S = [ (3,7,5) , (8,-10,3), (56,1,4) ]

R = explicit(S)
print(R)

print(dist_sq(R[0], S[0]))
print(dist_sq(R[0], S[1]))
print(dist_sq(R[0], S[2]))