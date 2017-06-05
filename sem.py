
import random
import math
import rips
import cech
import checks
import collections

#reads points from file
def read_points(filename):
    f = open(filename, 'r')

    d = f.read()
    d = d.replace("},{", "\n")
    d = d.replace("}", "")
    d = d.replace("{", "")

    points = []

    for line in d.split("\n"):
        ls = line.split(",")
        if len(ls) == 3:
            points.append(tuple(map(float, ls)))
    
    return points

def generate_points(num_points)	:
    points = []
    
    for i in range(0, num_points):
        phi = random.uniform(-math.pi, math.pi)
        theta = random.uniform(0, 2*math.pi)
        x = math.sin(theta) * math.cos(phi)
        y = math.sin(theta) * math.sin(phi)
        z = math.cos(theta)
        points.append((x,y,z))
        
    return points

def optimal_points(num_points):
    print("Generating points")
    S = generate_points(num_points)

    start_e = 0.5
    forces = {}

    for i in range(0,5000):
        e = 0.5 * start_e + (start_e) * (2/(i+1))
        newS = []
        for v in S:
            f = (0,0,0)
            for u in S:
                if u != v:
                    diff = (u[0]-v[0], u[1]-v[1], u[2]-v[2])
                    ab = diff[0]**2 + diff[1]**2 + diff[2]**2

                    f = (f[0] - e*(diff[0]/ab),
                         f[1] - e*(diff[1]/ab),
                         f[2] - e*(diff[2]/ab))

            v = (v[0] + f[0], v[1] + f[1], v[2] + f[2])
            
            #normalise
            norm = math.sqrt( v[0]**2 + v[1]**2 + v[2]**2 )
            v = (v[0]/norm, v[1]/norm, v[2]/norm)

            newS.append(v)


        #forces were applied
        S = newS
    print("Points generated")
    return S

def rips_example():
    S = generate_points(100)
    rips.vr_search(S, 0.3, save_plot = True)


def cech_example():
    S = generate_points(100)
    cech.cech_search(S, 0.5, save_plot = True)

def opti_example():
    S = optimal_points(50)
    rips.vr_search(S, 0.28, save_plot = True)

def reduce_example():
    S = read_points("data/sensors02.txt");
    result = cech.cech_search(S, 0.2, save_plot = True)

    CX = result[1]
    DV = result[2]

    final_CX, final_DV = remove_redundant(CX, DV)

    EG = [(final_DV[e[0]], final_DV[e[1]]) for e in final_CX[1]]
    S = final_DV.values()
    rips.plot(S, EG) #, save_name="cechFinal", file_format="png")


def is_inside(center, point, radius):
    return ((point[0] - center[0])**2 + (point[1] - center[1])**2 + (point[2] - center[2])**2 < radius**2)

def remove_redundant(CX, DV):

    points_to_remove = [];

    for i in range(3, len(CX)):

        CXi = CX[i];
        for sx in CXi:
            simplex = {DV[v] for v in sx}
            boundry = cech.mb(simplex, [])
            for v2 in sx:
                if is_inside(boundry[0], DV[v2], math.sqrt(boundry[1])):
                    if v2 not in points_to_remove:
                        #print(str(DV[v2])+" index: " + str(v2))
                        points_to_remove.append(v2)

        for j in range(0,len(points_to_remove)):
            new_DV = DV.copy();
            new_DV.pop(points_to_remove[j]);
            new_CX = collections.defaultdict(list)

            for key, sxlist in CX.iteritems():
                for sx in sxlist:
                    if points_to_remove[j] not in sx:
                        new_CX[key].append(sx)

            if checks.is_connected_old(new_CX) and checks.is_sphere(new_CX, new_DV):
                print("Redundant sensor: " + str(DV[points_to_remove[j]]) + " at index" + str(points_to_remove[j]))
                CX = new_CX
                DV = new_DV
                points_to_remove.pop(j);
                break;

    return CX, DV


def main():
    #vr_example()
    #eq_example()
    reduce_example()
    opti_example()

if __name__ == "__main__":
    main()