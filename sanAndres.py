from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

class Car(Agent):
	def __init__(self, model, pos):
		super().__init__(model.next_id(), model)
		self.lastTurn = None
		self.pos = pos 
		self.exactPos = pos
		self.velocity = (0.1, 0)
		self.angle = 0
	def step(self):
		print(self.model.matrix[self.pos[1]][self.pos[0]])
		self.getAngle()
		newPos = (self.exactPos[0]+self.velocity[0], self.exactPos[1]+self.velocity[1])
		self.exactPos = newPos
		self.model.grid.move_agent(self, (int(newPos[0]), int(newPos[1])))

	def getAngle(self):
		print(self.pos, self.lastTurn)
		self.angle = 0
		if self.pos != self.lastTurn:
			if int(self.model.matrix[self.pos[1]][self.pos[0]]) == 3:
				self.lastTurn = self.pos
				self.velocity = (0.1, 0)
				self.angle = -90
			elif int(self.model.matrix[self.pos[1]][self.pos[0]]) == 4:
				self.lastTurn = self.pos
				self.velocity = (0, -0.1)
				self.angle = 90




class City(Model):
	def __init__(self):
		super().__init__()
		self.matrix = []
		self.loadMatrix()
		self.schedule = RandomActivation(self)
		self.grid = MultiGrid(60, 56, torus=False)
		car = Car(self, (23,33))
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