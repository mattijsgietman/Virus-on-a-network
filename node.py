from enum import Enum
import random

class State(Enum):
    # Define the states of the nodes
    SUSCEPTIBLE = 0
    INFECTED = 1
    RESISTANT = 2

class ModelType(Enum):
    # Define the model types
    SIS = 0
    SIR = 1

# Define the Node class
class Node():
    def __init__(self, pos, model, infectivity=0.3, state:State=State.SUSCEPTIBLE):
        # Initialize the node
        self.state = state # Set the state of the node
        self.pos = pos # Set the position of the node
        self.model = model # Set the model
        self.infectivity = infectivity # Set the infectivity of the node
        self.next_state = State.SUSCEPTIBLE # Set the next state of the node

    # Property to retrieve the neighbours of the node
    @property
    def neighbours(self):
        return self.model.grid.get_neighbors(self.pos, include_center=False)
    
    # Function to step through the model
    def step(self):
        # Enter if the node is susceptible
        if self.state == State.SUSCEPTIBLE: 
            # Loop through the neighbours
            for neighbour in self.neighbours:
                # Check if the neighbour is infected
                if neighbour.state == State.INFECTED:
                    # Check if the neighbour infects the node
                    if neighbour.infectivity > random.random():
                        # Set the next state of the node to infected
                        self.next_state = State.INFECTED
                        break
        # Enter if the node is infected            
        elif self.state == State.INFECTED:
            # Check if the node recovers
            if self.model.recovery_chance > random.random():
                # Set the next state of the node to susceptible if the model is SIS
                if self.model.model_type == ModelType.SIS:
                    self.next_state = State.SUSCEPTIBLE
                    return
                else:
                    # Set the next state of the node to resistant if the model is SIR
                    if self.model.resistance_chance > random.random():
                        self.next_state = State.RESISTANT
                        return
                self.next_state = State.SUSCEPTIBLE
                return
            else:
                # Set the next state of the node to resistant if it does not fall into the above conditions
                self.next_state = State.INFECTED
                return

        # Enter if the model is SIR
        if self.model.model_type == ModelType.SIR:
            # Check if the node is susceptible
            if self.state == State.SUSCEPTIBLE:
                # Check if the node is resistant
                if self.model.vaccine_chance > random.random():
                    # Set the next state of the node to resistant if the node gets vaccinated
                    self.next_state = State.RESISTANT
            
    # Function to advance the node
    def advance(self):
        # Set the state of the node to the next state
        self.state = self.next_state
        