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

	def turnRight(self):
		# se revisan los vecinos y de acuerdo a la forma de la vuelta se cambia la velocidad
		neighbors = self.model.grid.get_neighborhood(self.pos, moore=False)
		if self.getWeight(neighbors[0]) == 1 and self.getWeight(neighbors[1]) == 1:
			# derecha hacia abajo
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
			else:
				self.velocity = (0, 1)
		elif self.getWeight(neighbors[0]) == 1 and self.getWeight(neighbors[2]) == 1:
			# abajo hacia izquierda
			
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
			else:
				self.velocity = (0, 1)
		elif self.getWeight(neighbors[3]) == 1 and self.getWeight(neighbors[1]) == 1:
			# arriba hacia derecha

			if self.velocity[0] == 0:
				self.velocity = (1, 0)
			else:
				self.velocity = (0, 1)
		elif self.getWeight(neighbors[3]) == 1 and self.getWeight(neighbors[2]) == 1:
			# izquierda a arriba
			if self.velocity[0] == 0:
				self.velocity = (1, 0)
			else:
				self.velocity = (0, 1)

	def turnLeft(self):
		# se revisan los vecinos y de acuerdo a la forma de la vuelta se cambia la velocidad
		# TODO: Corregir vueltas a la derecha

		neighbors = self.model.grid.get_neighborhood(self.pos, moore=False)
		if (self.getWeight(neighbors[0]) == 2 and self.getWeight(neighbors[1]) == 2) or (self.getWeight(neighbors[0]) == 1 and self.getWeight(neighbors[1]) == 1):
			# arriba hacia izquierda
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
			else:
				self.velocity = (0, 1)
		elif self.getWeight(neighbors[0]) == 2 and self.getWeight(neighbors[2]) == 2:
			# derecha hacia arriba
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
			else:
				self.velocity = (0, 1)
		elif self.getWeight(neighbors[3]) == 2 and self.getWeight(neighbors[1]) == 2:
			# izquierda hacia abajo
			if self.velocity[0] == 0:
				self.velocity = (1, 0)
			else:
				self.velocity = (0, -1)
			
		elif self.getWeight(neighbors[3]) == 2 and self.getWeight(neighbors[2]) == 2:
			# abajo hacia derecha
			if self.velocity[0] == 0:
				
				self.velocity = (1, 0)
			else:
				self.velocity = (0, 1)

	def getAngle(self):
		self.angle = 0
		# sólo se cambia el ángulo si no se ha pasado antes por dicha posición	
		if int(self.model.matrix[self.pos[1]][self.pos[0]]) == 3:
			# chequeo de carril
			if self.getWeight(self.lastTurn) == 1:
				self.turnRight()
			else:
				self.turnLeft()
			self.lastTurn = self.pos
			#giro
			self.angle = 90
		# checar semaforo
		elif int(self.model.matrix[self.pos[1]][self.pos[0]]) == 4:
			
			if random()*100 > 50:
				self.lastTurn = self.pos
				if self.getWeight(self.pos) == 1:
					self.turnRight()
				else:
					self.turnLeft()
				self.angle = 90


		self.lastTurn = self.pos




class City(Model):
	def __init__(self):
		super().__init__()
		self.matrix = []
		self.loadMatrix()
		self.schedule = RandomActivation(self)
		self.grid = MultiGrid(60, 57, torus=False)
		car = Car(self, (23,33))
		# car = Car(self, (10,1))
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