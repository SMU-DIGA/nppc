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
        7: {"num_variables": 40, "num_clauses": 40},
        8: {"num_variables": 50, "num_clauses": 50},
        9: {"num_variables": 60, "num_clauses": 60},
        10: {"num_variables": 70, "num_clauses": 70},
        11: {"num_variables": 80, "num_clauses": 80},
    },
    "Vertex Cover": {
        1: {"num_nodes": 4, "cover_size": 2},
        2: {"num_nodes": 8, "cover_size": 3},
        3: {"num_nodes": 12, "cover_size": 4},
        4: {"num_nodes": 16, "cover_size": 5},
        5: {"num_nodes": 20, "cover_size": 10},
        6: {"num_nodes": 22, "cover_size": 11},
        7: {"num_nodes": 24, "cover_size": 12},
        8: {"num_nodes": 26, "cover_size": 13},
        9: {"num_nodes": 28, "cover_size": 14},
        10: {"num_nodes": 32, "cover_size": 16},
        11: {"num_nodes": 36, "cover_size": 18},
        12: {"num_nodes": 40, "cover_size": 20},
        13: {"num_nodes": 80, "cover_size": 40},
    },
    "Clique": {
        1: {"num_nodes": 4, "clique_size": 2},
        2: {"num_nodes": 8, "clique_size": 4},
        3: {"num_nodes": 12, "clique_size": 6},
        4: {"num_nodes": 14, "clique_size": 7},
        5: {"num_nodes": 16, "clique_size": 8},
        6: {"num_nodes": 18, "clique_size": 9},
        7: {"num_nodes": 20, "clique_size": 10},
        8: {"num_nodes": 22, "clique_size": 11},
        9: {"num_nodes": 24, "clique_size": 12},
        10: {"num_nodes": 26, "clique_size": 13},
        11: {"num_nodes": 28, "clique_size": 14},
        12: {"num_nodes": 30, "clique_size": 15},
        13: {"num_nodes": 40, "clique_size": 20},
    },
    "Independent Set": {
        1: {"num_nodes": 4, "ind_set_size": 2},
        2: {"num_nodes": 8, "ind_set_size": 4},
        3: {"num_nodes": 12, "ind_set_size": 6},
        4: {"num_nodes": 16, "ind_set_size": 8},
        5: {"num_nodes": 20, "ind_set_size": 10},
        6: {"num_nodes": 24, "ind_set_size": 12},
        7: {"num_nodes": 26, "ind_set_size": 13},
        8: {"num_nodes": 28, "ind_set_size": 14},
        9: {"num_nodes": 30, "ind_set_size": 15},
        10: {"num_nodes": 32, "ind_set_size": 16},
        11: {"num_nodes": 34, "ind_set_size": 17},
        12: {"num_nodes": 36, "ind_set_size": 18},
        13: {"num_nodes": 48, "ind_set_size": 24},
    },
    "Partition": {
        1: {"n": 2, "max_value": 1},
        2: {"n": 4, "max_value": 40},
        3: {"n": 10, "max_value": 100},
        4: {"n": 20, "max_value": 200},
        5: {"n": 30, "max_value": 300},
        6: {"n": 40, "max_value": 400},
        7: {"n": 50, "max_value": 500},
        8: {"n": 55, "max_value": 550},
        9: {"n": 60, "max_value": 600},
        10: {"n": 65, "max_value": 650},
        11: {"n": 70, "max_value": 700},
        12: {"n": 75, "max_value": 750},
        13: {"n": 80, "max_value": 800},
    },
    "Subset Sum": {
        1: {"num_elements": 5, "max_value": 100},
        2: {"num_elements": 10, "max_value": 100},
        3: {"num_elements": 20, "max_value": 200},
        4: {"num_elements": 40, "max_value": 400},  
        5: {"num_elements": 80, "max_value": 800},
        6: {"num_elements": 100, "max_value": 1000},
        7: {"num_elements": 120, "max_value": 1200},
        8: {"num_elements": 160, "max_value": 1000},
        9: {"num_elements": 160, "max_value": 1600},
        10: {"num_elements": 200, "max_value": 2000},
        11: {"num_elements": 200, "max_value": 1000},
        12: {"num_elements": 400, "max_value": 2000},
        13: {"num_elements": 600, "max_value": 2000},
    },
    "Set Packing": {
        1: {"num_elements": 10, "num_subsets": 10, "num_disjoint_sets": 2},
        2: {"num_elements": 40, "num_subsets": 40, "num_disjoint_sets": 8},
        3: {"num_elements": 100, "num_subsets": 200, "num_disjoint_sets": 50},
        4: {"num_elements": 100, "num_subsets": 400, "num_disjoint_sets": 30},
        5: {"num_elements": 100, "num_subsets": 500, "num_disjoint_sets": 30},
        6: {"num_elements": 100, "num_subsets": 600, "num_disjoint_sets": 30},
        7: {"num_elements": 100, "num_subsets": 800, "num_disjoint_sets": 30},
        8: {"num_elements": 100, "num_subsets": 1000, "num_disjoint_sets": 30},
        9: {"num_elements": 200, "num_subsets": 400, "num_disjoint_sets": 60},
        10: {"num_elements": 200, "num_subsets": 800, "num_disjoint_sets": 60},
        11: {"num_elements": 400, "num_subsets": 1000, "num_disjoint_sets": 200},
    },
    "Set Splitting": {
        1: {"num_elements": 5, "num_subsets": 5},
        2: {"num_elements": 10, "num_subsets": 10},
        3: {"num_elements": 10, "num_subsets": 50},
        4: {"num_elements": 10, "num_subsets": 100},
        5: {"num_elements": 10, "num_subsets": 200},
        6: {"num_elements": 100, "num_subsets": 100},
        7: {"num_elements": 100, "num_subsets": 200},
        8: {"num_elements": 10, "num_subsets": 500},
        9: {"num_elements": 10, "num_subsets": 1000},
        10: {"num_elements": 15, "num_subsets": 500},
        11: {"num_elements": 20, "num_subsets": 500},
    },
    "Shortest Common Superstring": {
        1: {"n": 10, "k": 5},
        2: {"n": 20, "k": 10},
        3: {"n": 40, "k": 20},
        4: {"n": 80, "k": 40},
        5: {"n": 100, "k": 50},
        6: {"n": 100, "k": 100},
        7: {"n": 100, "k": 200},
        8: {"n": 200, "k": 200},
        9: {"n": 200, "k": 400},
        10: {"n": 300, "k": 400},
        11: {"n": 300, "k": 600},
        12: {"n": 100, "k": 1000},
    },
    "Quadratic Diophantine Equations": {
        1: {"low": 1, "high": 100},
    },
    "Quadratic Congruences": {
        1: {"min_value": 10, "max_value": 100},
    },
    "3-Dimensional Matching (3DM)": {
        1: {"n": 3},
    },
    "Travelling Salesman (TSP)": {
        1: {"num_cities": 5, "target_length": 10},
    },
    "Dominating Set": {
        1: {"num_nodes": 10, "k": 5},
    },
    "Hitting String": {
        1: {"n": 5, "m": 10},
    },
    "Hamiltonian Cycle": {
        1: {"num_nodes": 5, "directed": False},
        2: {"num_nodes": 8, "directed": False},
        3: {"num_nodes": 10, "directed": False},
        4: {"num_nodes": 12, "directed": False},
        5: {"num_nodes": 16, "directed": False},
        6: {"num_nodes": 18, "directed": False},
        7: {"num_nodes": 20, "directed": False},
        8: {"num_nodes": 22, "directed": False},
        9: {"num_nodes": 25, "directed": False},
        10: {"num_nodes": 30, "directed": False},
    },
    "Bin Packing": {
        1: {"num_items": 10, "bin_capacity": 20, "num_bins": 3},
    },
    "Exact Cover by 3-Sets (X3C)": {
        1: {"num_elements": 3, "num_subsets": 6},
        2: {"num_elements": 4, "num_subsets": 8},
        3: {"num_elements": 5, "num_subsets": 10},
        4: {"num_elements": 7, "num_subsets": 14},
        5: {"num_elements": 8, "num_subsets": 16},
        6: {"num_elements": 10, "num_subsets": 20},
        7: {"num_elements": 15, "num_subsets": 30},
        8: {"num_elements": 20, "num_subsets": 40},
        9: {"num_elements": 30, "num_subsets": 60},
    },
    "Minimum Cover": {
        1: {"num_elements": 5, "num_sets": 10, "k": 3},
        2: {"num_elements": 10, "num_sets": 20, "k": 5},
        3: {"num_elements": 10, "num_sets": 30, "k": 5},
        4: {"num_elements": 15, "num_sets": 20, "k": 8},
        5: {"num_elements": 15, "num_sets": 30, "k": 10},
        6: {"num_elements": 20, "num_sets": 40, "k": 10},
        7: {"num_elements": 25, "num_sets": 50, "k": 10},
        8: {"num_elements": 30, "num_sets": 60, "k": 10},
        9: {"num_elements": 35, "num_sets": 70, "k": 10},
        10: {"num_elements": 40, "num_sets": 80, "k": 10},
        11: {"num_elements": 45, "num_sets": 90, "k": 10},
        12: {"num_elements": 50, "num_sets": 100, "k": 10},
        13: {"num_elements": 55, "num_sets": 110, "k": 10},
        14: {"num_elements": 60, "num_sets": 120, "k": 10},
        15: {"num_elements": 65, "num_sets": 130, "k": 10},
        16: {"num_elements": 70, "num_sets": 140, "k": 10},
    },
    "Graph 3-Colourability (3-COL)": {
        1: {"num_nodes": 5, "num_edges": 8},
        2: {"num_nodes": 8, "num_edges": 12},
        3: {"num_nodes": 10, "num_edges": 20},
        4: {"num_nodes": 15, "num_edges": 25},
        5: {"num_nodes": 15, "num_edges": 30},
        6: {"num_nodes": 15, "num_edges": 40},
        7: {"num_nodes": 20, "num_edges": 30},
        8: {"num_nodes": 20, "num_edges": 40},
        9: {"num_nodes": 20, "num_edges": 45},
        10: {"num_nodes": 20, "num_edges": 50},
        11: {"num_nodes": 30, "num_edges": 60},
        12: {"num_nodes": 30, "num_edges": 80},
    },
    "Clustering": {
        1: {"num_elements": 6, "b": 5},
        8: {"num_elements": 50, "b": 10},  # 0
        9: {"num_elements": 60, "b": 10},  # 0
        10: {"num_elements": 70, "b": 10},  # 0
    },
    "Betweenness": {
        1: {"num_element": 3, "num_triples": 1},
        2: {"num_element": 4, "num_triples": 2},
        3: {"num_element": 5, "num_triples": 3},
        4: {"num_element": 6, "num_triples": 4},
        5: {"num_element": 7, "num_triples": 5},
        6: {"num_element": 8, "num_triples": 6},
    },
    "Minimum Sum of Squares": {
        1: {"num_elements": 10, "k": 3},
    },
    "Bandwidth": {
        1: {"num_nodes": 3, "bandwidth": 2},
        2: {"num_nodes": 4, "bandwidth": 2},
        3: {"num_nodes": 5, "bandwidth": 3},
        4: {"num_nodes": 5, "bandwidth": 2},
        5: {"num_nodes": 6, "bandwidth": 3},
        6: {"num_nodes": 6, "bandwidth": 2},
        7: {"num_nodes": 7, "bandwidth": 3},
        8: {"num_nodes": 7, "bandwidth": 2},
        9: {"num_nodes": 8, "bandwidth": 3},
        10: {"num_nodes": 8, "bandwidth": 2},
    },
    "Maximum Leaf Spanning Tree": {
        1: {"num_nodes": 10, "target_leaves": 3},
    },
}

PROBLEMS = list(PROBLEM_LEVELS.keys())
