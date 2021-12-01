from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from random import random

class Car(Agent):
	def __init__(self, model, pos):
		super().__init__(model.next_id(), model)
		self.lastTurn = None
		self.pos = pos 
		self.exactPos = pos
		self.velocity = (1, 0)
		self.angle = 0
		self.flag = False
		self.direction = False
		
	def step(self):
		# print(self.model.matrix[self.pos[1]][self.pos[0]])
		self.getAngle()
		# print(self.model.grid.get_neighborhood(self.pos, moore=False))
		newPos = (self.exactPos[0]+self.velocity[0], self.exactPos[1]+self.velocity[1])
		self.exactPos = newPos
		self.model.grid.move_agent(self, (int(newPos[0]), int(newPos[1])))


	# regresa el peso de la posición en la matriz
	def getWeight(self, pos):
		return int(self.model.matrix[pos[1]][pos[0]])


	def turn(self, weight1, weight2):
		# se revisan los vecinos y de acuerdo a la forma de la vuelta se cambia la velocidad


		neighbors = self.model.grid.get_neighborhood(self.pos, moore=False)
		if self.getWeight(neighbors[0]) == weight1 and self.getWeight(neighbors[1]) == weight2:
			# arriba hacia izquierda
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
			else:
				self.velocity = (0, -1)
		elif self.getWeight(neighbors[2]) == weight1 and self.getWeight(neighbors[0]) == weight2:
			# derecha hacia arriba
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
			else:
				self.velocity = (0, 1)
		elif self.getWeight(neighbors[1]) == weight1 and self.getWeight(neighbors[3]) == weight2:
			# izquierda hacia abajo
			if self.velocity[0] == 0:
				self.velocity = (1, 0)
			else:
				self.velocity = (0, -1)
			
		elif self.getWeight(neighbors[3]) == weight1 and self.getWeight(neighbors[2]) == weight2:
			# abajo hacia derecha
			if self.velocity[0] == 0:
				
				self.velocity = (1, 0)
			else:
				self.velocity = (0, 1)

	def getAngle(self):
		self.angle = 0
		# sólo se cambia el ángulo si no se ha pasado antes por dicha posición	
		if self.getWeight(self.pos) == 3:
			# chequeo de carril
			if self.getWeight(self.lastTurn) == 1:
				# print("derecha")
				self.turn(1, 1)
			else:
				# print("izquierda")
				self.turn(2, 2)
			self.lastTurn = self.pos
			#giro
			self.angle = 90
		# TODO: checar semaforo
		elif self.getWeight(self.pos) == 4:
			# print("rotonda")
			if random()*100 > 50:
				# print("vuelta")
				if self.getWeight(self.lastTurn) == 1:
					self.direction = True
				else:
					self.direction = False
				self.flag = True
		elif self.getWeight(self.pos) == 5 and self.flag:
			# print("continua")
			if self.direction:
				self.turn(4, 1)
			else:
				self.turn(4, 2)
			self.angle = 90
			self.flag = False


		self.lastTurn = self.pos




class City(Model):
	def __init__(self):
		super().__init__()
		self.matrix = []
		self.loadMatrix()
		self.schedule = RandomActivation(self)
		self.grid = MultiGrid(60, 57, torus=False)
		
		self.initCars()

	def initCars(self):
		for pos in [(23,33), (10, 1)]:
			car = Car(self, pos)
			self.grid.place_agent(car, car.pos)
			self.schedule.add(car)
		
      
	def step(self):
		self.schedule.step()

	# se carga la matriz con el mapa de la simulación
	def loadMatrix(self):
		f = open("./map.txt", "r")
		for line in f:
			tmp = list(line[0:len(line)-1])
			self.matrix.append(tmp)
		self.matrix = self.matrix[::-1]