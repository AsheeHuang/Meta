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
        for i in range(self.city_num) :
            self.pheromone.append([1 for i in range(self.city_num)])
        for i in range(self.city_num) :
            self.pheromone[i][i] = 0
    def init_visibility(self):
         self.visibility = [[0 for i in range(self.city_num)]for j in range(self.city_num)]
         for i in range(self.city_num) :
             for j in range(self.city_num) :
                 if float(distance[i][j]) != 0 :
                    self.visibility[i][j] = 1/float(distance[i][j])
    def ant_go(self,alpha = 1.5,beta = 1.0):
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
            prob = list(filter(lambda a : a != 0 ,prob))
            current_city = choice(remain_city,10,p = prob)[0] #select next city by prob
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
    def run(self,ant_num,repeat_time,persistence_rate=0.7,Q=2000):
        def globle_update(solution):
            count = [[0 for i in range(self.city_num)]for j in range(self.city_num)]
            for i in solution :
                sol = i[0]
                fit = i[1]
                for j in range(1,len(sol)) :
                   u,v = min(sol[j-1],sol[j]), max(sol[j-1],sol[j])
                   count[u][v] += Q/fit
                   #count[v][u] = count[u][v]
            # print_matrix(count)
            # for i in count:
            #     print(i)
            for i in range(self.city_num) :
                for j in range(i,self.city_num):
                    self.pheromone[i][j] = persistence_rate * self.pheromone[i][j] + count[i][j]
                    self.pheromone[j][i] = persistence_rate * self.pheromone[j][i] + count[i][j]


        for i in range(repeat_time) :
            solution = []
            fitness_sum = 0
            print("------------------------------ACO Round",i,"-----------------------------------")
            for j in range(ant_num) :
                sol = self.ant_go()
                fitness = self.fitness(sol)
                fitness_sum += fitness
                solution.append([sol,fitness])
                if fitness < self.best :
                    self.best = fitness
                    self.solution = sol
            globle_update(solution)
            print("Average fitness : ", fitness_sum / ant_num)
            print("Best solution : ",self.best)




def read_data(dir) :
    distance = []
    data = open(dir,'r')
    # append distance data in list
    for i in data:
        line = i.split(" ")
        line = list(filter(None,line))
        line[len(line)-1] = line[len(line)-1].replace('\n',"")
        line = list(map(int,line))
        distance.append(line)

    # for i in distance :
    #     print(i)
    # print(distance[1][3])
    return distance
def print_matrix(matrix):
    for i in matrix :
        for j in i :
            print("%.2f" % j , end = ' ')
        print()

if __name__ == "__main__" :
    distance = read_data("./Bays29.txt")
    # distance = read_data("./test.txt")

    aco = TSP(distance)
    aco.run(100,15,persistence_rate=0.7,Q=200)
    print("Best solution ",aco.best)
    for i in aco.solution :
        print(str(i)+'->', end ='')
    print(aco.solution[0])



