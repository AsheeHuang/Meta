from random import randrange
from numpy.random import choice
class TSP :
    solution = []
    distance = []
    pheromone = []
    visibility = []
    city_num = 0
    best = 9999999999
    def __init__(self,distance):
        self.distance = distance
        self.city_num = len(distance)
        self.init_pheromone()
        self.init_visibility()
    def init_pheromone(self):
        self.pheromone=[]
        for i in range(self.city_num) :
            self.pheromone.append([1 for i in range(self.city_num)])
        for i in range(self.city_num) :
            self.pheromone[i][i] = 0
    def init_visibility(self):
         self.visibility = [[0 for i in range(self.city_num)]for j in range(self.city_num)]
         for i in range(self.city_num) :
             for j in range(i+1,self.city_num) :
                 if float(distance[i][j]) != 0 :
                    self.visibility[i][j] = 1/float(distance[i][j])
                    self.visibility[j][i] = self.visibility[i][j]
    def ant_go(self,alpha = 1.0,beta = 1.0):
        def calculate_prob(current_city,remain_city) :
            prob = [0 for i in range(self.city_num)]
            total = 0
            for i in remain_city :
                total += pow(self.pheromone[current_city][i],alpha)*pow(self.visibility[current_city][i],beta)
            for i in remain_city :
                # print(pow(self.pheromone[current_city][i],alpha)*pow(self.visibility[current_city][i],beta),total)
                prob[i] =pow(self.pheromone[current_city][i],alpha)*pow(self.visibility[current_city][i],beta)/total
            return  prob
        solution = []
        remain_city = [i for i in range(self.city_num)] #city is not traversed yet
        current_city = remain_city.pop(randrange(len(remain_city)))  #randomly select a city as first city
        solution.append(current_city)
        # print(current_city)
        # print(remain_city)

        while(remain_city):
            prob = calculate_prob(current_city,remain_city)
            prob = list(filter(lambda a : a != 0 ,prob)) #delete all "0" in prob so that length of prob and city will be the same
            current_city = choice(remain_city,1,p = prob)[0] #select next city by prob
            remain_city.remove(current_city)
            solution.append(current_city) #append city in solution
        #print("Path : ",solution)
        # solution.append(solution[0]) #back to start point
        return solution
    def fitness(self,solution):
        sum = 0
        for i in range(1,len(solution)) :
            sum += distance[solution[i-1]][solution[i]]
        sum += distance[solution[-1]][solution[0]] #back to start point
        return sum
    def run(self,ant_num,repeat_time,alpha,beta,persistence_rate=0.7,Q=2000):
        def globle_update(solution):
            acc_pheromone = [[0 for i in range(self.city_num)]for j in range(self.city_num)]
            for i in solution :
                sol = i[0]
                fit = i[1]
                for j in range(1,len(sol)) :
                   u,v = min(sol[j-1],sol[j]), max(sol[j-1],sol[j])
                   acc_pheromone[u][v] += Q/fit
                   #count[v][u] = count[u][v]
            # print_matrix(count)
            # for i in count:
            #     print(i)
            for i in range(self.city_num) :
                for j in range(i,self.city_num):
                    self.pheromone[i][j] = persistence_rate * self.pheromone[i][j] + acc_pheromone[i][j]
                    self.pheromone[j][i] = persistence_rate * self.pheromone[j][i] + acc_pheromone[i][j]

        counter = 0
        for i in range(repeat_time) :
            solution = []
            fitness_sum = 0
            # print("------------------------------ACO Round",i,"-----------------------------------")
            for j in range(ant_num) :
                sol = self.ant_go(alpha=alpha,beta=beta)
                fitness = self.fitness(sol)
                fitness_sum += fitness
                solution.append([sol,fitness])
                if fitness < self.best :
                    counter =0
                    self.best = fitness
                    self.solution = sol
            counter += 1
            if counter > 100 :
                break

            globle_update(solution)
            # print("Average fitness : ", fitness_sum / ant_num)
            # print("Best solution : ",self.best)
def read_data(dir) :
    def dist(city1_x,city2_x,city1_y,city2_y) :
        return pow(pow(city1_x-city2_x,2)+pow(city1_y-city2_y,2),0.5)
    distance = []
    data = open(dir,'r')
    lines = data.readlines()
    data = open(dir, 'r')
    if len(lines[0].split(' ')) == 1 : # if the first line is number of city
        city_num = int(lines[0])
        citys = [[] for i in range(city_num+1)]
        # append distance data in list
        for i in range(1,city_num+1) :
            citys[i] = lines[i].split(' ')
            citys[i][2] = citys[i][2].replace('\n','')
            citys[i] = list(map(float,citys[i]))
        citys.pop(0)
        for i in range(city_num) :
            line = []
            for j in range(city_num) :
                line.append(dist(citys[i][1],citys[j][1],citys[i][2],citys[j][2]))
            distance.append(line)
    else:
        for i in data:
            line = i.split(" ")
            line = list(filter(None,line))
            line[len(line)-1] = line[len(line)-1].replace('\n',"")
            line = list(map(int,line))
            distance.append(line)
    return distance
def print_matrix(matrix):
    for i in matrix :
        for j in i :
            print("%.2f" % j , end = ' ')
        print()

if __name__ == "__main__" :
    # distance = read_data("./Bays29.txt")
    # distance = read_data("./St70.txt")
    # distance = read_data("./Berlin52.txt")
    # distance = read_data("./Eil51.txt")
    # distance = read_data("./Eil76.txt")
    # distance = read_data("./Oliver30.txt")
    # distance = read_data("./Pr76.txt")

    dir = ["./Bays29.txt","./St70.txt","./Berlin52.txt","./Eil51.txt","./Eil76.txt","./Oliver30.txt","./Pr76.txt"]

    for d in dir :
        distance = read_data(d) #read data

        aco = TSP(distance)
        aco.run(ant_num=20,repeat_time=50,alpha=1.0,beta=2.0,persistence_rate=0.8,Q=200)
        print("---------------------%s--------------------" % d)
        print("Best solution ",aco.best)
        for i in aco.solution :
            print(str(i)+'->', end ='')
        print(aco.solution[0])
        print()