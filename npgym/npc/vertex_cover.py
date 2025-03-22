import random

def generate_instance(num_nodes: int, cover_size: int, edge_prob: float = 0.5):
    assert cover_size <= num_nodes
    
    graph = dict()
    graph["nodes"] = [i for i in range(num_nodes)]
    graph["edges"] = set()

    cover_vertices = set(random.sample(range(num_nodes), cover_size))
    remaining_nodes = set(range(num_nodes)) - cover_vertices
    
    for v in remaining_nodes:
        cover_node = random.choice(list(cover_vertices))
        graph["edges"].add(tuple(sorted((v, cover_node))))
    
    for i in cover_vertices:
        for j in range(num_nodes):
            if random.random() < edge_prob and j != i:
                graph["edges"].add(tuple(sorted((i, j))))

    instance = {"cover_size": cover_size, "graph": graph}
    cover_vertices = sorted(list(cover_vertices))
    return instance, cover_vertices

def verify_solution(instance, cover):
    cover_size = instance["cover_size"]
    graph = instance["graph"]
    num_vertices = len(graph["nodes"])
    
    if not isinstance(cover, list):
        return False, "Wrong solution format."
    
    cover = set(cover)

        if not cover:
            return False, "The cover cannot be empty."

        if max(cover) >= num_vertices or min(cover) < 0:
            return False, "The vertex index exceeds the max number."

        if len(cover) > cover_size:
            return False, f"The cover size is larger than {cover_size}"

        for u, v in graph["edges"]:
            if u not in cover and v not in cover:
                return False, f"Edge ({u}, {v}) is not covered."

        return True, "Correct solution."
    except:
        return False, "Verification error."

def test():
    num_nodes = 10
    cover_size = 3
    graph, solution = generate_instance(num_nodes, cover_size)
    print(graph)
    print(solution)
    is_valid, message = verify_solution(graph, solution)
    print(f"验证顶点覆盖:", message)