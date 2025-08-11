import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_workflow_graph():
    """Create a visual representation of the StravaWorkflow LangGraph"""
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Define nodes with their types
    nodes = {
        'START': {'type': 'start', 'color': '#4CAF50'},
        'analyze_query': {'type': 'decision', 'color': '#2196F3'},
        'prepare_graphs': {'type': 'action', 'color': '#FF9800'},
        'prepare_data': {'type': 'action', 'color': '#FF9800'},
        'verify_graphs': {'type': 'verification', 'color': '#9C27B0'},
        'verify_code': {'type': 'verification', 'color': '#9C27B0'},
        'graph_data': {'type': 'action', 'color': '#FF9800'},
        'analyze_data': {'type': 'action', 'color': '#FF9800'},
        'final_response': {'type': 'output', 'color': '#F44336'},
        'END': {'type': 'end', 'color': '#4CAF50'}
    }
    
    # Add nodes
    for node, attrs in nodes.items():
        G.add_node(node, **attrs)
    
    # Add edges
    edges = [
        ('START', 'analyze_query'),
        ('analyze_query', 'prepare_graphs'),
        ('analyze_query', 'prepare_data'),
        ('prepare_graphs', 'verify_graphs'),
        ('prepare_data', 'verify_code'),
        ('verify_graphs', 'graph_data'),
        ('verify_code', 'analyze_data'),
        ('graph_data', 'final_response'),
        ('analyze_data', 'final_response'),
        ('final_response', 'END')
    ]
    
    G.add_edges_from(edges)
    
    return G

def visualize_workflow():
    """Create and display the workflow visualization"""
    
    G = create_workflow_graph()
    
    # Create figure
    plt.figure(figsize=(14, 10))
    
    # Use hierarchical layout
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Adjust positions for better layout
    pos['START'] = np.array([0, 0.8])
    pos['analyze_query'] = np.array([0, 0.4])
    pos['prepare_graphs'] = np.array([-0.6, 0])
    pos['prepare_data'] = np.array([0.6, 0])
    pos['verify_graphs'] = np.array([-0.6, -0.3])
    pos['verify_code'] = np.array([0.6, -0.3])
    pos['graph_data'] = np.array([-0.6, -0.6])
    pos['analyze_data'] = np.array([0.6, -0.6])
    pos['final_response'] = np.array([0, -0.9])
    pos['END'] = np.array([0, -1.2])
    
    # Draw nodes with different colors based on type
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    node_sizes = [800 if node in ['START', 'END'] else 600 for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          node_size=node_sizes,
                          alpha=0.8,
                          edgecolors='black',
                          linewidths=2)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, 
                          edge_color='gray',
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          width=2,
                          alpha=0.7)
    
    # Add conditional edge labels
    edge_labels = {
        ('analyze_query', 'prepare_graphs'): 'Graph Request',
        ('analyze_query', 'prepare_data'): 'Data Analysis Request'
    }
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10)
    
    # Add node labels
    labels = {node: node.replace('_', '\n') for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight='bold')
    
    # Add title and legend
    plt.title('StravaWorkflow LangGraph Structure', fontsize=16, fontweight='bold', pad=20)
    
    # Create legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4CAF50', 
                  markersize=10, label='Start/End'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2196F3', 
                  markersize=10, label='Decision'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF9800', 
                  markersize=10, label='Action'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#9C27B0', 
                  markersize=10, label='Verification'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#F44336', 
                  markersize=10, label='Output')
    ]
    
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
    
    plt.axis('off')
    plt.tight_layout()
    
    # Save the graph
    plt.savefig('workflow_graph.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return G

def print_workflow_summary():
    """Print a summary of the workflow structure"""
    G = create_workflow_graph()
    
    print("=== StravaWorkflow LangGraph Summary ===\n")
    
    print("Nodes:")
    for node in G.nodes():
        node_type = G.nodes[node]['type']
        print(f"  - {node} ({node_type})")
    
    print("\nEdges:")
    for edge in G.edges():
        print(f"  - {edge[0]} -> {edge[1]}")
    
    print("\nWorkflow Paths:")
    print("Path 1: START -> analyze_query -> prepare_graphs -> verify_graphs -> graph_data -> final_response -> END")
    print("Path 2: START -> analyze_query -> prepare_data -> verify_code -> analyze_data -> final_response -> END")
    
    print("\nConditional Logic:")
    print("- analyze_query node has conditional edges based on query type")
    print("- Graph requests go to prepare_graphs path")
    print("- Data analysis requests go to prepare_data path")

if __name__ == "__main__":
    # Create and display the workflow graph
    G = visualize_workflow()
    
    # Print summary
    print_workflow_summary() 