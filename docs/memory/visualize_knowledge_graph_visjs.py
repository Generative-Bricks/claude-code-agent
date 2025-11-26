#!/usr/bin/env python3
"""
Knowledge Graph Visualization Generator (vis.js Network Version)

Generates an interactive HTML visualization of the memory.jsonl knowledge graph
using vis.js Network library, which is specifically designed for graph visualization.

Advantages over Plotly:
- Better graph-specific layout algorithms (physics simulation)
- More interactive features (drag nodes, zoom, pan, clustering)
- Better performance for network graphs
- Built-in search and filtering
- More intuitive for graph exploration

Usage:
    # Install dependencies (using uv recommended):
    uv pip install -r requirements.txt
    
    # Then run (using uv run to use the venv):
    uv run python visualize_knowledge_graph_visjs.py
    # Opens knowledge_graph_visjs.html in your browser
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

try:
    import networkx as nx
except ImportError:
    print("Required packages not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "networkx", "numpy"])
    import networkx as nx


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

# Relation type colors (lighter for edges)
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


def create_visjs_html(graph: nx.DiGraph, entity_data: Dict[str, Dict], output_path: Path) -> None:
    """Create an interactive vis.js Network HTML visualization."""
    
    # Prepare nodes for vis.js
    nodes = []
    node_id_map = {}  # Map entity name to vis.js node ID
    node_counter = 0
    
    # Group nodes by entity type for better organization
    entity_types = set()
    for node, data in graph.nodes(data=True):
        entity_type = data.get("entity_type", "Unknown")
        entity_types.add(entity_type)
    
    # Create nodes with colors and labels
    for node, data in graph.nodes(data=True):
        entity_type = data.get("entity_type", "Unknown")
        observations = entity_data.get(node, {}).get("observations", [])
        
        # Build title (tooltip) with observations
        obs_text = "<br>".join(observations[:5]) if observations else "No observations"
        if len(observations) > 5:
            obs_text += f"<br><i>(+{len(observations) - 5} more)</i>"
        
        title = f"<b>{node}</b><br>Type: {entity_type}"
        if observations:
            title += f"<br><br>Observations:<br>{obs_text}"
        
        # Calculate node size based on connections (degree centrality)
        degree = graph.degree(node)
        size = 10 + min(degree * 2, 30)  # Size between 10 and 40
        
        node_id_map[node] = node_counter
        nodes.append({
            "id": node_counter,
            "label": node,
            "title": title,
            "color": {
                "background": ENTITY_COLORS.get(entity_type, "#CCCCCC"),
                "border": "#333333",
                "highlight": {
                    "background": ENTITY_COLORS.get(entity_type, "#CCCCCC"),
                    "border": "#000000"
                }
            },
            "size": size,
            "font": {
                "size": 12,
                "face": "Arial"
            },
            "group": entity_type,  # For clustering
        })
        node_counter += 1
    
    # Prepare edges for vis.js
    edges = []
    for u, v, data in graph.edges(data=True):
        relation_type = data.get("relation_type", "related_to")
        
        edges.append({
            "from": node_id_map[u],
            "to": node_id_map[v],
            "label": relation_type,
            "color": {
                "color": RELATION_COLORS.get(relation_type, "#CCCCCC"),
                "highlight": "#FF0000"
            },
            "arrows": {
                "to": {
                    "enabled": True,
                    "scaleFactor": 0.8
                }
            },
            "width": 2,
            "title": f"{u} → {v}<br>Relation: {relation_type}",
            "smooth": {
                "type": "continuous",
                "roundness": 0.5
            }
        })
    
    # Create HTML with vis.js Network
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Knowledge Graph Visualization</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        #mynetwork {{
            width: 100%;
            height: 90vh;
            border: 1px solid #ddd;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            color: #333;
            margin: 0;
        }}
        .header p {{
            color: #666;
            margin: 5px 0;
        }}
        .controls {{
            margin-bottom: 15px;
            padding: 10px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }}
        .controls button {{
            margin: 5px;
            padding: 8px 16px;
            background-color: #4ECDC4;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }}
        .controls button:hover {{
            background-color: #45B7D1;
        }}
        .legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 10px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
            border: 1px solid #333;
        }}
        .info {{
            margin-top: 10px;
            padding: 10px;
            background-color: #e8f4f8;
            border-radius: 4px;
            font-size: 12px;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Claude Code Agent Knowledge Graph</h1>
        <p>Interactive visualization of entities and relationships from memory.jsonl</p>
    </div>
    
    <div class="controls">
        <button onclick="fitNetwork()">Fit to Screen</button>
        <button onclick="resetZoom()">Reset Zoom</button>
        <button onclick="togglePhysics()">Toggle Physics</button>
        <button onclick="exportImage()">Export as PNG</button>
        <input type="text" id="searchBox" placeholder="Search nodes..." onkeyup="searchNodes()" style="padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; width: 200px;">
    </div>
    
    <div class="legend">
        <strong>Entity Types:</strong>
        {''.join([f'<div class="legend-item"><div class="legend-color" style="background-color: {ENTITY_COLORS.get(et, "#CCCCCC")};"></div><span>{et}</span></div>' for et in sorted(entity_types)])}
    </div>
    
    <div id="mynetwork"></div>
    
    <div class="info">
        <strong>Tips:</strong> Drag nodes to rearrange • Scroll to zoom • Click nodes to highlight connections • 
        Use search box to find specific entities • Toggle physics to stabilize layout
    </div>
    
    <script type="text/javascript">
        // Create nodes and edges
        const nodes = new vis.DataSet(JSON_NODES_PLACEHOLDER);
        const edges = new vis.DataSet(JSON_EDGES_PLACEHOLDER);
        
        // Create network
        const container = document.getElementById('mynetwork');
        const data = {{
            nodes: nodes,
            edges: edges
        }};
        
        const options = {{
            nodes: {{
                shape: 'dot',
                shadow: true,
                font: {{
                    size: 12,
                    face: 'Arial'
                }}
            }},
            edges: {{
                arrows: {{
                    to: {{ enabled: true, scaleFactor: 0.8 }}
                }},
                font: {{
                    size: 10,
                    align: 'middle'
                }},
                smooth: {{
                    type: 'continuous',
                    roundness: 0.5
                }}
            }},
            physics: {{
                enabled: true,
                stabilization: {{
                    enabled: true,
                    iterations: 200
                }},
                barnesHut: {{
                    gravitationalConstant: -2000,
                    centralGravity: 0.1,
                    springLength: 200,
                    springConstant: 0.04,
                    damping: 0.09
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 100,
                zoomView: true,
                dragView: true
            }},
            layout: {{
                improvedLayout: true
            }}
        }};
        
        const network = new vis.Network(container, data, options);
        
        let physicsEnabled = true;
        
        // Event handlers
        network.on("click", function (params) {{
            if (params.nodes.length > 0) {{
                const nodeId = params.nodes[0];
                const node = nodes.get(nodeId);
                console.log("Selected node:", node.label);
            }}
        }});
        
        network.on("stabilizationEnd", function() {{
            console.log("Network stabilized");
        }});
        
        // Control functions
        function fitNetwork() {{
            network.fit();
        }}
        
        function resetZoom() {{
            network.moveTo({{ scale: 1 }});
        }}
        
        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
            network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
            console.log("Physics " + (physicsEnabled ? "enabled" : "disabled"));
        }}
        
        function exportImage() {{
            const canvas = network.getCanvas();
            const dataURL = canvas.toDataURL('image/png');
            const link = document.createElement('a');
            link.download = 'knowledge_graph.png';
            link.href = dataURL;
            link.click();
        }}
        
        function searchNodes() {{
            const searchTerm = document.getElementById('searchBox').value.toLowerCase();
            if (searchTerm === '') {{
                nodes.update(nodes.get().map(node => ({{ ...node, hidden: false }})));
                return;
            }}
            
            const allNodes = nodes.get();
            allNodes.forEach(node => {{
                const matches = node.label.toLowerCase().includes(searchTerm);
                nodes.update({{ id: node.id, hidden: !matches }});
            }});
        }}
    </script>
</body>
</html>"""
    
    # Replace placeholders with actual JSON data
    nodes_json = json.dumps(nodes, indent=2)
    edges_json = json.dumps(edges, indent=2)
    html_content = html_content.replace("JSON_NODES_PLACEHOLDER", nodes_json)
    html_content = html_content.replace("JSON_EDGES_PLACEHOLDER", edges_json)
    
    # Write HTML file
    output_path.write_text(html_content, encoding='utf-8')


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
    output_path = script_dir / "knowledge_graph_visjs.html"
    stats_path = script_dir / "knowledge_graph_stats_visjs.md"
    
    if not jsonl_path.exists():
        print(f"Error: {jsonl_path} not found!")
        return
    
    print("Loading knowledge graph from memory.jsonl...")
    graph, entity_data = load_memory_graph(jsonl_path)
    
    print(f"Loaded {len(graph.nodes())} entities and {len(graph.edges())} relations")
    
    print("Generating interactive vis.js Network visualization...")
    create_visjs_html(graph, entity_data, output_path)
    
    print(f"Writing visualization to {output_path}...")
    
    print("Generating statistics...")
    stats = generate_statistics(graph, entity_data)
    stats_path.write_text(stats)
    print(f"Statistics written to {stats_path}")
    
    print("\n✅ Visualization complete!")
    print(f"   - Interactive graph: {output_path}")
    print(f"   - Statistics: {stats_path}")
    print("\n📊 Features:")
    print("   - Physics simulation for natural layout")
    print("   - Drag nodes to rearrange")
    print("   - Search and filter nodes")
    print("   - Export as PNG")
    print("   - Click nodes to see connections")


if __name__ == "__main__":
    main()

