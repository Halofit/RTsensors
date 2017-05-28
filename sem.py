
import random
import math
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
        

def main():
    S = generate_points(100)
    print("Computing VRcx")
    VRcx, DV = cech.VR(S,0.2)


    print("Plotting")
    DViv = {v:k for k,v in DV.items()}#invert DV
    EG = [ (DViv[e[0]], DViv[e[1]]) for e in VRcx[1]]
    cech.plot(S, EG)
    

if __name__ == "__main__":
    main()