from Graph import Graph

def main():
    graph = Graph(filename="road-data.csv")

    start_node = "Medellin"
    end_node = "Bogota"

    graph.display_info()
    graph.shortest_path(start_node, end_node)
    graph.check_adjacency(start_node, end_node)

if __name__ == "__main__":
    main()