PROBLEM2PATH = {
    "3-Satisfiability (3-SAT)": "three_sat",  # 0
    "Vertex Cover": "vertex_cover",  # 1
    "Clique": "clique",  # 2
    "Independent Set": "independent_set",  # 3
    "Partition": "partition",  # 4
    "Subset Sum": "subset_sum",  # 5
    "Set Packing": "set_packing",  # 6
    "Set Splitting": "set_splitting",  # 7
    "Shortest Common Superstring": "shortest_common_superstring",  # 8
    "Quadratic Diophantine Equations": "quad_diop_equ",  # 9
    "Quadratic Congruences": "quadratic_congruence",  # 10
    "3-Dimensional Matching (3DM)": "three_dimension_matching",  # 11
    "Travelling Salesman (TSP)": "tsp",  # 12
    "Dominating Set": "domninating_set",  # 13
    "Hitting String": "hitting_string",  # 14
    "Hamiltonian Cycle": "hamiltonian_cycle",  # 15
    "Bin Packing": "bin_packing",  # 16
    "Exact Cover by 3-Sets (X3C)": "x3c",  # 17
    "Minimum Cover": "minimum_cover",  # 18
    "Graph 3-Colourability (3-COL)": "graph_three_colorability",  # 19
    "Clustering": "clustering",  # 20
    "Betweenness": "betweenness",  # 21
    "Minimum Sum of Squares": "min_sum_square",  # 22
    "Bandwidth": "bandwidth",  # 23
    "Maximum Leaf Spanning Tree": "max_leaf_span_tree",  # 24
}

PROBLEM_LEVELS = {
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
    "Set Packing": {
        1: {"num_elements": 10, "num_subsets": 20, "num_disjoint_sets": 3},
    },
    "Set Splitting": {
        1: {"num_elements": 10, "num_subsets": 4},
    },
    "Shortest Common Superstring": {
        1: {"n": 3, "k": 10},
    },
    "Quadratic Diophantine Equations": {
        1: {"low": 1, "high": 50},
        2: {"low": 1, "high": 100},
        3: {"low": 1, "high": 500},
        4: {"low": 1, "high": 1000},
        5: {"low": 1, "high": 5000},
        6: {"low": 1, "high": 10000},
        7: {"low": 1, "high": 50000},
        8: {"low": 1, "high": 80000},
        9: {"low": 1, "high": 100000},
        10: {"low": 1, "high": 200000},
    },
    "Quadratic Congruences": {
        1: {"min_value": 1, "max_value": 100}, 
        2: {"min_value": 1, "max_value": 1000}, 
        3: {"min_value": 1, "max_value": 10000},
        4: {"min_value": 1, "max_value": 50000},
        5: {"min_value": 1, "max_value": 100000},
        6: {"min_value": 1, "max_value": 300000},
        7: {"min_value": 1, "max_value": 500000},
        8: {"min_value": 1, "max_value": 800000},
        9: {"min_value": 1, "max_value": 1000000},
        10: {"min_value": 1, "max_value": 3000000},
    },
    "3-Dimensional Matching (3DM)": {
        1: {"n": 5},
        2: {"n": 10},
        3: {"n": 30},
        4: {"n": 50},
        5: {"n": 100}, 
        6: {"n": 150},
        7: {"n": 200},
        8: {"n": 250},
        9: {"n": 300},
        10: {"n": 350},
        11: {"n": 400},
        12: {"n": 500},
    },
    "Travelling Salesman (TSP)": {
        1: {"num_cities": 5, "target_length": 100},
        2: {"num_cities": 8, "target_length": 100},
        3: {"num_cities": 10, "target_length": 100},
        4: {"num_cities": 12, "target_length": 100},
        5: {"num_cities": 15, "target_length": 100},
        6: {"num_cities": 17, "target_length": 200},
        7: {"num_cities": 20, "target_length": 200},
        8: {"num_cities": 22, "target_length": 200},
        9: {"num_cities": 25, "target_length": 200},
        10: {"num_cities": 27, "target_length": 200},
        11: {"num_cities": 30, "target_length": 200},
        12: {"num_cities": 40, "target_length": 300},
    },
    "Dominating Set": {
        1: {"num_nodes": 10, "k": 5, "edge_prob": 0.3},
        2: {"num_nodes": 15, "k": 5, "edge_prob": 0.3},
        3: {"num_nodes": 30, "k": 15, "edge_prob": 0.3},
        4: {"num_nodes": 50, "k": 20, "edge_prob": 0.3},
        5: {"num_nodes": 70, "k": 20, "edge_prob": 0.3},
        6: {"num_nodes": 100, "k": 20, "edge_prob": 0.3},
        7: {"num_nodes": 70, "k": 20, "edge_prob": 0.2},
        8: {"num_nodes": 80, "k": 20, "edge_prob": 0.2},
        9: {"num_nodes": 100, "k": 20, "edge_prob": 0.2},
        10: {"num_nodes": 150, "k": 20, "edge_prob": 0.2},
        11: {"num_nodes": 160, "k": 15, "edge_prob": 0.2},
        12: {"num_nodes": 180, "k": 15, "edge_prob": 0.2},
    },
    "Hitting String": {
        1: {"n": 5, "m": 10},
        2: {"n": 5, "m": 20},
        3: {"n": 10, "m": 20},
        4: {"n": 10, "m": 30},
        5: {"n": 10, "m": 40},
        6: {"n": 10, "m": 45},
        7: {"n": 10, "m": 50},
        8: {"n": 10, "m": 55},
        9: {"n": 10, "m": 60},
        10: {"n": 10, "m": 70},
    },
    "Hamiltonian Cycle": {
        1: {"num_nodes": 5, "directed": False},
    },
    "Bin Packing": {
        1: {"num_items": 10, "bin_capacity": 20, "num_bins": 3},
        2: {"num_items": 20, "bin_capacity": 30, "num_bins": 3},
        3: {"num_items": 30, "bin_capacity": 30, "num_bins": 3},
        4: {"num_items": 40, "bin_capacity": 30, "num_bins": 3},
        5: {"num_items": 50, "bin_capacity": 50, "num_bins": 5},
        6: {"num_items": 60, "bin_capacity": 50, "num_bins": 5},
        7: {"num_items": 70, "bin_capacity": 50, "num_bins": 5},
        8: {"num_items": 80, "bin_capacity": 50, "num_bins": 5},
        9: {"num_items": 80, "bin_capacity": 30, "num_bins": 10},
        10: {"num_items": 100, "bin_capacity": 50, "num_bins": 10},
    },
    "Exact Cover by 3-Sets (X3C)": {
        1: {"num_elements": 3, "num_subsets": 5},
    },
    "Minimum Cover": {
        1: {"num_elements": 5, "num_sets": 10, "k": 3},
    },
    "Graph 3-Colourability (3-COL)": {
        1: {"num_nodes": 5, "num_edges": 8},
    },
    "Clustering": {
        1: {"num_elements": 6, "b": 5},
    },
    "Betweenness": {
        1: {"num_element": 4, "num_triples": 3},
    },
    "Minimum Sum of Squares": {
        1: {"num_elements": 10, "k": 3},
    },
    "Bandwidth": {
        1: {"num_nodes": 5, "bandwidth": 2},
    },
    "Maximum Leaf Spanning Tree": {
        1: {"num_nodes": 10, "target_leaves": 3},
    },
}

PROBLEMS = list(PROBLEM_LEVELS.keys())
