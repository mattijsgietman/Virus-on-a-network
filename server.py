from network import Network
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import NetworkModule
from mesa.visualization.UserParam import Slider, Choice

from node import State

# Define the portrayal of the network
def network_portrayal(G):
    portrayal = dict() # Create a dictionary to hold the portrayal of the network
    # Define the colors for the different states
    c_map = {State.SUSCEPTIBLE: 'blue', State.INFECTED: 'red', State.RESISTANT: 'Yellow'}
    
    # Create a list to hold the nodes
    portrayal['nodes'] = [{'id': n_id,
                           'size': 8,
                           'color': c_map[n['agent'][0].state],
                           }
                          for n_id, n in G.nodes(data=True)]
    
    # Get the infected nodes
    infected_nodes = [n_id for n_id, n in G.nodes(data=True) if n['agent'][0].state == State.INFECTED]
    
    # Create a list to hold the edges
    portrayal['edges'] = [{'id': i,
                           'source': source,
                           'target': target,
                           'color': 'black',
                           'width': 0.1,
                           }
                          for i, (source, target, _) in enumerate(G.edges(data=True))]

    # Highlight the edges that result in infections with red lines
    for edge in portrayal['edges']:
        if edge['source'] in infected_nodes and edge['target'] not in infected_nodes:
            edge['color'] = 'red'
            edge['width'] = 1.5  # increase the width of the edge to make it more prominent

    return portrayal

# Define the modules to be displayed
network = NetworkModule(network_portrayal, 1000, 1000)

# Define the charts to be displayed
perc_inf_vs_perc_sus = ChartModule([{"Label": "Percentage Infected", "Color": "Red"},
                        {"Label": "Percentage Susceptible", "Color": "Blue"},
                        {"Label": "Percentage Resistant", "Color": "Yellow"}], data_collector_name='datacollector')
inf_vs_sus = ChartModule([{"Label": "Total Infected", "Color": "Red"},
                           {"Label": "Total Susceptible", "Color": "Blue"},
                           {"Label": "Total Resistant", "Color": "Yellow"}], data_collector_name='datacollector')

# Define the parameters that can be adjusted in the model
model_params = {
    "N": Slider("Number of Nodes (N)", 500, 1, 1000, 1),
    "K": Slider("Average Degree (K)", 10, 1, 100, 1),
    "recovery_chance": Slider("Recovery Chance", 0.01, 0, 1, 0.01),
    "vaccine_chance": Slider("Vaccine Chance", 0.01, 0, 1, 0.01),
    "resistance_chance": Slider("Resistance Chance", 0.3, 0, 1, 0.01),
    "num_infected": Slider("Initial Number of Infected", 1, 1, 100, 1),
    "infectivity": Slider("Infectivity", 0.3, 0, 1, 0.01),
    "model_type": Choice("Model Type", value="SIS", choices=["SIS", "SIR"])
}

# Create the server
server = ModularServer(Network,
                       [perc_inf_vs_perc_sus, inf_vs_sus, network],
                       "Network Model", model_params=model_params)