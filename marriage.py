# CS4102 Fall 2019 -- Homework 8
#################################
# Collaboration Policy: You are encouraged to collaborate with up to 4 other
# students, but all work submitted must be your own independently written
# solution. List the computing ids of all of your collaborators in the comment
# at the top of your java or python file. Do not seek published or online
# solutions for any assignments. If you use any published or online resources
# (which may not include solutions) when completing this assignment, be sure to
# cite them. Do not submit a solution that you are unable to explain orally to a
# member of the course staff.
#################################
# Your Computing ID: md5jd
# Collaborators: 
# Sources: Introduction to Algorithms, Cormen
#################################
from collections import defaultdict
import networkx as nx


class Marriage:

    lukePath = []
    lorelaiPath = []

    def __init__(self):
        return

    def getLukePath(self):
        return self.lukePath

    def getLorelaiPath(self):
        return self.lorelaiPath

    # This is the method that should set off the computation
    # of marriage.  It takes as input a list lines of input
    # as strings.  You should parse that input and then compute 
    # the shortest paths that both Luke and Lorelai should take.
    # The class fields of lukePath and lorelaiPath should be filled
    # with their respective paths.  The getters above will be called
    # by the grader script.
    #
    # @return the length of the shortest paths (in rooms)
    def compute(self, file_data):
        n = int(file_data[0])
        path1 = file_data[1]
        path2 = file_data[2]
        noadj = [[True for i in range(n)] for j in range(n)]
        node = 0
        begin = defaultdict(list)
        for x in range(3, len(file_data)):
            a = file_data[x].split()
            for i in a:
                i = int(i)
                begin[node].append(i)
            begin[node].append(node)
            node += 1
        for i in range(0, n):
            for w in begin[i]:
                noadj[i][w] = False
        earth2 = nx.Graph()
        for i in range(0, n):
            for j in range(0, n):
                if not noadj[i][j]:
                    continue
                x = str(i) + " " + str(j)
                for lu in begin[i]:
                    for lo in begin[j]:
                        if noadj[lu][lo]:
                            y = str(lu) + " " + str(lo)
                            earth2.add_edge(x, y)
        m, e = path1.split()
        u, z = path2.split()
        start = m + " " + u
        end = e + " " + z
        finale = nx.algorithms.shortest_paths.generic.shortest_path(earth2, start, end)
        length = len(finale)
        for g in range(0, length):
            ke, lai = finale[g].split()
            self.lukePath.append(int(ke))
            self.lorelaiPath.append(int(lai))
        return length
