problem2path = {
    "3-Satisfiability (3-SAT)": "three_sat",   # 0
    "Vertex Cover": "vertex_cover",            # 1
    "Clique": "clique",                        # 2
    "Independent Set": "independent_set",      # 3
    "Partition": "partition",                  # 4
    "Subset Sum": "subset_sum",                # 5
    "Set Packing": "set_packing",              # 6
    "Set Splitting": "set_splitting",          # 7
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
        2: {"num_nodes": 6, "ind_set_size": 3},
        3: {"num_nodes": 8, "ind_set_size": 4},
        4: {"num_nodes": 16, "ind_set_size": 8},
        5: {"num_nodes": 32, "ind_set_size": 16},
        6: {"num_nodes": 64, "ind_set_size": 32},
    },
    "Partition": {
        1: {"n": 2, "max_value": 10},
        2: {"n": 4, "max_value": 20},
        3: {"n": 6, "max_value": 40},
        4: {"n": 8, "max_value": 80},
        5: {"n": 12, "max_value": 100},
        6: {"n": 16, "max_value": 160},
        100: {"n": 6, "max_value": 100},
    },
    "Subset Sum": {
        2: {"num_elements": 5, "max_value": 100},
        3: {"num_elements": 10, "max_value": 150},
        4: {"num_elements": 15, "max_value": 200},
        5: {"num_elements": 20, "max_value": 250},
        6: {"num_elements": 25, "max_value": 200},
    },
    "Set Packing": {
        1: {"num_elements": 10, "num_subsets": 20, "num_disjoint_sets": 3},
        2: {"num_elements": 12, "num_subsets": 25, "num_disjoint_sets": 4},
        3: {"num_elements": 16, "num_subsets": 30, "num_disjoint_sets": 5},
        4: {"num_elements": 20, "num_subsets": 35, "num_disjoint_sets": 6},
        5: {"num_elements": 24, "num_subsets": 40, "num_disjoint_sets": 7},
        6: {"num_elements": 30, "num_subsets": 45, "num_disjoint_sets": 8},
    },
    "Set Splitting": {
        1: {"num_elements": 10, "num_subsets": 4},
        2: {"num_elements": 15, "num_subsets": 4},
        3: {"num_elements": 20, "num_subsets": 8},
        4: {"num_elements": 25, "num_subsets": 12},
        5: {"num_elements": 30, "num_subsets": 16},
        6: {"num_elements": 35, "num_subsets": 20},
    },
}