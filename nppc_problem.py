problem2path = {
    "3-Satisfiability (3-SAT)": "three_sat",
    "Vertex Cover": "vertex_cover",
    "Clique": "clique",
}

problem_levels = {
    "3-Satisfiability (3-SAT)": {
        1: {"num_variables": 5, "num_clauses": 5},
        2: {"num_variables": 5, "num_clauses": 5},
        3: {"num_variables": 5, "num_clauses": 5},
        4: {"num_variables": 5, "num_clauses": 5},
        5: {"num_variables": 5, "num_clauses": 5},
        6: {"num_variables": 5, "num_clauses": 5},
    },
    "Vertex Cover": {
        1: {"num_nodes": 4, "cover_size": 2},
        2: {"num_nodes": 6, "cover_size": 3},
        3: {"num_nodes": 8, "cover_size": 4},
        4: {"num_nodes": 10, "cover_size": 5},
        5: {"num_nodes": 12, "cover_size": 6},
        6: {"num_nodes": 14, "cover_size": 7},
    },
    "Clique": {
        1: {"num_nodes": 4, "clique_size": 2},
        2: {"num_nodes": 6, "clique_size": 3},
        3: {"num_nodes": 8, "clique_size": 4},
        4: {"num_nodes": 10, "clique_size": 5},
        5: {"num_nodes": 12, "clique_size": 6},
        6: {"num_nodes": 14, "clique_size": 7},
    },
}
