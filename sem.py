
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
		
		
def main():
    pass

if __name__ == "__main__":
    main()