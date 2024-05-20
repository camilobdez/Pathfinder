# Shortest and Safest Path Finder

This project aims to provide the shortest and safest path between any two points in a city, specifically designed to prevent street sexual harassment. The algorithm uses a combination of distance and risk factors to determine the optimal route, ensuring users can travel quickly and safely.

## Features
- **Shortest Path Calculation**: Uses Dijkstra's algorithm to find the shortest path.
- **Safety Consideration**: Incorporates a risk factor based on harassment data.
- **Data-Driven**: Utilizes real data from Open Street Maps and local surveys to calculate risks.

## Data Sources
- Open Street Maps (OSM)
- Medellín Quality of Life Survey (2017)
- Crime and harassment data from local authorities

## Methodology
1. **Data Collection and Processing**:
    - The map of Medellín was obtained from Open Street Maps and processed using the Python API `OSMnx`.
    - The risk of harassment was calculated as a linear combination of various socio-economic factors obtained from the Medellín Quality of Life Survey.

2. **Algorithm**:
    - A graph was created using the processed data, where edges represent streets with weights considering both distance and harassment risk.
    - Dijkstra's algorithm was employed to find the shortest path while minimizing the risk of harassment.

3. **Path Calculation**:
    - Three different paths were calculated, each balancing distance and risk differently.
    - Users can choose a path based on their preference for safety or travel time.

## Usage
### Prerequisites
- Python 3.x
- Required libraries: `networkx`, `matplotlib`, `geopandas`, `osmnx`

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/camilobdez/pathfinder.git
    cd parthfinder
    ```
2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Project
1. Prepare the dataset and place it in the appropriate directory.
2. Run the main script:
    ```sh
    python main.py
    ```
3. Input the coordinates of the start and end points when prompted.

### Example
To find the shortest and safest path between EAFIT University and the National University:
1. Ensure the data file `calles_de_medellin_con_acoso.csv` is in place.
2. Execute the script and input the respective coordinates when asked.

### Results
The algorithm outputs three potential paths:
1. **Path 1**: Prioritizes safety, may be longer.
2. **Path 2**: Balances between safety and distance.
3. **Path 3**: Shortest distance, moderate safety.

### Sample Output
| Origin | Destination | Distance (meters) | Risk |
|--------|-------------|--------------------|------|
| EAFIT  | UNAL        | 9832               | 0.572|
| EAFIT  | UNAL        | 9401.977           | 0.639|
| EAFIT  | UNAL        | 9353.253           | 0.704|


### Visualization
![(3 paths) (-75 6298634, 6 3033556)_to_(-75 5780337, 6 1828054)](https://github.com/camilobdez/pathfinder/assets/121780547/6ada00ee-0b61-462e-b4a0-bf52de6ca8bb)

## Conclusion

The project demonstrates a practical approach to finding the shortest and safest paths in urban areas, balancing between minimizing travel time and reducing exposure to potential harassment.

## References
- He, Z. and Qin, X. (2016). Incorporating a Safety Index into Pathfinding. Transportation Research Record.
- Ma, D. (2020). Preventing Sexual Harassment Through a Path Finding Algorithm Using Nearby Search. Omdena.
- Gauri, V. and Sandeep, C. (2019). Route-The Safe: A Robust Model for Safest Route Prediction Using Crime and Accidental Data. ResearchGate.
- Keler, A. and Damascene, J. (2016). Safety-aware routing for motorised tourists based on open data and VGI. ResearchGate.
- Techie Delight. (2022). Find the shortest path in a maze. Techie Delight.
- Techie Delight. (2022). Shortest path in a maze – Lee Algorithm. Techie Delight.
- Pencil Programmer. (2022). Shortest Path in Maze using Backtracking. Pencil Programmer.
- Li, J. and Han, X. (2019). Revised Pulse Algorithm for Elementary Shortest Path Problem with Resource Constraints. Seventh International Symposium on Computing and Networking.

## Acknowledgements
This project was created for our course of algorithms and data structures and includes contributions from various open-source libraries.

## Collaborators

- Camilo Bermúdez
- Luis Baena
