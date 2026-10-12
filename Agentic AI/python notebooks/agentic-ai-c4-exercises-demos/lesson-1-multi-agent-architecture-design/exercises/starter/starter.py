import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D




def layered_layout(graph, source, horizontal_spacing=1.0, vertical_spacing=1.4, sweeps=4):
    """Left-to-right layered layout (Sugiyama-style) with crossing reduction."""
    # 1. Break cycles: drop edges that point back toward the source (return paths)
    hops = nx.single_source_shortest_path_length(graph, source)
    far = max(hops.values()) + 1
    dist = {n: hops.get(n, far) for n in graph.nodes}

    dag = nx.DiGraph()
    dag.add_nodes_from(graph.nodes)
    for u, v in graph.edges:
        if dist[v] < dist[u]:
            continue  # return edge, ignore for layering
        if dist[v] == dist[u] and nx.has_path(dag, v, u):
            continue  # would create a loop within the same distance
        dag.add_edge(u, v)

    # 2. Assign each node a column by longest path from the source
    layer = {}
    for node in nx.topological_sort(dag):
        layer[node] = max((layer[p] + 1 for p in dag.predecessors(node)), default=0)

    layers = {}
    for node, idx in layer.items():
        layers.setdefault(idx, []).append(node)

    # 3. Reduce crossings: reorder each column by the average position of its neighbors
    undirected = graph.to_undirected()
    order = {n: i for col in layers.values() for i, n in enumerate(col)}

    def reorder(columns, neighbor_col_offset):
        for idx in columns:
            def barycenter(n):
                nbrs = [order[m] for m in undirected.neighbors(n)
                        if layer[m] == idx + neighbor_col_offset]
                return sum(nbrs) / len(nbrs) if nbrs else order[n]
            layers[idx].sort(key=barycenter)
            for i, n in enumerate(layers[idx]):
                order[n] = i

    cols = sorted(layers)
    for _ in range(sweeps):
        reorder(cols[1:], -1)         # left-to-right sweep
        reorder(cols[-2::-1], +1)     # right-to-left sweep

    # 4. Convert columns/rows to coordinates, centering each column vertically
    pos = {}
    for idx, col in layers.items():
        for i, node in enumerate(col):
            pos[node] = (idx * horizontal_spacing, ((len(col) - 1) / 2 - i) * vertical_spacing)
    return pos


def column_layout(columns, horizontal_spacing=300, vertical_spacing=170):
    """Place nodes in fixed columns, top to bottom in the order given, centered vertically."""
    pos = {}
    for col_idx, column in enumerate(columns):
        for row_idx, node in enumerate(column):
            pos[node] = (col_idx * horizontal_spacing,
                         ((len(column) - 1) / 2 - row_idx) * vertical_spacing)
    return pos


