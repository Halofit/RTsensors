import itertools
import rips
import checks

def dist_sq(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]
    return dx**2 + dy**2 + dz**2

    
def explicit(R): 
    R = list(R)
    if len(R) > 3:
        #return ((0,0,0), 1) # -> four poits determine sphere
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
        z1 = R[0][2]
        z2 = R[1][2]
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
    vr,dic = rips.VR(S, epsilon)
    c = {}
        
    for dim in vr:
        if dim < 2:
            c[dim] = vr[dim]
        else:
            c[dim] = []
            for sx in vr[dim]:
                P = {dic[v] for v in sx}

                B = mb(P, [])
                if B[1] <= epsilon**2:
                    c[dim].append(sx)
                else:
                    #print("Reject: {}, Ball: {}, eps: {}".format(P, B, epsilon**2))
                    pass
    return c, dic



def cech_search(S, r_start, num_iter = 100, save_plot = False):
    minimum_change = 1e-5

    #find first working solution
    best_solution = None
    best_solution_dictionary = None
    r_max = r_start
    r_min = 0
    while best_solution == None:
        print(r_max)
        CX,DV = Cech(S, r_max)

        if checks.is_sphere(CX, DV):
            best_solution = CX
            best_solution_dictionary = DV
        else :
            r_min = r_max
            r_max = r_max*1.5

    if save_plot:
        EG = [ (DV[e[0]], DV[e[1]]) for e in CX[1]]
        rips.plot(S,EG, save_name = "cech0", file_format="png")

    for i in range(0, num_iter):
        r_curr = (r_max + r_min)/2 #pick middle point
        
        CX, DV = Cech(S, r_curr)

        if checks.is_sphere(CX, DV):
            best_solution = CX
            best_solution_dictionary = DV
            r_max = r_curr

            if save_plot:
                EG = [ (DV[e[0]], DV[e[1]]) for e in CX[1]]
                rips.plot(S,EG, save_name = "cech" + str(i), file_format="png")
        else :
            r_min = r_curr
        
        print(i, r_curr, checks.is_sphere(CX))

        #exit early if there is very little wiggle room left
        if (r_max - r_min) < minimum_change:
            break
    
    return r_max, best_solution, best_solution_dictionary