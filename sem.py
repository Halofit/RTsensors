
import random
import math
import rips
import cech
import checks

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
            points.append( tuple(map(float, ls)) )
    
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

def equidistant_points(num_points):
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

def vr_example():
    S = generate_points(100)
    rips.vr_search(S, 0.3, save_plot = True)


def cech_example():
    S = generate_points(100)
    cech.cech_search(S, 0.5, save_plot = True)

def eq_example():
    S = equidistant_points(50)
    rips.vr_search(S, 0.28, save_plot = True)

def main():
    #vr_example()
    eq_example()

if __name__ == "__main__":
    main()