def create_diagram(title, nodes, edges, node_labels=None, node_types=None, edge_labels=None,
                   columns=None):
    graph = nx.DiGraph()
    
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    
    if node_labels is None:
        node_labels = {node: node for node in nodes}
    if node_types is None:
        node_types = {node: 'agent' for node in nodes}
    if edge_labels is None:
        edge_labels = {}

    # Graphviz "dot" draws left-to-right layers and minimizes edge crossings;
    # fall back to the pure-Python layered layout if pygraphviz isn't installed.
    # If explicit columns are given, use them instead. Positions are in points (1/72 inch).
    if columns is not None:
        pos = column_layout(columns)
    else:
        try:
            agraph = nx.nx_agraph.to_agraph(graph)
            agraph.graph_attr.update(rankdir="LR", ranksep="0.8", nodesep="0.4")
            # Tell dot each node's real footprint: the shape plus the text label underneath,
            # so it leaves enough room and labels don't collide
            agraph.node_attr.update(shape="box", fontsize="13", height="1.6", margin="0.2,0")
            for node in nodes:
                agraph.get_node(node).attr["label"] = node_labels[node]
            # Return edges (pointing back toward the source) shouldn't push nodes into
            # later columns, otherwise sibling nodes like the two specialists get split up
            hops = nx.single_source_shortest_path_length(graph, nodes[0])
            for u, v in graph.edges:
                if u in hops and v in hops and hops[v] < hops[u]:
                    agraph.get_edge(u, v).attr["constraint"] = "false"
            agraph.layout(prog="dot")
            pos = {node: tuple(float(c) for c in agraph.get_node(node).attr["pos"].split(","))
                   for node in nodes}
        except ImportError:
            pos = layered_layout(graph, nodes[0], horizontal_spacing=260, vertical_spacing=120)

    # Size the figure to the layout (1 layout point = 1 figure point) so dot's spacing holds
    xs, ys = [p[0] for p in pos.values()], [p[1] for p in pos.values()]
    pad_x, pad_y = 130, 90
    width = max(xs) - min(xs) + 2 * pad_x
    height = max(ys) - min(ys) + 2 * pad_y
    fig = plt.figure(figsize=(width / 72, height / 72))
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.set_xlim(min(xs) - pad_x, max(xs) + pad_x)
    ax.set_ylim(min(ys) - pad_y, max(ys) + pad_y)
    plt.title(title, fontsize=16, fontweight='bold', pad=20)

    node_colors = []
    node_shapes = []
    node_sizes = []
    
    for node in nodes:
        node_type = node_types.get(node, 'agent')
        
        if node_type == 'agent':
            node_colors.append("#6495ED")
            node_shapes.append('o')
            node_sizes.append(2800)
        elif node_type == 'tool':
            node_colors.append("#FFD700")
            node_shapes.append('s')
            node_sizes.append(2600)
        elif node_type == 'user':
            node_colors.append("#FF6347")
            node_shapes.append('d')
            node_sizes.append(2400)
        elif node_type == 'data':
            node_colors.append("#90EE90")
            node_shapes.append('h')
            node_sizes.append(2500)
        else:
            node_colors.append("#C0C0C0")
            node_shapes.append('p')
            node_sizes.append(2300)

    for i, node in enumerate(nodes):
        nx.draw_networkx_nodes(graph, pos, 
                             nodelist=[node],
                             node_color=[node_colors[i]], 
                             node_shape=node_shapes[i],
                             node_size=node_sizes[i],
                             edgecolors='black', 
                             linewidths=1.5, 
                             alpha=0.9)
    
    # Two-way pairs (A->B and B->A) get a wider curve so the arrows don't overlap
    two_way = [(u, v) for u, v in graph.edges if graph.has_edge(v, u)]
    one_way = [(u, v) for u, v in graph.edges if not graph.has_edge(v, u)]
    edge_groups = [(one_way, "arc3,rad=0.1"), (two_way, "arc3,rad=0.15")]

    for edgelist, style in edge_groups:
        # Passing the real node sizes makes arrows stop at the shape border, not the center
        nx.draw_networkx_edges(graph, pos,
                             edgelist=edgelist,
                             nodelist=nodes,
                             node_size=node_sizes,
                             edge_color="black",
                             arrowsize=25,
                             width=2.0,
                             alpha=0.9,
                             arrowstyle='-|>',
                             connectionstyle=style)

    # Labels sit just below each shape so they don't cover the arrowheads
    for node, (x, y) in pos.items():
        plt.annotate(node_labels[node], (x, y),
                xytext=(0, -34), textcoords='offset points',
                fontsize=11,
                ha='center',
                va='top',
                fontweight='bold',
                bbox=dict(facecolor='white', 
                         alpha=0.8, 
                         edgecolor='lightgray', 
                         boxstyle='round,pad=0.5'))
                         
    # Edge labels are placed on the curved edge itself, using the same curve as the arrow
    for edgelist, style in edge_groups:
        group_labels = {e: label for e, label in edge_labels.items() if e in edgelist}
        if not group_labels:
            continue
        nx.draw_networkx_edge_labels(graph, pos,
                                     edge_labels=group_labels,
                                     nodelist=nodes,
                                     node_size=node_sizes,
                                     connectionstyle=style,
                                     rotate=False,
                                     font_size=12,
                                     font_weight='bold',
                                     font_color='darkblue',
                                     bbox=dict(facecolor='white',
                                              alpha=0.9,
                                              edgecolor='blue',
                                              boxstyle='round,pad=0.3'))

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor="#6495ED", markersize=15, label='Agent'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor="#FFD700", markersize=15, label='Tool/Resource'),
        Line2D([0], [0], marker='d', color='w', markerfacecolor="#FF6347", markersize=15, label='User Interface'),
        Line2D([0], [0], marker='h', color='w', markerfacecolor="#90EE90", markersize=15, label='Data Component')
    ]
    # Legend sits below the diagram so it never covers nodes
    plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.0),
               ncol=4, fontsize=12, frameon=False)

    plt.axis("off")
    
    # Save the diagram as an image file
    filename = title.replace(' ', '_').replace(':', '') + '.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Diagram saved as: {filename}")
    plt.close()



