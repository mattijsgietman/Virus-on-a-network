
# Introduction to Complex Systems: Virus on a Network



This project simulates the spread of a virus on a network using the Mesa framework. The simulation models the interaction between nodes in the network, where nodes can be in one of three states: Susceptible, Infected, or Resistant. The simulation also allows for different parameters to be adjusted, such as infectivity, recovery chance, vaccine chance, and resistance chance.

## Features

- **Node States**: Nodes can be in one of three states: Susceptible, Infected, or Resistant.
- **Simulation Parameters**: Various parameters can be adjusted to observe their impact on virus spread:
  - Average Degree (K): The average degree of the network.
  - Recovery Chance: The probability of a node recovering from infection.
  - Vaccine Chance: The probability of a node getting vaccinated.
  - Resistance Chance: The probability of a node developing resistance to the virus.
  - Infectivity: The probability of a node infecting its neighbors.
  - Model Type: The type of the model (SIS or SIR).
  
## Visualization

The simulation provides a visualization of the network and the virus spread using the Mesa visualization modules. Nodes are displayed as circles with different colors representing their states (blue for Susceptible, red for Infected, and yellow for Resistant). Edges between nodes are shown as black lines, with edges leading to infections highlighted in red.


![](Banner.png)

## Setup and Installation

1. Clone the repository:

2. Navigate to the project directory:`cd ICS_Virus_on_a_network`
3. Install the required dependencies: `pip install mesa networkx matplotlib`
4. Run the simulation:`python run.py`
5. Adjust the simulation parameters using the sliders and choice options in the GUI to observe their impact on virus spread.

## Code Structure

- `node.py`: Defines the `Node` class representing individual nodes in the network.
- `model.py`: Defines the `Network` class representing the simulation model.
- `run.py`: Main script to run the simulation and launch the GUI.
- `server.py`: Hosting the server to run the MESA simulation.
- `plot.py`: Providing visualization for the data from a batchrun.
- `readme.md`: Documentation and setup instructions for the project.

## Contributers

@Ramon Olivieira
@David Mostert
@Mattis Gietman
@Julia de Lange
@QuinReef


## License

This project is licensed under the MIT License. See `LICENSE` for more information.
