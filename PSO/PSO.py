from random import random

class PSO :
    GBest = 0
    def __init__(self,particle_num,dimension_num,ub,lb) :
        self.particle_num = particle_num
        self.dimension_num = dimension_num
        self.ub = ub
        self.lb = lb

        self.pBestFitness = [999999999999 for i in range(particle_num)]
        self.pBestPos = [[0 for i in range(dimension_num)] for j in range(particle_num)]
        self.pos = [[0 for i in range(dimension_num)] for j in range(particle_num)]
        self.velocity = [[0 for i in range(dimension_num)] for j in range(particle_num)]

        self.maxSpeed = (self.ub - self.lb) *0.01
        self.init_particle()
        self.pBestFitness = self.calFitness(self.pos)
        self.GBest = self.findMin(self.pBestFitness)

        print(self.GBest)
    def init_particle(self) :
        for i in range(self.particle_num) :
            for j in range(self.dimension_num) :
                self.pos[i][j] = random() * (self.ub-self.lb) + self.lb
                self.velocity[i][j] = random() * (self.maxSpeed * 2) - self.maxSpeed
            # print(self.velocity[i])
    def calFitness(self,pos) :
        fitness = [9999999999999 for i in range(self.particle_num)]
        for i in range(self.particle_num) :
            sum = 0
            for j in range(self.dimension_num) :
                sum += pow(pos[i][j],2)
            fitness[i] = sum
            if fitness[i] < self.pBestFitness[i] :
                self.pBestFitness[i] = fitness[i]
                self.pBestPos[i] = pos[i]
            if fitness[i] < self.pBestFitness[self.GBest] :
                self.GBest = i
                self.pBestPos[i] = pos[i]
        return fitness
    def move_particle(self,repeat_time) :
        count = 0
        while(count < repeat_time) :
            for i in range(self.particle_num) :
                self.calFitness(self.pos)
                for j in range(self.dimension_num):
                    self.pos[i][j] = 0.7298*self.velocity[i][j] + (1.496 * random() * (self.pBestPos[i][j]-self.pos[i][j]))+ (1.496 * random() * (self.pBestPos[i][j]-self.pos[i][j]))
                    self.velocity[i][j] = self.velocity[i][j] + (1.496 * random() * (self.pBestPos[i][j]-self.pos[i][j]))+ (1.496 * random() * (self.pBestPos[i][j]-self.pos[i][j]))
                    if self.velocity[i][j] > self.maxSpeed :
                        self.velocity[i][j] = self.maxSpeed
                    if self.pos[i][j] > self.ub :
                        self.pos[i][j] = self.ub
                    if self.pos[i][j] <self.lb :
                        self.pos[i][j] = self.lb
                    count += 1

    def findMin(self,fitness):
        min = 999999999999
        index = -1
        for i in range(len(fitness)) :
            if min > fitness[i] :
                min = fitness[i]
                index = i
        return index

if __name__ == '__main__' :
    pso = PSO(30,30,100,-100)
    print(pso.pBestFitness)
    pso.move_particle(6000)
    print(pso.pBestFitness)
    print(pso.pBestPos[pso.GBest])
    print("Fitness : ", pso.pBestFitness[pso.GBest])
