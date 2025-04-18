import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import heapq

NUM_SPECTRUM_SLOTS = 80
NUM_WAVELENGTHS = 4

class NetworkGraph:
    def _init_(self):
        self.graph = nx.Graph()
        self.slot_table = {}

    def add_node(self, node):
        self.graph.add_node(node)

    def add_edge(self, u, v, weight):
        self.graph.add_edge(u, v, weight=weight)
        key = tuple(sorted([u, v]))
        if key not in self.slot_table:
            self.slot_table[key] = [[False] * NUM_SPECTRUM_SLOTS for _ in range(NUM_WAVELENGTHS)]

    def get_path_weight(self, path):
        return sum(self.graph[u][v]['weight'] for u, v in zip(path, path[1:]))

    def display_graph(self, canvas):
        canvas.draw_graph(self.graph, self.slot_table)

    def reset(self):
        self.graph.clear()
        self.slot_table.clear()

    def allocate_slots(self, path, slots_needed, wavelength, allow_non_contiguous=False):
        if not path or slots_needed <= 0:
            return False, []

        edges = [tuple(sorted([path[i], path[i+1]])) for i in range(len(path) - 1)]

        for start in range(NUM_SPECTRUM_SLOTS - slots_needed + 1):
            if all(not any(self.slot_table[edge][wavelength][start:start+slots_needed]) for edge in edges):
                for edge in edges:
                    for i in range(start, start+slots_needed):
                        self.slot_table[edge][wavelength][i] = True
                return True, ['contiguous'] * len(edges)

        if allow_non_contiguous:
            available_slots = [
                set(i for i in range(NUM_SPECTRUM_SLOTS) if not self.slot_table[edge][wavelength][i])
                for edge in edges
            ]
            intersection = set.intersection(*available_slots)
            if len(intersection) >= slots_needed:
                slots = list(intersection)[:slots_needed]
                for edge in edges:
                    for i in slots:
                        self.slot_table[edge][wavelength][i] = True
                return True, ['non-contiguous'] * len(edges)

        return False, []

    def free_slots(self, path, wavelength):
        edges = [tuple(sorted([path[i], path[i+1]])) for i in range(len(path) - 1)]
        for edge in edges:
            self.slot_table[edge][wavelength] = [False] * NUM_SPECTRUM_SLOTS

    def dijkstra(self, start, end):
        distances = {node: float('inf') for node in self.graph.nodes()}
        distances[start] = 0
        prev = {}
        pq = [(0, start)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)
            if current_node == end:
                break
            for neighbor in self.graph.neighbors(current_node):
                weight = self.graph[current_node][neighbor]['weight']
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    prev[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        path, node = [], end
        while node in prev:
            path.insert(0, node)
            node = prev[node]
        if path:
            path.insert(0, node)
        return path

    def heuristic(self, u, v):
        return abs(hash(u) - hash(v)) % 10

    def astar(self, start, end):
        open_set = [(0, start)]
        came_from = {}
        g_score = {node: float('inf') for node in self.graph.nodes()}
        g_score[start] = 0
        f_score = {node: float('inf') for node in self.graph.nodes()}
        f_score[start] = self.heuristic(start, end)

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == end:
                break
            for neighbor in self.graph.neighbors(current):
                tentative_g = g_score[current] + self.graph[current][neighbor]['weight']
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        path, node = [], end
        while node in came_from:
            path.insert(0, node)
            node = came_from[node]
        if path:
            path.insert(0, node)
        return path

class GraphCanvas(tk.Frame):
    def _init_(self, parent):
        super()._init_(parent)
        self.figure = plt.Figure(figsize=(5, 5))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_graph(self, graph, slot_table):
        self.ax.clear()
        pos = nx.spring_layout(graph)
        edge_colors = []
        for u, v in graph.edges():
            key = tuple(sorted([u, v]))
            used = sum(sum(w) for w in slot_table[key])
            if used == 0:
                edge_colors.append('blue')
            elif used < NUM_SPECTRUM_SLOTS * NUM_WAVELENGTHS / 2:
                edge_colors.append('orange')
            elif used < NUM_SPECTRUM_SLOTS * NUM_WAVELENGTHS:
                edge_colors.append('pink')
            else:
                edge_colors.append('red')

        nx.draw(graph, pos, ax=self.ax, with_labels=True, edge_color=edge_colors, node_color='lightgreen', node_size=500)
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, ax=self.ax)
        self.canvas.draw()

