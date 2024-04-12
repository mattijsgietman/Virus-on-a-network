import random
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import ListedColormap
from network import Network
   

random.seed(7)

def plot_grid(model,fig):
    graph = model.network
    pos = nx.spring_layout(graph)  
    plt.clf()
    ax=fig.add_subplot()
    states = [int(i.state.value) for i in model.grid.get_all_cell_contents()]
    colors = [cmap(i) for i in states]

    nx.draw(graph, pos, node_size=100, edge_color='gray', node_color=colors, #with_labels=True,
            alpha=0.9,font_size=14,ax=ax)
    return

#example usage
model = Network()

steps = 10
print(model.perc_infected)

for step in range(steps):
    fig,ax= plt.subplots(1,1,figsize=(16,10))
    f=plot_grid(model,fig)
    plt.show()
    model.step()
    print(model.perc_infected)

