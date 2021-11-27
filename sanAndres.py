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
		print(self.model.matrix[self.pos[1]][self.pos[0]])
		self.getAngle()
		# print(self.model.grid.get_neighborhood(self.pos, moore=False))
		newPos = (self.exactPos[0]+self.velocity[0], self.exactPos[1]+self.velocity[1])
		self.exactPos = newPos
		self.model.grid.move_agent(self, (int(newPos[0]), int(newPos[1])))


	def getWeight(self, pos):
		return int(self.model.matrix[pos[1]][pos[0]])

	def turnRight(self):
		
		neighbors = self.model.grid.get_neighborhood(self.pos, moore=False)
		if self.getWeight(neighbors[0]) == 1 and self.getWeight(neighbors[1]) == 1:
			# derecha hacia abajo
			# print("derecha hacia abajo")
			self.velocity = (0, -1)
		elif self.getWeight(neighbors[0]) == 1 and self.getWeight(neighbors[2]) == 1:
			# abajo hacia izquierda
			# print("abajo hacia izquierda")
			self.velocity = (-1, 0)
		elif self.getWeight(neighbors[3]) == 1 and self.getWeight(neighbors[1]) == 1:
			# arriba hacia derecha
			print("arriba hacia derecha")

			if self.velocity[0] == 0:
				self.velocity = (1, 0)
			else:
				self.velocity = (0, 1)
		elif self.getWeight(neighbors[3]) == 1 and self.getWeight(neighbors[2]) == 1:
			# izquierda a arriba
			# print("izquierda a arriba")
			self.velocity = (0, 1)

	def turnLeft(self):
		# TODO: Corregir vueltas a la derecha	
		neighbors = self.model.grid.get_neighborhood(self.pos, moore=False)
		if self.getWeight(neighbors[0]) == 2 and self.getWeight(neighbors[1]) == 2:
			# arriba hacia izquierda
			# print("derecha hacia abajo")
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
			else:
				self.velocity = (0, 1)
		elif self.getWeight(neighbors[0]) == 2 and self.getWeight(neighbors[2]) == 2:
			# derecha hacia arriba
			# print("abajo hacia izquierda")
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
			else:
				self.velocity = (0, 1)
		elif self.getWeight(neighbors[3]) == 2 and self.getWeight(neighbors[1]) == 2:
			# izquierda hacia abajo
			# print("arriba hacia derecha")
			if self.velocity[0] == 0:
				self.velocity = (1, 0)
			else:
				self.velocity = (0, -1)
			
		elif self.getWeight(neighbors[3]) == 2 and self.getWeight(neighbors[2]) == 2:
			# abajo hacia derecha
			# print("izquierda a arriba")
			if self.velocity[0] == 0:
				
				self.velocity = (1, 0)
			else:
				self.velocity = (0, 1)

	def getAngle(self):
		# print(self.pos, self.lastTurn)
		self.angle = 0
		# print(self.pos)
		if self.pos != self.lastTurn:
			if int(self.model.matrix[self.pos[1]][self.pos[0]]) == 3:
				# print(self.pos)
				# for x in neighbors:
				# 	print(x, self.model.matrix[x[1]][x[0]])
				# print(self.getWeight(neighbors[3]))

				if self.getWeight(self.pos) == 1:
					self.turnRight()
				else:
					self.turnLeft()

				self.lastTurn = self.pos

				self.angle = 90
			elif int(self.model.matrix[self.pos[1]][self.pos[0]]) == 4:
				

				
				if random()*100 > 50:

					self.lastTurn = self.pos

					if self.getWeight(self.pos) == 1:
						self.turnRight()
					else:
						self.turnLeft()

					self.angle = 90




class City(Model):
	def __init__(self):
		super().__init__()
		self.matrix = []
		self.loadMatrix()
		self.schedule = RandomActivation(self)
		self.grid = MultiGrid(60, 57, torus=False)
		car = Car(self, (10,1))
		# car = Car(self, (10,1))
		self.grid.place_agent(car, car.pos)
		self.schedule.add(car)

      
	def step(self):
		self.schedule.step()

	def loadMatrix(self):
		f = open("./map.txt", "r")
		for line in f:
			tmp = list(line[0:len(line)-1])
			self.matrix.append(tmp)
		self.matrix = self.matrix[::-1]