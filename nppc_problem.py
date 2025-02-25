problem2path = {
    "3-Satisfiability (3-SAT)": "three_sat",
    "Vertex Cover": "vertex_cover",
    "Clique": "clique",
    "Independent Set": "independent_set",
    "Partition": "partition",
    "Subset Sum": "subset_sum",
    "Bin Packing": "bin_packing",
}

problem_levels = {
    "3-Satisfiability (3-SAT)": {
        1: {"num_variables": 5, "num_clauses": 5},
        2: {"num_variables": 10, "num_clauses": 10},
        3: {"num_variables": 15, "num_clauses": 15},
        4: {"num_variables": 20, "num_clauses": 20},
        5: {"num_variables": 25, "num_clauses": 25},
        6: {"num_variables": 30, "num_clauses": 30},
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
    "Independent Set": {
        1: {"num_nodes": 4, "ind_set_size": 2},
    },
    "Partition": {
        1: {"n": 6},
    },
    "Subset Sum": {
        1: {"num_elements": 5},
    },
    "Bin Packing": {
        1: {"num_items": 10, "bin_capacity": 20, "num_bins": 3},
    },
}
