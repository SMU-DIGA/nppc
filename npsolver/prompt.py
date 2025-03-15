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
Question: Does G contain a k-clique, i.e. a subset W of the nodes V such that W has size k and for each distinct pair of nodes u, v in W, {u,v} is an edge of G?""",
    "Independent Set": """Input: n-node undirected graph G(V,E); positive integer k<=n.
Question: Does G have an independent set of size at least k, i.e. a subset W of at least k nodes from V such that no pair of nodes in W is joined by an edge in E?""",
    "Partition": """Input: Finite set A; for each element a in A a positive integer size s(a).
Question: Can A be partitioned into 2 disjoint sets A1 and A2 in a such a way that the sum of the sizes s(x) of elements x in A1 is exactly the same as the sum of the sizes s(y) of the elements y in A2.""",
    "Subset Sum": """Input: Finite set A; for each element a in A a positive integer size s(a); a positive integer K.
Question: Is there a subset B of A such that the sum of the sizes, s(x), of the elements x in B is exactly equal to K?""",
    "Set Packing": """Input: A collection C=(C1,...,Cm) of finite sets; a positive integer k<=m.
Question: Are there k sets - D1,...,Dk - from the collection C such that for all 1<=i< j<=k, Di and Dj have no common elements?""",
    "Set Splitting": """Input: A finite set S; A collection C1,...,Cm of subsets of S.
Question: Can S be partitioned into two disjoint subsets - S1 and S2 - such that for each set Ci it holds that Ci is not a subset of S1 and Ci is not a subset of S2?""",
    "Shortest Common Superstring": """Input: A finite set R={r1,r2,...,rm} of strings (sequences of symbols); positive integer k.
Question: Is there a string w of length at most k such that every string in R is a substring of w, i.e. for each r in R, w can be decomposed as w=w0rw1 where w0, w1 are (possibly empty) strings?""",
    "Quadratic Diophantine Equations": """Input: Positive integers a, b, and c.
Question: Are there two positive integers x and y such that (a*x*x)+(b*y)=c?""",
    "Quadratic Congruences": """Input: Positive integers a, b, and c.
Question: Is there a positive integer x whose value is less than c and is such that x*x==a(mod b), i.e. the remainder when x*x is divided by b is equal to a?""",
    "3-Dimensional Matching (3DM)": """Input: 3 disjoint sets X, Y, and Z, each containing exactly n elements; a set M of m triples {(xi,yi,zi):1<=i<=m} such that xi is in X, yi in Y, and zi in Z, i.e. M is a subset of XxYxZ.
Question: Does M contain a matching, i.e. is there a subset Q of M such that |Q|=n and for all distinct pairs of triples (u,v,w) and (x,y,z) in Q it holds that u/=x and v/=y and w/=z?""",
    "Travelling Salesman (TSP)": """Input: A set C of n cities {c1,...,cn}; a positive integer distance d(i, j) for each pair of cities (ci,cj) (1<=i< j<=n); a positive integer B representing the maximum allowed travel distance.
Question: Is there an ordering < pi(1),pi(2),...,pi(n)> of the n cities such that the total travel distance, calculated as the sum of d(pi(i), pi(i+1)) for i = 1 to n-1, plus d(pi(n), pi(1)), is at most B?""",
    "Dominating Set": """Input: An undirected graph G(V,E) with n nodes; a positive integer k where k<=n.
Question: Does G contain a dominating set of size at most k, i.e. a subset W of V containing at most k nodes such that every node u in V-W (i.e. in V but not in W) has at least one neighbor w in W where {u,w} is an edge in E?""",
    "Hitting String": """Input: A finite set S = {s1, ..., sm}, where each si is a string of length n over the alphabet {0,1,*}.
Question: Is there a binary string x=x1x2...xn of length n such that for each string sj in S, there is at least one position i (1 ≤ i ≤ n) where x and sj have the same symbol, or sj has '*' in that position?""",
    "Hamiltonian Cycle": """Input: n-node graph G(V,E).
Question: Is there a cycle in G that visits every node in V exactly once and returns to the starting node, and thus contains exactly n edges?""",
    "Bin Packing": """Input: A finite set U of m items; for each item u in U, a positive integer size s(u); positive integers B (bin capacity) and k, where k ≤ m..
Question: Can U be partitioned into k disjoint subsets U1, ..., Uk such that the total size of the items in each subset Ui (for 1 ≤ i ≤ k) does not exceed B?""",
    "Exact Cover by 3-Sets (X3C)": """Input: A finite set X containing exactly 3n elements; a collection C of subsets of X each of which contains exactly 3 elements.
Question: Does C contain an exact cover for X, i.e. a sub-collection of 3-element sets D=(D1,...,Dn) such that each element of X occurs in exactly one subset in D?""",
    "Minimum Cover": """Input: A finite set S; A collection C=(C1,...,Cm) of subsets of S; a positive integer k<=m.
Question: Does C contain a cover for S comprising at most k subsets, i.e. a collection D=(D1,...,Dt), where t<=k, each Di is a set in C, and such that every element in S belongs to at least one set in D?""",
    "Graph 3-Colourability (3-COL)": """Input: An n-node undirected graph G(V,E) with node set V and edge set E.
Question: Can each node of G(V,E) be assigned exactly one of three colours - Red, Blue, Green - in such a way that no two nodes which are joined by an edge, are assigned the same colour?""",
    "Clustering": """Input: Finite set X; for each pair of elements x and y in X, a positive integer distance d(x,y); positive integer B.
Question: Is there a partition of X into 3 disjoint sets - X1,X2,X3 - with which: for each set Xi (1<=i<=3), for all pairs x and y in Xi it holds that d(x,y)<=B?""",
    "Betweenness": """Input: A finite set A of n elements; a set C of ordered triples, (a,b,c), of distinct elements from A.
Question: Is there a one-to-one function, f:A->{0,1,2,...,n-1} such that for each triple (a,b,c) in C it holds that either f(a)< f(b)< f(c) or f(c)< f(b)< f(a)?""",
    "Minimum Sum of Squares": """Input: A set A of n elements; for each element a in A a positive integer size s(a); positive integers k<=n and J.
Question: Can A be partitioned into k disjoint sets A1,...,Ak such that sum from i=1 to k ( sum from {x in Ai} s(x))2<=J?""",
    "Bandwidth": """Input: n-node undirected graph G(V,E); positive integer k<=n.
Question: Is there a linear ordering of V with bandwidth at most k, i.e. a one-to-one function f:V->{0,1,2,...,n-1} such that for all edges {u,v} in G, |f(u)-f(v)|<=k?""",
    "Maximum Leaf Spanning Tree": """Input: n-node undirected graph G(V,E); positive integer k<=n.
Question: Does G have a spanning tree in which at least k nodes have degree 1?""",
}
