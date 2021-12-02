from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from random import random
from car import Car
from traffic_light import TrafficLight

class City(Model):
	def __init__(self):
		super().__init__()
		self.matrix = []
		self.loadMatrix()
		self.schedule = RandomActivation(self)
		self.grid = MultiGrid(60, 57, torus=False)
		
		self.initCars()
		self.initTrafficLights()

	def initCars(self):
		cars = [
			(16,33),
			(20,33),
			(24,33), 
			(2, 1),
			(6, 1),
			(10, 1), 
			(14,1), 
			(18, 1), 
			(22, 1), 
			(26,1),  
			(30, 1), 
			(20, 12),
			(24, 12),
			(28, 12),
			(32, 12),
			(36, 12),
			(40, 54),
			(44, 54),
			(48, 54),
			(52, 54)
			]
		for pos in cars:
			car = Car(self, pos, (1, 0))
			self.grid.place_agent(car, car.pos)
			self.schedule.add(car)

	def initTrafficLights(self):
		
		trafficLight1 = TrafficLight(self, (0, 0))
		self.grid.place_agent(trafficLight1, trafficLight1.pos)
		self.schedule.add(trafficLight1)
		
      
	def step(self):
		self.schedule.step()

	# se carga la matriz con el mapa de la simulación
	def loadMatrix(self):
		f = open("./map.txt", "r")
		for line in f:
			tmp = list(line[0:len(line)-1])
			self.matrix.append(tmp)
		self.matrix = self.matrix[::-1]