""" 
Suggested Extensions, Pick One or Mix
1. Add a "Translation Verification Agent"
This agent checks if the translation preserves meaning/cultural context.

Comes after the language specialist and before the response goes to the user.

2. Add a "Multimodal Media Tool"
A tool that retrieves images/audio relevant to the query (e.g., a sound clip of a traditional song or image of a local artifact).

Connects to both the language specialist and the knowledge base.

3. Add a "Feedback Collector"
Captures user feedback after receiving information.

Helps improve future responses and tracks which areas need more detail or clarification.

4. Add a "Cultural Sensitivity Checker" Tool
Ensures that knowledge being returned is appropriate to share (some Indigenous knowledge is restricted or sacred).


"""


def extended_uluru_exercise():
    # Existing Nodes
    nodes = [
        "Visitor Input",
        "Language Identification",
        "Arrernte Language Specialist",
        "Pitjantjatjara Language Specialist",
        "Knowledge Base Lookup",
        "Translation Verification Agent",  # New Node
        "Multimodal Media Tool",           # New Node
        "Feedback Collector",              # New Node
        "Cultural Sensitivity Checker",    # New Node
    ]
    
    edges = [
        ("Visitor Input", "Language Identification"),
        ("Visitor Input", "Feedback Collector"),
        ("Language Identification", "Visitor Input"),
        ("Language Identification", "Arrernte Language Specialist"),
        ("Language Identification", "Pitjantjatjara Language Specialist"),
        ("Arrernte Language Specialist", "Language Identification"),
        ("Pitjantjatjara Language Specialist", "Language Identification"),
        ("Arrernte Language Specialist", "Translation Verification Agent"),
        ("Pitjantjatjara Language Specialist", "Translation Verification Agent"),
        ("Translation Verification Agent", "Language Identification"),
        ("Arrernte Language Specialist", "Knowledge Base Lookup"),
        ("Pitjantjatjara Language Specialist", "Knowledge Base Lookup"),
        ("Knowledge Base Lookup", "Arrernte Language Specialist"),
        ("Knowledge Base Lookup", "Pitjantjatjara Language Specialist"),
        ("Knowledge Base Lookup", "Multimodal Media Tool"),
        ("Knowledge Base Lookup", "Cultural Sensitivity Checker"),
        ("Multimodal Media Tool", "Arrernte Language Specialist"),
        ("Multimodal Media Tool", "Pitjantjatjara Language Specialist"),
        ("Cultural Sensitivity Checker", "Pitjantjatjara Language Specialist"),
        ("Cultural Sensitivity Checker", "Arrernte Language Specialist"),
        
        
    ]
    
    node_types = {
        "Visitor Input": "user",
        "Language Identification": "tool",
        "Arrernte Language Specialist": "agent",
        "Pitjantjatjara Language Specialist": "agent",
        "Knowledge Base Lookup": "tool",
        "Translation Verification Agent": "agent",
        "Multimodal Media Tool": "tool",
        "Feedback Collector": "tool",
        "Cultural Sensitivity Checker": "tool",
    }

    edge_labels = {
        
    }

    # Fixed layout: each inner list is a column, nodes listed top to bottom
    columns = [
        ["Visitor Input", "Feedback Collector"],
        ["Language Identification"],
        ["Arrernte Language Specialist", "Translation Verification Agent",
         "Pitjantjatjara Language Specialist"],
        ["Cultural Sensitivity Checker", "Knowledge Base Lookup", "Multimodal Media Tool"],
    ]

    create_diagram(
        "Uluru Cultural Center: Extended System",
        nodes,
        edges,
        None,
        node_types,
        edge_labels,
        columns
    )
if __name__ == "__main__":
    extended_uluru_exercise()
