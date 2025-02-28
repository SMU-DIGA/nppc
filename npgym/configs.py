PROBLEM2PATH = {
    "3-Satisfiability (3-SAT)": "three_sat",  # 0
    "Vertex Cover": "vertex_cover",  # 1
    "Clique": "clique",  # 2
    "Independent Set": "independent_set",  # 3
    "Partition": "partition",  # 4
    "Subset Sum": "subset_sum",  # 5
    "Set Packing": "set_packing",  # 6
    "Set Splitting": "set_splitting",  # 7
}

PROBLEM_LEVELS = {
    "3-Satisfiability (3-SAT)": {
        1: {"num_variables": 5, "num_clauses": 5},
        2: {"num_variables": 10, "num_clauses": 10},
        3: {"num_variables": 15, "num_clauses": 15},
        4: {"num_variables": 20, "num_clauses": 20},
        5: {"num_variables": 25, "num_clauses": 25},
        6: {"num_variables": 30, "num_clauses": 30},
        7: {"num_variables": 40, "num_clauses": 40},
        8: {"num_variables": 50, "num_clauses": 50},
        9: {"num_variables": 60, "num_clauses": 60},
        10: {"num_variables": 70, "num_clauses": 70},
        11: {"num_variables": 80, "num_clauses": 80},
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
    "Set Packing": {
        1: {"num_elements": 10, "num_subsets": 20, "num_disjoint_sets": 3},
    },
    "Set Splitting": {
        1: {"num_elements": 10, "num_subsets": 4},
    },
}

PROBLEMS = list(PROBLEM_LEVELS.keys())
