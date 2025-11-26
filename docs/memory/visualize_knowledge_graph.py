#!/usr/bin/env python3
"""
Knowledge Graph Visualization Generator

Generates an interactive HTML visualization of the memory.jsonl knowledge graph
using NetworkX for graph structure and Plotly for interactive visualization.

Usage:
    # Install dependencies first (using uv recommended):
    uv pip install -r requirements.txt
    
    # Or with pip:
    pip install networkx plotly numpy
    
    # Then run (using uv run to use the venv):
    uv run python visualize_knowledge_graph.py
    # Opens knowledge_graph.html in your browser
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

try:
    import networkx as nx
    import plotly.graph_objects as go
    from plotly.offline import plot
except ImportError:
    print("Required packages not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx", "plotly"])
    import networkx as nx
    import plotly.graph_objects as go
    from plotly.offline import plot


# Color scheme for different entity types
ENTITY_COLORS = {
    "Repository": "#FF6B6B",  # Red
    "SDK": "#4ECDC4",  # Teal
    "Language": "#45B7D1",  # Blue
    "Agent": "#96CEB4",  # Green
    "Tool": "#FFEAA7",  # Yellow
    "Pattern": "#DDA0DD",  # Plum
    "MCPServer": "#98D8C8",  # Mint
    "Documentation": "#F7DC6F",  # Light Yellow
    "Architectural Decision": "#BB8FCE",  # Light Purple
    "Learning": "#85C1E2",  # Sky Blue
    "Skill": "#F8B88B",  # Peach
}

# Relation type colors
RELATION_COLORS = {
    "uses": "#888888",
    "implements": "#4ECDC4",
    "includes": "#96CEB4",
    "demonstrates": "#DDA0DD",
    "exemplifies": "#FFEAA7",
    "supports": "#45B7D1",
    "tests": "#FF6B6B",
    "implemented_in": "#98D8C8",
    "integrates": "#F7DC6F",
    "informs": "#85C1E2",
}


def load_memory_graph(jsonl_path: Path) -> Tuple[nx.DiGraph, Dict[str, Dict]]:
    """Load entities and relations from memory.jsonl into a NetworkX graph."""
    graph = nx.DiGraph()
    entity_data = {}
    
    # Read JSONL file line by line (standard library approach)
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON line: {e}")
                continue
            
            # Handle entity entries
            if "entityType" in entry and "name" in entry:
                entity_name = entry["name"]
                entity_type = entry["entityType"]
                observations = entry.get("observations", [])
                
                graph.add_node(entity_name, entity_type=entity_type)
                entity_data[entity_name] = {
                    "type": entity_type,
                    "observations": observations,
                }
            
            # Handle relation entries
            elif "from" in entry and "to" in entry:
                from_entity = entry["from"]
                to_entity = entry["to"]
                relation_type = entry.get("relationType", "related_to")
                
                # Ensure nodes exist
                if from_entity not in graph:
                    graph.add_node(from_entity)
                if to_entity not in graph:
                    graph.add_node(to_entity)
                
                # Add edge with relation type
                graph.add_edge(from_entity, to_entity, relation_type=relation_type)
    
    return graph, entity_data


def create_plotly_visualization(graph: nx.DiGraph, entity_data: Dict[str, Dict]) -> go.Figure:
    """Create an interactive Plotly visualization of the knowledge graph."""
    
    # Use spring layout for better node positioning
    pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)
    
    # Separate edges by relation type for better visualization
    edge_traces = []
    relation_types = set()
    for u, v, data in graph.edges(data=True):
        relation_type = data.get("relation_type", "related_to")
        relation_types.add(relation_type)
    
    # Create edge traces grouped by relation type
    for relation_type in sorted(relation_types):
        edge_x = []
        edge_y = []
        edge_info = []
        
        for u, v, data in graph.edges(data=True):
            if data.get("relation_type") == relation_type:
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                edge_info.append(f"{u} → {v} ({relation_type})")
        
        if edge_x:  # Only add trace if there are edges
            edge_trace = go.Scatter(
                x=edge_x,
                y=edge_y,
                line=dict(
                    width=1,
                    color=RELATION_COLORS.get(relation_type, "#CCCCCC"),
                ),
                hoverinfo="none",
                mode="lines",
                name=relation_type,
                showlegend=True,
            )
            edge_traces.append(edge_trace)
    
    # Create node traces grouped by entity type
    node_traces = []
    entity_types = set()
    for node, data in graph.nodes(data=True):
        entity_type = data.get("entity_type", "Unknown")
        entity_types.add(entity_type)
    
    for entity_type in sorted(entity_types):
        node_x = []
        node_y = []
        node_text = []
        node_info = []
        
        for node, data in graph.nodes(data=True):
            if data.get("entity_type") == entity_type:
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)
                
                # Build hover info
                observations = entity_data.get(node, {}).get("observations", [])
                obs_preview = "; ".join(observations[:2]) if observations else "No observations"
                if len(observations) > 2:
                    obs_preview += f" (+{len(observations) - 2} more)"
                
                info = f"<b>{node}</b><br>Type: {entity_type}<br>Observations: {obs_preview}"
                node_info.append(info)
        
        if node_x:  # Only add trace if there are nodes
            node_trace = go.Scatter(
                x=node_x,
                y=node_y,
                mode="markers+text",
                name=entity_type,
                marker=dict(
                    size=15,
                    color=ENTITY_COLORS.get(entity_type, "#CCCCCC"),
                    line=dict(width=2, color="white"),
                ),
                text=node_text,
                textposition="middle center",
                textfont=dict(size=8, color="black"),
                hovertext=node_info,
                hoverinfo="text",
                showlegend=True,
            )
            node_traces.append(node_trace)
    
    # Combine all traces
    data = edge_traces + node_traces
    
    # Create figure
    fig = go.Figure(
        data=data,
        layout=go.Layout(
            title=dict(
                text="Claude Code Agent Knowledge Graph",
                x=0.5,
                font=dict(size=20),
            ),
            showlegend=True,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    text="Interactive knowledge graph showing entities and relationships from memory.jsonl",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                    xanchor="left",
                    yanchor="bottom",
                    font=dict(size=12, color="#888888"),
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor="white",
            paper_bgcolor="white",
        ),
    )
    
    return fig


def generate_statistics(graph: nx.DiGraph, entity_data: Dict[str, Dict]) -> str:
    """Generate statistics about the knowledge graph."""
    stats = []
    stats.append("## Knowledge Graph Statistics\n")
    
    # Entity counts by type
    entity_counts = defaultdict(int)
    for node, data in graph.nodes(data=True):
        entity_type = data.get("entity_type", "Unknown")
        entity_counts[entity_type] += 1
    
    stats.append("### Entity Counts by Type\n")
    for entity_type, count in sorted(entity_counts.items(), key=lambda x: -x[1]):
        stats.append(f"- **{entity_type}**: {count}")
    
    stats.append(f"\n**Total Entities**: {len(graph.nodes())}")
    stats.append(f"**Total Relations**: {len(graph.edges())}\n")
    
    # Relation type counts
    relation_counts = defaultdict(int)
    for u, v, data in graph.edges(data=True):
        relation_type = data.get("relation_type", "related_to")
        relation_counts[relation_type] += 1
    
    stats.append("### Relation Types\n")
    for relation_type, count in sorted(relation_counts.items(), key=lambda x: -x[1]):
        stats.append(f"- **{relation_type}**: {count}")
    
    # Most connected nodes
    stats.append("\n### Most Connected Entities\n")
    degree_centrality = nx.degree_centrality(graph)
    top_nodes = sorted(degree_centrality.items(), key=lambda x: -x[1])[:10]
    for node, centrality in top_nodes:
        stats.append(f"- **{node}**: {graph.degree(node)} connections (centrality: {centrality:.3f})")
    
    return "\n".join(stats)


def main():
    """Main function to generate the visualization."""
    script_dir = Path(__file__).parent
    jsonl_path = script_dir / "memory.jsonl"
    output_path = script_dir / "knowledge_graph.html"
    stats_path = script_dir / "knowledge_graph_stats.md"
    
    if not jsonl_path.exists():
        print(f"Error: {jsonl_path} not found!")
        return
    
    print("Loading knowledge graph from memory.jsonl...")
    graph, entity_data = load_memory_graph(jsonl_path)
    
    print(f"Loaded {len(graph.nodes())} entities and {len(graph.edges())} relations")
    
    print("Generating interactive visualization...")
    fig = create_plotly_visualization(graph, entity_data)
    
    print(f"Writing visualization to {output_path}...")
    plot(fig, filename=str(output_path), auto_open=True)
    
    print("Generating statistics...")
    stats = generate_statistics(graph, entity_data)
    stats_path.write_text(stats)
    print(f"Statistics written to {stats_path}")
    
    print("\n✅ Visualization complete!")
    print(f"   - Interactive graph: {output_path}")
    print(f"   - Statistics: {stats_path}")


if __name__ == "__main__":
    main()

