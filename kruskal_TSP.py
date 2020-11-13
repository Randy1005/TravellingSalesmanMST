import sys
import time


class Edge(object):
	def __init__(self, vertices=None, Time=None):
		# vertices: tuple
		# Time: int
		self.vertices = vertices
		self.Time = Time


def childOf(edge, parent):
	if parent == edge[0]:
		return edge[1]
	else:
		return edge[0]


def preorderTraversal(rootNode, edgeSetMST, traversed, TSPRoute):

	if rootNode in traversed:
		return

	TSPRoute.append(rootNode)

	children = []
	for edge in edgeSetMST:
		if rootNode in edge.vertices:
			traversed.append(rootNode)
			children.append(childOf(edge.vertices, rootNode))

	for child in children:
		preorderTraversal(child, edgeSetMST, traversed, TSPRoute)


def findRootCollapsing(subsets, vertex):
	root = vertex
	"""
	find root of vertex:
	subsets[vertex] >= 0 means vertex still belongs to other set
	"""
	while subsets[root] >= 0:
		root = subsets[root]

	"""
	collapsing:
	update parent of vertex to root of that set
	for speeding up when searching for root
	"""
	while vertex != root:
		parent = subsets[vertex]
		subsets[vertex] = root
		vertex = parent

	return root
	

def Union(subsets, vertexA, vertexB):
	ARoot = findRootCollapsing(subsets, vertexA)
	BRoot = findRootCollapsing(subsets, vertexB)

	"""
	when abs(subsets[ARoot]) >= abs(subsets[BRoot]), or subsets[ARoot] <= subsets[BRoot] 
	meaning elements in setA >= elements in setB
	then merge setB into setA, and update root to ARoot
	vice versa
	"""
	if subsets[ARoot] <= subsets[BRoot]:
		subsets[ARoot] += subsets[BRoot]
		subsets[BRoot] = ARoot
	else:
		subsets[BRoot] += subsets[ARoot]
		subsets[ARoot] = BRoot

	return



def kruskalMST(adjMat, subsets, edgeSetMST):

	"""
	edgeTimeSorted: edges sorted by 'Time', 
					ascending order
	"""
	edgeTimeSorted = []

	# obtain the edge objects
	for i in range(len(subsets)):
		for j in range(i):
			if adjMat[i][j] != 0:
				edgeTimeSorted.append(Edge((i, j), adjMat[i][j]))

	# sort edge time in ascending order
	edgeTimeSorted.sort(key=lambda x: x.Time)

	# start selecting edges, starting from the one with minimum time
	for edge in edgeTimeSorted:
		# if no cycle occured
		if findRootCollapsing(subsets, edge.vertices[0]) != findRootCollapsing(subsets, edge.vertices[1]):
			edgeSetMST.append(edge) # store this edge
			Union(subsets, edge.vertices[0], edge.vertices[1]) # union these sets

	return


def main():
	if len(sys.argv) != 3:
		print("please input proper commandline arguments")
		print("usage: python3 kruskal_TSP.py <site_set_filename> <number_of_sites>")

	else:
		""" 
		parameters:	[0]avg_stay_time, [1]rating [2]actual site names
		adjMatrix:	n-dimensional list storing n * n point to point distances
		edgeSetMST: store selected edges
		subsets: '-n' means number of child, 'm' means parent/root
		"""
		params = []
		adjMatrix = []
		edgeSetMST = []
		subsets = []

		# for showing the actual names of sites
		siteNameSet = [
					   "花瓶石", 
					   "美人洞", 
					   "烏鬼洞", 
					   "山豬溝", 
					   "落日亭", 
					   "碧雲寺", 
					   "生態廊", 
					   "白燈塔", 
					   "三民老街",	
					   "觀音石", 
					   "厚石",
					   "中澳",
					   "小綠龜浮潛店"
		]
		

		# input filename & number of sites
		site_set_file = sys.argv[1]
		num_sites = int(sys.argv[2])

		# read in from file
		with open(site_set_file, "r") as f:
			read_str = f.readlines()

		cnt = 0
		for i in read_str:
			tmp_list = i.split() # using white space as delimiter
			tmp_list = list(map(int, tmp_list)) # convert to integers
			if cnt < num_sites:
				adjMatrix.append(tmp_list)
			else:
				params.append(tmp_list)
			cnt += 1
		
		# start time
		startTime = time.clock()

		# initialize subset with -1
		for i in range(num_sites):
			subsets.append(-1)
		
		kruskalMST(adjMatrix, subsets, edgeSetMST)
		
		# obtain root vertex
		root = -1
		for vtx in subsets:
			if vtx < 0:
				root = subsets.index(vtx)

		# preorder MST traversal
		traversed = []
		TSPRoute = []
		preorderTraversal(root, edgeSetMST, traversed, TSPRoute)
		TSPRoute.append(root)

		# end time
		endTime = time.clock()

		# calculate trip total time (with avg. stay time)
		totalTime = 0
		travelTime = 0
		for i in range(len(TSPRoute) - 1):
			totalTime += ((adjMatrix[TSPRoute[i]][TSPRoute[i+1]]) + params[0][TSPRoute[i+1]])
			travelTime += adjMatrix[TSPRoute[i]][TSPRoute[i+1]]


		actualSite = []
		# change to actual name
		for site in TSPRoute:
			actualSite.append(siteNameSet[site])

		# print("edgeSetMST:")
		# print("edges    Time")
		# for edge in edgeSetMST:
		# 	print(edge.vertices, "    ", edge.Time)

		print("\nRoute: ", TSPRoute)
		print("Route(actual sites): ", actualSite)
		print("Travel Time: ", travelTime, "minutes")
		print("Trip Total Time(with average stay time of each site): ", totalTime, "minutes")
		print("Execution Time: ", endTime - startTime, "seconds")



if __name__ == '__main__':
	main()

