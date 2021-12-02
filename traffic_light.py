from mesa import Agent

class TrafficLight(Agent):
    RED = False
    GREEN = True
    def __init__(self, model, pos):
      super().__init__(model.next_id(), model)
      # True: Verde
      # False: Rojo
      self.pos = pos
      self.state = TrafficLight.GREEN
      self.clock = 35
    
    def step(self):
      self.clock -= 1

      if self.clock == 0:
        self.clock = 35
        self.state = not self.state
