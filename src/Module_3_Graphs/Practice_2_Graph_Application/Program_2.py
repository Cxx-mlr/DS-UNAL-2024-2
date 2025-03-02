from Graph import Graph

def main():
    graph = Graph(filename="test-data.csv")

    start_node = "A"
    end_node = "F"

    graph.display_info()
    graph.shortest_path(start_node, end_node)
    graph.check_adjacency(start_node, end_node)

if __name__ == "__main__":
    main()