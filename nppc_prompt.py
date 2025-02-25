nppc_template = """
# <problem_name> Problem Description:
<problem_description>

# Examples:
<in_context_examples>
# Problem to Solve: 
Problem: <problem_to_solve>

# Instruction:
Now please solve the above problem. Reason step by step and present your answer in the "solution" field in the following json format:
```json
{"solution": "___" }
```

"""

example_and_solution = """Problem: <example_problem>
{"solution": <example_solution>}
"""

problem_descriptions = {
    "3-Satisfiability (3-SAT)": """Input: A set of m clauses - C1 ,C2,...,Cm - over a set of n Boolean valued variables Xn=<x1,x2,...,xn>, such that each clause depends on exactly three distinct variables from Xn. A clause being a Boolean expression of the form yi+yj+yk where each y is of the form x or -x (i.e. negation of x) with x being some variable in Xn. For example if n=4 and m=3 a possible instance could be the (set of) Boolean expressions: C1=(x1+(-x2)+(-x3)); C2=(x2+x3+(-x4)); C3=((-x1)+x3+x4);
Question: Can each variable xi of Xn be assigned a Boolean value alphai in such a way that every clause evaluates to the Boolean result true under the assignment < xi:=alphai:1<=i<=n>? """,
    "Vertex Cover": """Input: An n-node undirected graph G(V,E) with node set V and edge set E; a positive integer k with k<=n.
Question: Is there a subset W of V having size at most k and such that for every edge {u,v} in E at least one of u and v belongs to W?""",
    "Clique": """Input: An n-node undirected graph G(V,E) with node set V and edge set E; a positive integer k with k<=n.
Question: Does G contain a k-clique, i.e. a subset W of the nodes V such that W has size k and for each distinct pair of nodes u, v in W, {u,v} is an edge of G?
""",
    "Independent Set": """Input: n-node undirected graph G(V,E); positive integer k<=n.
Question: Does G have an independent set of size at least k, i.e. a subset W of at least k nodes from V such that no pair of nodes in W is joined by an edge in E?""",
    "Partition": """Input: Finite set A; for each element a in A a positive integer size s(a).
Question: Can A be partitioned into 2 disjoint sets A1 and A2 in a such a way that the sum of the sizes s(x) of elements x in A1 is exactly the same as the sum of the sizes s(y) of the elements y in A2.
Comments: It should be noted that it is not required that A1 and A2 contain equal numbers of elements, although even with this condition the problem is still NP-complete.""",
    "Subset Sum": """Input: Finite set A; for each element a in A a positive integer size s(a); a positive integer K.
Question: Is there a subset B of A such that the sum of the sizes, s(x), of the elements x in B is exactly equal to K?""",
    "Bin Packing": """Input: A finite set U of m items; for each item u in U a positive integer size s(u); positive integers B (called the bin capacity) and k<=m.
Question: Can U be partitioned into k disjoint sets U1,...,Uk such that for each Ui (1<=i<=k) the total sum of the sizes of the items in Ui does not exceed B?""",
}
