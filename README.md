##🔌 Optical Signal Optimization using WDM Slot Allocation

This project provides a graphical simulation for Wavelength Division Multiplexing (WDM)-based optical networks. It enables dynamic graph creation, shortest path calculation using Dijkstra's and A* algorithms, and spectrum slot allocation over multiple wavelengths.

Built using Python, Tkinter for GUI, and NetworkX + Matplotlib for graph visualization.

🚀 Features
📈 Visual graph builder (nodes, weighted edges)

🧠 Pathfinding using Dijkstra's and A* algorithms

🌐 Slot allocation using contiguous and non-contiguous spectrum slots

🌈 Supports multiple wavelengths (default: 4)

❌ Slot freeing and full graph reset

🔍 Slot usage visualization with edge color coding

🖼️ Demo Screenshot

🧰 Installation
Clone the repository

bash
Copy
Edit
git clone https://github.com/YourUsername/optical-wdm-slot-allocation.git
cd optical-wdm-slot-allocation
Create virtual environment (optional but recommended)

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install required packages

bash
Copy
Edit
pip install -r requirements.txt
📦 Requirements
Make sure the following packages are installed:

nginx
Copy
Edit
tk
matplotlib
networkx
You can install them manually if requirements.txt is missing:

bash
Copy
Edit
pip install matplotlib networkx
💡 How It Works
Launch the app.

Add nodes and edges (format: u v weight).

Enter source, destination, slots required, and wavelength index.

Run both Dijkstra and A* algorithms for path finding.

Allocate slots — contiguous preferred by default (toggle available).

Visual feedback with edge color coding based on slot utilization:

🔵 Blue → unused

🟠 Orange → partially used

💗 Pink → heavily used

🔴 Red → fully used

You can free slots or reset the graph anytime.

⚙️ Configuration
Spectrum Slots: 80 (default)

Wavelengths: 4

Adjustable from constants in the code:

python
Copy
Edit
NUM_SPECTRUM_SLOTS = 80
NUM_WAVELENGTHS = 4
📊 Algorithms Used
Dijkstra's Algorithm – for shortest weighted path.

A* Search Algorithm – with a hash-based heuristic.

📚 References
WDM Technology – Wikipedia

NetworkX Documentation

Dijkstra’s Algorithm – GeeksforGeeks

A* Algorithm – GeeksforGeeks
