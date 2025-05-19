# 🔌 Optical Signal Optimization using WDM Slot Allocation

This project provides a graphical simulation for **Wavelength Division Multiplexing (WDM)**-based optical networks. It enables dynamic graph creation, shortest path calculation using **Dijkstra's** and **A\*** algorithms, and **spectrum slot allocation** over multiple wavelengths.

Built using **Python**, **Tkinter** for GUI, and **NetworkX** + **Matplotlib** for graph visualization.

---

## 🚀 Features

- 📈 Visual graph builder (nodes, weighted edges)
- 🧠 Pathfinding using **Dijkstra's** and **A\*** algorithms
- 🌐 Slot allocation using contiguous and non-contiguous spectrum slots
- 🌈 Supports multiple **wavelengths** (default: 4)
- ❌ Slot freeing and full graph reset
- 🔍 Slot usage visualization with edge color coding

---

## 🖼️ Demo Screenshot

![WDM Slot Allocation GUI](path/to/screenshot.png)

> Replace `path/to/screenshot.png` with your actual image path (e.g., `assets/demo.png`)

---
##💡 How It Works

Launch the GUI.

Add nodes and edges (node1 node2 weight).

Set source, destination, slots required, and wavelength index.

Run Dijkstra and A* pathfinding.

Allocate slots – contiguous preferred (can be toggled).

View edge color coding:

🔵 Blue → unused

🟠 Orange → partially used

💗 Pink → heavily used

🔴 Red → fully used

Options to free slots or reset the graph.

---
##📊 Algorithms Used

Dijkstra's Algorithm: Classic shortest path finder for weighted graphs.

A* Search Algorithm: Heuristic-driven pathfinding.

Each run displays:

Path found

Time taken

Whether slot allocation was successful

