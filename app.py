import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from aco import ACO
from dijkstra import dijkstra

st.set_page_config(layout="wide")

st.title("🐜 Ant Colony Logic: Explained Visually")
st.markdown("This tool translates the complex math of Ant Colony Optimization (ACO) into something you can easily understand by watching it happen!")

# Generate Graph
@st.cache_data
def get_graph(nodes, edge_prob):
    # Ensure graph is connected
    G = nx.erdos_renyi_graph(nodes, edge_prob)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(nodes, edge_prob)
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 20)
    # Spring layout natively spaces things out without needing the heavy 'scipy' package
    pos = nx.spring_layout(G, seed=42)
    return G, pos

# Sidebar controls - Now with plain English explanations
st.sidebar.header("Step 1. Build the World")
nodes = st.sidebar.slider("Number of Cities (Nodes)", 5, 20, 10, help="How many total points are on the map.")
edge_prob = st.sidebar.slider("Road Connectivity", 0.3, 1.0, 0.6, help="How many roads connect the cities together. 1.0 means every city connects to every other city.")

if st.sidebar.button("🎲 Draw a New Map"):
    st.cache_data.clear()

G, pos = get_graph(nodes, edge_prob)

st.sidebar.header("Step 2. Set the Mission")
start_node = st.sidebar.selectbox("Start Point (The Nest)", list(G.nodes()), 0)
end_node = st.sidebar.selectbox("End Point (The Food)", list(G.nodes()), len(G.nodes())-1)

st.sidebar.header("Step 3. Ant Biology (Variables)")
ants = st.sidebar.slider("Ants per Trip", 5, 50, 15, help="More ants mean more exploration on each turn, but it takes more time.")
iterations = st.sidebar.slider("Generations (Loops)", 5, 100, 30, help="How many times the entire colony repeats the journey to lock down the best scent trail.")
alpha = st.sidebar.slider("Follow the Scent (Alpha)", 0.0, 5.0, 1.0, help="High alpha means ants blindly follow the thickest pheromone trails.")
beta = st.sidebar.slider("Follow the Eyes (Beta)", 0.0, 5.0, 2.0, help="High beta means ants prefer roads that look visibly shorter, ignoring scent.")
evaporation = st.sidebar.slider("Scent Fading (Evaporation)", 0.0, 1.0, 0.5, help="How fast trails vanish. This prevents ants from getting permanently stuck on a bad early path.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("The Map")
    st.markdown("The numbers on the lines represent **Distance** (longer is slower).")
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Custom colors
    colors = []
    for n in G.nodes():
        if n == start_node:
            colors.append('#2ECC71') # Green Nest
        elif n == end_node:
            colors.append('#E74C3C') # Red Food
        else:
            colors.append('#3498DB') # Blue 

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=700, edgecolors='black')
    nx.draw_networkx_labels(G, pos, ax=ax, font_weight='bold', font_color='white')
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='lightgray', width=1.0)
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=9)
    
    st.pyplot(fig)

with col2:
    st.subheader("Watch Them Learn")
    
    if start_node == end_node:
        st.error("The Nest and Food cannot be the exact same place! Please change the dropdowns.")
    else:
        if st.button("🚀 Unleash the Ants!", type="primary"):
            d_path, d_cost = dijkstra(G, start_node, end_node)
            
            aco = ACO(G, ants=ants, iterations=iterations, alpha=alpha, beta=beta, evaporation=evaporation)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # This box will explain what is happening live
            narrative_box = st.info("The ants are waking up and randomly exploring...")
            graph_placeholder = st.empty()
            
            best_cost = float('inf')
            best_path = None
            history = []
            
            for it in range(iterations):
                paths = []
                for _ in range(ants):
                    path, cost = aco.construct_path(start_node, end_node)
                    if cost != float('inf'):
                        paths.append((path, cost))
                    
                    # Update narrative live if a breakthrough happens
                    if cost < best_cost:
                        best_cost = cost
                        best_path = path
                        narrative_box.success(f"**Breakthrough on Loop {it+1}!** An ant stumbled upon a fast route ({best_path}) taking only {best_cost} distance. It dropped a massive pheromone trail here!")

                aco.update(paths)
                if best_cost != float('inf'):
                    history.append(best_cost)
                
                # Update progress
                progress_bar.progress((it + 1) / iterations)
                status_text.markdown(f"**Generation {it+1}/{iterations}** | Shortest path found so far: `{best_cost if best_cost != float('inf') else 'Still lost...'}`")

                # Animate Graph
                if (it + 1) % max(1, (iterations // 6)) == 0 or (it + 1) == iterations:
                    fig_anim, ax_anim = plt.subplots(figsize=(6, 6))
                    nx.draw_networkx_nodes(G, pos, ax=ax_anim, node_color=colors, node_size=700, edgecolors='black')
                    nx.draw_networkx_labels(G, pos, ax=ax_anim, font_weight='bold', font_color='white')
                    
                    pheromones = aco.pheromone
                    max_p = max(pheromones.values()) if pheromones else 1.0
                    
                    for (u, v) in G.edges():
                        p_val = max(pheromones.get((u, v), 1.0), pheromones.get((v, u), 1.0))
                        intensity = p_val / max_p
                        
                        linewidth = 1 + (intensity * 6)
                        alpha_val = min(1.0, 0.2 + (intensity * 0.8))
                        
                        color = plt.cm.Reds(intensity)
                        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax_anim, edge_color=[color], width=linewidth, alpha=alpha_val)

                    graph_placeholder.pyplot(fig_anim)
                    plt.close(fig_anim)
                    time.sleep(0.15) 
                
            progress_bar.empty()
            status_text.empty()
            
            st.divider()
            
            # Clear Language Summary
            st.subheader("Final Conclusion: What just happened?")
            st.write(f"1. The colony started by wandering totally blind from Node **{start_node}** to Node **{end_node}**.")
            st.write(f"2. Over **{iterations}** trips, hundreds of ants deposited a chemical 'pheromone' scent on the roads they took.")
            st.write("3. Short roads accumulated more scent because the ants crossed them faster and more frequently.")
            st.write(f"4. Eventually, the colony 'learned' to completely abandon the bad routes and confidently take the path of `{best_path}`, taking only **{best_cost}** distance!")
            
            c1, c2 = st.columns(2)
            c1.metric("Ant Colony Best Distance", best_cost)
            c2.metric("Computer Perfect Optimal (Dijkstra)", d_cost, delta=f"{best_cost - d_cost} penalty" if best_cost > d_cost else "Perfect match", delta_color="inverse")
            
            with st.expander("Show the Learning Curve Chart"):
                if history:
                    fig_curve, ax_curve = plt.subplots(figsize=(8, 2))
                    ax_curve.plot(history, marker='o', color='#3498DB')
                    ax_curve.set_title("Notice how the distance drops down as the ants 'learn'")
                    ax_curve.set_xlabel("Generations")
                    ax_curve.set_ylabel("Shortest Distance Found")
                    st.pyplot(fig_curve)
                else:
                    st.info("The maze was too complex; the ants never found a valid path.")