class App:
    def _init_(self, root):
        self.root = root
        self.graph = NetworkGraph()

        self.canvas = GraphCanvas(root)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.panel = tk.Frame(root)
        self.panel.pack(side=tk.LEFT, fill=tk.Y)

        self.build_ui()

    def build_ui(self):
        ttk.Label(self.panel, text="Node:").pack()
        self.node_entry = ttk.Entry(self.panel)
        self.node_entry.pack()
        ttk.Button(self.panel, text="Add Node", command=self.add_node).pack()

        ttk.Label(self.panel, text="Edge (u v weight):").pack()
        self.edge_entry = ttk.Entry(self.panel)
        self.edge_entry.pack()
        ttk.Button(self.panel, text="Add Edge", command=self.add_edge).pack()

        ttk.Label(self.panel, text="Source:").pack()
        self.src_entry = ttk.Entry(self.panel)
        self.src_entry.pack()
        ttk.Label(self.panel, text="Destination:").pack()
        self.dst_entry = ttk.Entry(self.panel)
        self.dst_entry.pack()

        ttk.Label(self.panel, text="Slots Needed:").pack()
        self.slot_entry = ttk.Entry(self.panel)
        self.slot_entry.pack()

        self.contiguous_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.panel, text="Prefer Contiguous", variable=self.contiguous_var).pack()

        ttk.Label(self.panel, text="Wavelength:").pack()
        self.wavelength_var = tk.IntVar(value=0)
        self.wavelength_combo = ttk.Combobox(self.panel, textvariable=self.wavelength_var, values=list(range(NUM_WAVELENGTHS)), state="readonly")
        self.wavelength_combo.pack()

        ttk.Button(self.panel, text="Run All Paths & Allocate", command=self.run_all).pack()
        ttk.Button(self.panel, text="Free Slots", command=self.free_path).pack()
        ttk.Button(self.panel, text="Reset Graph", command=self.reset_graph).pack()

    def add_node(self):
        node = self.node_entry.get().strip()
        if node:
            self.graph.add_node(node)
            self.canvas.draw_graph(self.graph.graph, self.graph.slot_table)

    def add_edge(self):
        try:
            u, v, w = self.edge_entry.get().strip().split()
            self.graph.add_edge(u, v, int(w))
            self.canvas.draw_graph(self.graph.graph, self.graph.slot_table)
        except:
            messagebox.showerror("Invalid Input", "Enter edge as: node1 node2 weight")

    def run_all(self):
        src = self.src_entry.get().strip()
        dst = self.dst_entry.get().strip()
        try:
            slots_needed = int(self.slot_entry.get().strip())
        except:
            slots_needed = 0

        wavelength = self.wavelength_var.get()

        if not src or not dst:
            return

        results = {}
        for method in [('Dijkstra', self.graph.dijkstra), ('A*', self.graph.astar)]:
            start = time.time()
            path = method[1](src, dst)
            duration = time.time() - start
            results[method[0]] = (path, duration)

        summary = ""
        for algo, (path, dur) in results.items():
            alloc, types = self.graph.allocate_slots(path, slots_needed, wavelength, not self.contiguous_var.get())
            summary += f"{algo}: Path={path} | Time={dur:.4f}s | Allocation={'\u2705' if alloc else '\u274C'}\n"

        self.canvas.draw_graph(self.graph.graph, self.graph.slot_table)
        messagebox.showinfo("Results", summary)

    def free_path(self):
        src = self.src_entry.get().strip()
        dst = self.dst_entry.get().strip()
        wavelength = self.wavelength_var.get()
        path = self.graph.dijkstra(src, dst)
        self.graph.free_slots(path, wavelength)
        self.canvas.draw_graph(self.graph.graph, self.graph.slot_table)

    def reset_graph(self):
        self.graph.reset()
        self.canvas.draw_graph(self.graph.graph, self.graph.slot_table)

if _name_ == '_main_':
    root = tk.Tk()
    root.title("Graph Visualization & WDM Slot Allocation")
    app = App(root)
    root.mainloop()
