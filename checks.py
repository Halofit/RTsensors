from SimplicialComplex import SimplicialComplex


def is_connected(DV):
    simpComplex = SimplicialComplex(DV.values())
    betty_0 = simpComplex.betti_number(0)

    return betty_0 == 1


def is_sphere(CX, DV):
    euler = 0
    for dim in CX:
        euler += len(CX[dim])* ((-1)**dim )

        
    #TODO : we need to check the first betty number as well apparently (according to assistant)
    simpComplex = SimplicialComplex(DV.values())
    betty_1 = simpComplex.betti_number(1)
    print(betty_1)

    return betty_1 == 0 and euler == 2
