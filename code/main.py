from math import sqrt
from turtle import color
import pandas as pd
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import wkt
import dijkstra

def create_graph():

    df = pd.read_csv('calles_de_medellin_con_acoso.csv', sep=";")
    risk_media = df["harassmentRisk"].mean()
    df["harassmentRisk"].fillna(risk_media, inplace=True)
    
    G = nx.DiGraph()
    
    vertices = []
    destinations = []
    
    for i in range(len(df)):
        G.add_node(df.iloc[i]["origin"])
        G.add_node(df.iloc[i]["destination"])
        vertices.append(df.iloc[i]["origin"])
        destinations.append(df.iloc[i]["destination"])
    
    for i in range(len(vertices)):
        v1 = vertices[i]
        v2 = destinations[i]
        distance = df.iloc[i]["length"]
        double_via = df.iloc[i]["oneway"]
        risk = df.iloc[i]["harassmentRisk"]
        geometry = df.iloc[i]["geometry"]
        weight1 = distance * (risk * 10)
        weight2 = 5 * distance + (risk * 100)
        weight3 = sqrt(risk * risk + distance * distance)
        G.add_edge(v1, v2, weight1=weight1, weight2=weight2, weight3=weight3, geometry=geometry, risk=risk, old_distance=distance)
        if double_via:
            G.add_edge(v2, v1, weight1=weight1, weight2=weight2, weight3=weight3, geometry=geometry, risk=risk, old_distance=distance)

    return G

def print_graph(G):
    d = nx.to_dict_of_dicts(G)
    i = 1
    for keys, values in d.items():
        print(i)
        print(keys + " connected to")
        for value in values:
            print("=> " + value + ": {'weight1': " + str(values[value]["weight1"]) + "}"+
            ", {'weight2': " + str(values[value]["weight2"]) + "}"+
            ", {'weight3': " + str(values[value]["weight3"]) + "}"+
            ", {'original weight': " + str(values[value]["old_distance"]) + "}")
        print("")
        i += 1

def print_path(G):
    d = nx.to_dict_of_dicts(G)

    starting_node = input("\nWrite the starting node: ")

    while starting_node not in d.keys():
        starting_node = input("\nWrite a valid starting node: ")

    destination_node = input("\nWrite the destination node: ")

    while destination_node not in d.keys():
        destination_node = input("\nWrite a valid destination node: ")
        
    while starting_node == destination_node:
        print("\nThe starting node and the destination node are the same.")
        destination_node = input("\nWrite another destination node: ")

        while destination_node not in d.keys():
            destination_node = input("\nWrite a valid destination node: ")

    path1 = dijkstra.dijkstra_path(G, starting_node, destination_node, "weight1")

    path2 = dijkstra.dijkstra_path(G, starting_node, destination_node, "weight2")

    path3 = dijkstra.dijkstra_path(G, starting_node, destination_node, "weight3")

    path_geometry1 = []
    path_geometry2 = []
    path_geometry3 = []

    distance1 = 0
    distance2 = 0
    distance3 = 0
    
    risk1 = 0 
    risk2 = 0 
    risk3 = 0

    for i in range(len(path1)-1):
        path_geometry1.append(G[path1[i]][path1[i+1]]["geometry"])
        distance1 += G[path1[i]][path1[i+1]]["old_distance"]
        risk1 += G[path1[i]][path1[i+1]]["risk"]
    risk1 /= len(path1)-1

    for i in range(len(path2)-1):
        path_geometry2.append(G[path2[i]][path2[i+1]]["geometry"])
        distance2 += G[path2[i]][path2[i+1]]["old_distance"]
        risk2 += G[path2[i]][path2[i+1]]["risk"]
    risk2 /= len(path2)-1

    for i in range(len(path3)-1):
        path_geometry3.append(G[path3[i]][path3[i+1]]["geometry"])
        distance3 += G[path3[i]][path3[i+1]]["old_distance"]
        risk3 += G[path3[i]][path3[i+1]]["risk"]
    risk3 /= len(path3)-1

    print("\nThe paths found are:\n")

    print("\nPATH 1\n"+" -> ".join(path1))
    print("\nDistance: " + str(distance1)+"\n")
    print("\nRisk: " + str(risk1)+"\n")

    print("\nPATH 2\n"+" -> ".join(path2))
    print("\nDistance: " + str(distance2)+"\n")
    print("\nRisk: " + str(risk2)+"\n")

    print("\nPATH 3\n"+" -> ".join(path3))
    print("\nDistance: " + str(distance3)+"\n")
    print("\nRisk: " + str(risk3)+"\n")

    return [starting_node, destination_node, path_geometry1, path_geometry2, path_geometry3]
    
def generate_plot(starting_node, destination_node, path_geometry1, path_geometry2, path_geometry3):

    path_geometry1 = pd.DataFrame(path_geometry1, columns =['geometry'])
    path_geometry1['geometry'] = path_geometry1['geometry'].apply(wkt.loads)
    path_geometry1 = gpd.GeoDataFrame(path_geometry1)

    path_geometry2 = pd.DataFrame(path_geometry2, columns =['geometry'])
    path_geometry2['geometry'] = path_geometry2['geometry'].apply(wkt.loads)
    path_geometry2 = gpd.GeoDataFrame(path_geometry2)

    path_geometry3 = pd.DataFrame(path_geometry3, columns =['geometry'])
    path_geometry3['geometry'] = path_geometry3['geometry'].apply(wkt.loads)
    path_geometry3 = gpd.GeoDataFrame(path_geometry3)

    area = pd.read_csv('poligono_de_medellin.csv',sep=';')
    area['geometry'] = area['geometry'].apply(wkt.loads)
    area = gpd.GeoDataFrame(area)
    
    edges = pd.read_csv('calles_de_medellin_con_acoso.csv',sep=';')
    edges['geometry'] = edges['geometry'].apply(wkt.loads)
    edges = gpd.GeoDataFrame(edges)
    
    fig, ax = plt.subplots(figsize=(12,8))
    edges.plot(ax=ax, linewidth=0.3, missing_kwds={'color': 'dimgray'})
    area.plot(ax=ax, facecolor='black')
    path_geometry1.plot(ax=ax,linewidth=2, cmap="hsv")
    path_geometry2.plot(ax=ax,linewidth=2, cmap="cool")
    path_geometry3.plot(ax=ax,linewidth=2, cmap="copper")
    
    plt.title("Safe and shortest routes from " + starting_node + " to " + destination_node)
    plt.tight_layout()
    plt.savefig("(3 paths) " + starting_node + "_to_" + destination_node + ".png")

def main():
    G = create_graph()
    #print_graph(G)
    inputs_plot = print_path(G)
    generate_plot(inputs_plot[0], inputs_plot[1], inputs_plot[2], inputs_plot[3], inputs_plot[4])


main()
