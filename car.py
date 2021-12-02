from mesa import Agent

class Car(Agent):
	def __init__(self, model, pos, vel):
		super().__init__(model.next_id(), model)
		self.lastTurn = None
		self.pos = pos 
		self.exactPos = pos
		self.lastVelocity = vel
		self.velocity = vel
		self.angle = 0
		self.flag = False
		self.direction = False
		
	def step(self):
		# print(self.model.matrix[self.pos[1]][self.pos[0]])
		self.getAngle()
		# print(self.model.grid.get_neighborhood(self.pos, moore=False))
		newPos = (self.exactPos[0]+self.velocity[0], self.exactPos[1]+self.velocity[1])
		# print(newPos, self.exactPos)
		nextAgents = self.model.grid.get_cell_list_contents([(newPos[0], newPos[1])])
		# print(self.velocity, self.lastVelocity)
		if len(nextAgents) > 0 and nextAgents[0].pos != self.pos:
			if nextAgents[0].velocity == (0, 0):
				self.velocity = (0, 0)
		else:
			# TODO: Delay
			# print(self.velocity, self.lastVelocity)
			self.velocity = self.lastVelocity
			self.model.grid.move_agent(self, (int(newPos[0]), int(newPos[1])))
			self.exactPos = newPos


	# regresa el peso de la posición en la matriz
	def getWeight(self, pos):
		return int(self.model.matrix[pos[1]][pos[0]])


	def turn(self, weight1, weight2):
		# se revisan los vecinos y de acuerdo a la forma de la vuelta se cambia la velocidad

		# print(self.pos, self.)

		neighbors = self.model.grid.get_neighborhood(self.pos, moore=False)
		if self.getWeight(neighbors[0]) == weight1 and self.getWeight(neighbors[1]) == weight2:
			# arriba hacia izquierda
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
				self.angle = -90
			else:
				self.velocity = (0, -1)
				self.angle = 90
		elif self.getWeight(neighbors[2]) == weight1 and self.getWeight(neighbors[0]) == weight2:
			# derecha hacia arriba
			if self.velocity[0] == 0:
				self.velocity = (-1, 0)
				self.angle = 90
			else:
				self.velocity = (0, 1)
				self.angle = -90
		elif self.getWeight(neighbors[1]) == weight1 and self.getWeight(neighbors[3]) == weight2:
			# izquierda hacia abajo
			if self.velocity[0] == 0:
				self.velocity = (1, 0)
				self.angle = 90
			else:
				self.velocity = (0, -1)
				self.angle = -90
			
		elif self.getWeight(neighbors[3]) == weight1 and self.getWeight(neighbors[2]) == weight2:
			# abajo hacia derecha
			if self.velocity[0] == 0:
				self.velocity = (1, 0)
				self.angle = -90
			else:
				self.velocity = (0, 1)
				self.angle = 90

	def getAngle(self):
		self.angle = 0
		# sólo se cambia el ángulo si no se ha pasado antes por dicha posición	
		# print(self.lastVelocity, self.velocity, self.pos)
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

		# TODO: checar semaforo
		elif self.getWeight(self.pos) == 4:
			
			trafficLight = self.model.grid.get_cell_list_contents([(0, 0)])[0]
			
			# luz verde
			if trafficLight.state:
				# vuelta
				if self.random.random()*100 > 50:
					if self.getWeight(self.lastTurn) == 1:
						self.direction = True
					else:
						self.direction = False
					self.flag = True
				
				if self.velocity == (0, 0):
					self.velocity = self.lastVelocity
	
			else:
				self.velocity = (0, 0)

		elif self.getWeight(self.pos) == 5:
			
			trafficLight = self.model.grid.get_cell_list_contents([(0, 0)])[0]
			
			# print(self.lastTurn)
			# luz verde
			if not trafficLight.state:
				# vuelta
				if self.random.random()*100 > 50:
					if self.getWeight(self.lastTurn) == 1:
						self.direction = True
					else:
						self.direction = False
					self.flag = True
				
				if self.velocity == (0, 0):
					self.velocity = self.lastVelocity
	
			else:
				self.velocity = (0, 0)

		elif self.getWeight(self.pos) == 6 and self.flag:


			# get neighbors
			neighbors = self.model.grid.get_neighborhood(self.pos, moore=False)
			weight = 4

			# get last weight
			for neighbor in neighbors:
				if self.getWeight(neighbor) == 4:
					weight = 4
				elif self.getWeight(neighbor) == 5:
					weight = 5

			if self.direction:
				self.turn(weight, 1)
			else:
				self.turn(weight, 2)
			
			self.flag = False

		if not self.getWeight(self.pos) in [4, 5]:
			self.lastTurn = self.pos
		if self.velocity != (0, 0):
			# print(self.velocity, self.lastVelocity)
			self.lastVelocity = self.velocity