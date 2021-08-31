# CS4102 Fall 2019 -- Homework 5
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
# Collaborators: sa2dt, bc5fg
# Sources: Introduction to Algorithms, Cormen
#################################
import math


class SeamCarving:
    def __init__(self):
        return

    def distance(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2+(p2[2]-p1[2])**2)

    def energy_map(self, image):
        row = len(image)
        col = len(image[0])
        e = [[0 for i in range(col)] for j in range(row)]
        for i in range(row):
            for j in range(col):
                if (i == 0 and (j == 0 or j == (col-1))) or (i == (row-1) and (j == 0 or j == (col-1))):
                    if i == 0 and j == 0:
                        for x in range(i, i+2):
                            for y in range(j, j+2):
                                e[i][j] += 1 / 3 * self.distance(image[i][j], image[x][y])
                    elif i == 0 and j == (col-1):
                        for x in range(i, i+2):
                            for y in range(j-1, j+1):
                                e[i][j] += 1 / 3 * self.distance(image[i][j], image[x][y])
                    elif i == (row-1) and j == 0:
                        for x in range(i-1, i+1):
                            for y in range(j, j+2):
                                e[i][j] += 1 / 3 * self.distance(image[i][j], image[x][y])
                    else:
                        for x in range(i-1, i+1):
                            for y in range(j-1, j+1):
                                e[i][j] += 1 / 3 * self.distance(image[i][j], image[x][y])
                elif j == 0 or j == (col-1) or i == 0 or i == (row-1):
                    if j == 0:
                        for x in range(i-1, i+2):
                            for y in range(j, j+2):
                                e[i][j] += 1 / 5 * self.distance(image[i][j], image[x][y])
                    elif j == (col-1):
                        for x in range(i-1, i+2):
                            for y in range(j-1, j+1):
                                e[i][j] += 1 / 5 * self.distance(image[i][j], image[x][y])
                    elif i == 0:
                        for x in range(i, i+2):
                            for y in range(j-1, j+2):
                                e[i][j] += 1 / 5 * self.distance(image[i][j], image[x][y])
                    else:
                        for x in range(i-1, i+1):
                            for y in range(j-1, j+2):
                                e[i][j] += 1 / 5 * self.distance(image[i][j], image[x][y])
                else:
                    for x in range(i-1, i+2):
                        for y in range(j-1, j+2):
                            e[i][j] += 1 / 8 * self.distance(image[i][j], image[x][y])
        return e

    # This method is the one you should implement.  It will be called to perform
    # the seam carving.  You may create any additional data structures as fields
    # in this class or write any additional methods you need.
    # 
    # @return the seam's weight

    def run(self, image):
        #define global seam_list
        global seam_list
        seam_list = [0]

        #base cases for 1x1 image, 1xn image, nx1 image
        if len(image) == 1 or len(image[0]) == 1:
            if len(image) == 1 and len(image[0]) == 1:
                return math.sqrt(image[0][0][0]**2 + image[0][0][1]**2 + image[0][0][2]**2)
            elif len(image[0]) == 1:
                for g in range(len(image)-1):
                    seam_list.append(0)
                sum = self.distance(image[len(image)-1][0], image[len(image)-2][0])
                for w in range(len(image)-2, -1, -1):
                    if w == 0:
                        sum += self.distance(image[w][0], image[w+1][0])
                    else:
                        sum += 1 / 2 * self.distance(image[w][0], image[w-1][0])
                        sum += 1 / 2 * self.distance(image[w][0], image[w+1][0])
                return sum
            else:
                case = [0 for k in range(len(image[0]))]
                for q in range(len(image[0])):
                    if q == 0:
                        case[q] += self.distance(image[0][q], image[0][q+1])
                    elif q == len(image[0])-1:
                        case[q] += self.distance(image[0][q], image[0][q-1])
                    else:
                        case[q] += 1 / 2 * self.distance(image[0][q], image[0][q-1])
                        case[q] += 1 / 2 * self.distance(image[0][q], image[0][q+1])
                mv = case[0]
                index = 0
                for r in range(1, len(case)):
                    if case[r] < mv:
                        mv = case[r]
                        index = r
                seam_list[0] = index
                return mv

        #images
        x = self.energy_map(image)
        row = len(x)
        col = len(x[0])

        #weights
        weight = [[0 for i in range(col)] for j in range(row)]
        for a in range(col):
            weight[row-1][a] = x[row-1][a]
        for r in range(row-2, -1, -1):
            for c in range(col):
                if c == 0:
                    weight[r][c] = min(weight[r+1][c] + x[r][c], weight[r+1][c+1] + x[r][c])
                elif c == col-1:
                    weight[r][c] = min(weight[r+1][c-1] + x[r][c], weight[r+1][c] + x[r][c])
                else:
                    weight[r][c] = min(weight[r+1][c-1] + x[r][c], weight[r+1][c] + x[r][c], weight[r+1][c + 1] + x[r][c])

        # lowest weight
        lowest = math.inf
        index = 0
        for b in range(col):
            if weight[0][b] < lowest:
                lowest = weight[0][b]
                index = b
        seam_list[0] = index

        #seam_list
        for p in range(1, row):
            min_value = math.inf
            min_column = 0
            if seam_list[p-1] == 0:
                for y in range(0, 2):
                    if weight[p][seam_list[p-1]+y] < min_value:
                        min_value = weight[p][seam_list[p-1]+y]
                        min_column = seam_list[p-1] + y
            elif seam_list[p-1] == col-1:
                for y in range(-1, 1):
                    if weight[p][seam_list[p-1]+y] < min_value:
                        min_value = weight[p][seam_list[p-1]+y]
                        min_column = seam_list[p-1] + y
            else:
                for y in range(-1, 2):
                    if weight[p][seam_list[p-1]+y] < min_value:
                        min_value = weight[p][seam_list[p-1]+y]
                        min_column = seam_list[p-1] + y
            seam_list.append(min_column)
        return lowest

    # Get the seam, in order from top to bottom, where the top-left corner of the
    # image is denoted (0,0).
    # 
    # Since the y-coordinate (row) is determined by the order, only return the x-coordinate
    # 
    # @return the ordered list of x-coordinates (column number) of each pixel in the seam
    #         as an array
    def getSeam(self):
        return seam_list

