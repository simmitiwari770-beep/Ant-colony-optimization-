# 🐜 Ant Colony Optimization Visualizer

An interactive web application that visually demonstrates how **Ant Colony Optimization (ACO)** finds the shortest path in a graph, and compares it with the **Dijkstra algorithm (optimal solution)**.

This project transforms complex algorithm concepts into an intuitive and visual learning experience.

---

## 🚀 Features

- 🎯 Random graph generation (cities & roads)
- 🐜 Real-time Ant Colony Optimization simulation
- 📊 Pheromone trail visualization (learning process)
- ⚡ Comparison with Dijkstra’s shortest path
- 📈 Learning curve tracking
- 🎛️ Adjustable parameters:
  - Number of ants
  - Iterations
  - Alpha (pheromone importance)
  - Beta (distance importance)
  - Evaporation rate

---

## 🧠 Concept

Ant Colony Optimization is inspired by how real ants find the shortest path:

- Ants explore multiple paths randomly  
- They deposit pheromones on paths  
- Shorter paths accumulate stronger pheromones  
- Over time, the colony converges to the optimal path  

This is compared with:

👉 **Dijkstra Algorithm** — a deterministic algorithm that always finds the exact shortest path

---

## 🖥️ Tech Stack

- Python  
- Streamlit (UI)  
- NetworkX (Graph processing)  
- Matplotlib (Visualization)  

---

## 📂 Project Structure
├── app.py          # Main Streamlit application
├── aco.py          # Ant Colony Optimization logic
├── dijkstra.py     # Dijkstra shortest path
├── requirements.txt
└── README.md

---

## 🎮 How to Use

1. Set number of nodes and connectivity  
2. Choose start (nest) and end (food)  
3. Adjust ACO parameters  
4. Click **"Unleash the Ants 🚀"**  
5. Observe how ants learn the shortest path over time  

---

## 📊 Output

- Best path found by ACO  
- Optimal path using Dijkstra  
- Cost comparison  
- Learning curve graph  

---

## 🎯 Key Learnings

- Deterministic vs probabilistic algorithms  
- Exploration vs exploitation  
- Nature-inspired optimization  

---

## 🔥 Future Improvements

- Real-world map integration  
- Dynamic traffic simulation  
- Multi-objective optimization  
- Export results as reports  

---

## 👩‍💻 Author

**Simmi**  
BTech AIML Student  

---

## ⭐ Contribution

Feel free to fork and improve this project!

---

## 📌 Note

This project is created for educational purposes to help understand optimization algorithms visually.

