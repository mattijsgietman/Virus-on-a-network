import random

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

from node import Node, State, ModelType

# Class to represent the network model
class Network(Model):

    def __init__(self, K=10, N=500, recovery_chance=0.01, vaccine_chance=0.01, resistance_chance=0.3, infectivity=0.2, num_infected=1, model_type="SIS"):
            # Set the parameters
            self.num_nodes = N # Number of nodes
            self.K = K # Average degree
            self.prob = K / self.num_nodes # Probability of connection
            self.recovery_chance = recovery_chance # Chance of recovery
            self.resistance_chance = resistance_chance #  Chance of resistance
            self.vaccine_chance = vaccine_chance # Chance of vaccine
            self.infectivity = infectivity # Infectivity
            self.model_type = ModelType[model_type] # Model type
            self._steps = 0
            self._time = 0 
            self.running = True 
            self.cutoff = True

            # Determine the indices for the infected nodes
            infected_indices = random.sample(range(self.num_nodes), num_infected)

            # Create the network
            self.G = networkx.binomial_graph(self.num_nodes, self.prob) # Create a random graph
            self.grid = NetworkGrid(self.G) # Create a grid
            self.schedule = SimultaneousActivation(self) # Create a schedule

            # Create the nodes
            for i in range(self.num_nodes):
                node = Node(i, self, infectivity=self.infectivity)

                # If the node is infected, set the state to infected
                if i in infected_indices:
                    node.state = State.INFECTED

                self.grid.place_agent(node, i)
                self.schedule.add(node)

            # Create the data collector
            self.datacollector = DataCollector(model_reporters={"Percentage Infected": 'perc_infected', "Percentage Susceptible": 'perc_susceptible',
                                                                "Total Infected": 'num_infected', "Total Susceptible": 'num_susceptible', 
                                                                "Total Resistant": 'num_resistant', "Percentage Resistant": 'perc_resistant',})    
            # Collect the data
            self.datacollector.collect(self)

    # Properties to get the average degree
    @property
    def avg_degree(self):
        return 2 * self.G.number_of_edges() / self.num_nodes
    
    # Properties to get the number of infected,
    @property
    def num_infected(self):
        return sum([1 for i in self.grid.get_all_cell_contents() if i.state == State.INFECTED])

    # Properties to get the number of susceptible nodes   
    @property
    def num_susceptible(self):
        return sum([1 for i in self.grid.get_all_cell_contents() if i.state == State.SUSCEPTIBLE])
    
    # Properties to get the percentage of infected nodes
    @property
    def perc_infected(self):
        return self.num_infected / self.num_nodes
    
    # Properties to get the percentage of susceptible nodes
    @property
    def perc_susceptible(self):
        return self.num_susceptible / self.num_nodes
    
    # Properties to get the percentage of resistant nodes
    @property
    def perc_resistant(self):
        return sum([1 for i in self.grid.get_all_cell_contents() if i.state == State.RESISTANT]) / self.num_nodes
    
    # Properties to get the number of resistant nodes
    @property
    def num_resistant(self):
        return sum([1 for i in self.grid.get_all_cell_contents() if i.state == State.RESISTANT])
    
    # Function to step through the model
    def step(self):
        self.schedule.step() # Step through the schedule
        self.datacollector.collect(self) # Collect the data
        if self.perc_infected >= 0.9 and self.cutoff:
            # Stop the model if the percentage of infected nodes is greater than 90%
            self.running = False
    
    def plot(self):
        # Plot the network
        fig,ax= plt.subplots(1,1,figsize=(16,10))
        cmap = ListedColormap(["lightblue", "orange", "green",]) 
        graph = self.G  
        pos = networkx.kamada_kawai_layout(graph) 
        plt.clf()
        ax=fig.add_subplot()
        states = [int(i.state.value) for i in self.grid.get_all_cell_contents()]
        colors = [cmap(i) for i in states]

        networkx.draw(graph, pos, node_size=100, edge_color='gray', node_color=colors,
                alpha=0.9,font_size=14,ax=ax)
        
        plt.show()