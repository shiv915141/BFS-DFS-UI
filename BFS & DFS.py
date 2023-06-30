#!/usr/bin/env python
# coding: utf-8

# In[82]:


import tkinter as tk
from tkinter import messagebox

class GraphUI:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.bfs_result = []
        self.dfs_result = []
        self.graph_type = None

        self.root = tk.Tk()
        self.root.title("Graph UI")
        self.canvas = tk.Canvas(self.root, width=1000, height=600, background="light blue")
        self.canvas.pack()

        # Choose Graph Type Buttons
        self.graph_type_frame = tk.Frame(self.root)
        self.graph_type_frame.place(x=220, y=10)
        self.directed_button = tk.Button(self.graph_type_frame, text="Directed Graph",
                                         command=lambda: self.choose_graph_type('directed'))
        self.directed_button.grid(row=0, column=0, padx=250, pady=10)

        self.undirected_button = tk.Button(self.graph_type_frame, text="Undirected Graph",
                                           command=lambda: self.choose_graph_type('undirected'))
        self.undirected_button.grid(row=0, column=1, padx=250, pady=10)

        # Choose Vertices Button
        self.vertices_button = tk.Button(self.root, text="Choose Vertices", command=self.choose_vertices)
        self.vertices_button.place(x=35, y=150)

        # Join Vertices Button
        self.join_button = tk.Button(self.root, text="Join Vertices", command=self.join_vertices)
        self.join_button.place(x=35, y=400)

        # Apply BFS Button
        self.bfs_button = tk.Button(self.root, text="Apply BFS", command=self.apply_bfs)
        self.bfs_button.place(x=700, y=650)

        # Apply DFS Button
        self.dfs_button = tk.Button(self.root, text="Apply DFS", command=self.apply_dfs)
        self.dfs_button.place(x=800, y=650)

        self.counter = 1  # Vertex counter
        self.selected_vertex = None

        self.root.mainloop()

    def choose_graph_type(self, graph_type):
        self.graph_type = graph_type
        messagebox.showinfo("Graph Type", f"Graph type selected: {graph_type.capitalize()}")

    def choose_vertices(self):
        if self.graph_type is None:
            messagebox.showwarning("Graph Type", "Please select the graph type first.")
            return

        messagebox.showinfo("Choose Vertices", "Click on the canvas to add vertices")

        self.canvas.bind("<Button-1>", self.add_vertex)

    def add_vertex(self, event):
        x = event.x
        y = event.y
        vertex = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        self.vertices.append((x, y, vertex, self.counter))
        self.canvas.create_text(x, y - 10, text=str(self.counter), fill="black")
        self.counter += 1

    def join_vertices(self):
        if self.graph_type is None:
            messagebox.showwarning("Graph Type", "Please select the graph type first.")
            return

        messagebox.showinfo("Join Vertices", "Click and drag to join two vertices")

        self.canvas.bind("<Button-1>", self.select_vertex)
        self.canvas.bind("<B1-Motion>", self.connect_vertices)
        self.canvas.bind("<ButtonRelease-1>", self.deselect_vertex)

    def select_vertex(self, event):
        x = event.x
        y = event.y
        for vertex in self.vertices:
            vx, vy, v, label = vertex
            if abs(vx - x) <= 5 and abs(vy - y) <= 5:
                self.selected_vertex = vertex
                break

    def connect_vertices(self, event):
        if self.selected_vertex:
            x = event.x
            y = event.y
            self.canvas.delete("line")
            self.canvas.create_line(self.selected_vertex[0], self.selected_vertex[1], x, y, fill="black", tags="line")

    def deselect_vertex(self, event):
        if self.selected_vertex:
            x = event.x
            y = event.y
            for vertex in self.vertices:
                vx, vy, v, label = vertex
                if abs(vx - x) <= 5 and abs(vy - y) <= 5:
                    if vertex != self.selected_vertex:
                        if self.graph_type == 'undirected':
                            self.edges.append((self.selected_vertex[3], label))
                            self.canvas.delete("line")
                            self.canvas.create_line(self.selected_vertex[0], self.selected_vertex[1], vx, vy,
                                                    fill="black")
                        elif self.graph_type == 'directed':
                            self.edges.append((self.selected_vertex[3], label))
                            self.canvas.delete("line")
                            self.canvas.create_line(self.selected_vertex[0], self.selected_vertex[1], vx, vy,
                                                    fill="black", arrow=tk.LAST)
                    break
            self.selected_vertex = None

    def apply_bfs(self):
        if self.graph_type is None:
            messagebox.showwarning("Graph Type", "Please select the graph type first.")
            return

        if not self.vertices:
            messagebox.showwarning("No Vertices", "Please choose vertices before applying BFS.")
            return

        messagebox.showinfo("BFS Result", "Applying BFS...")

        # Perform BFS on the graph (using self.vertices and self.edges)
        start_vertex = self.vertices[0]  # Assuming the first vertex is the starting point
        visited = set()
        queue = [(start_vertex, 0)]  # Use a queue of tuples (vertex, level)
        self.bfs_result = []

        while queue:
            vertex, level = queue.pop(0)
            self.bfs_result.append((vertex, level))
            visited.add(vertex)

            # Find the neighbors of the current vertex
            neighbors = [edge[1] for edge in self.edges if edge[0] == vertex[3]]

            # Add unvisited neighbors to the queue
            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in [v[0] for v in queue]:
                    queue.append((self.get_vertex_by_label(neighbor), level + 1))

        # Display the result
        result_str = "BFS Result:\n"
        for vertex, level in self.bfs_result:
            result_str += f"Vertex: {vertex[3]}, Level: {level}\n"
        messagebox.showinfo("BFS Result", result_str)

    def apply_dfs(self):
        if self.graph_type is None:
            messagebox.showwarning("Graph Type", "Please select the graph type first.")
            return

        if not self.vertices:
            messagebox.showwarning("No Vertices", "Please choose vertices before applying DFS.")
            return

        messagebox.showinfo("DFS Result", "Applying DFS...")

        # Perform DFS on the graph (using self.vertices and self.edges)
        start_vertex = self.vertices[0]  # Assuming the first vertex is the starting point
        visited = set()
        stack = [(start_vertex, 0)]  # Use a stack of tuples (vertex, level)
        self.dfs_result = []

        while stack:
            vertex, level = stack.pop()
            self.dfs_result.append((vertex, level))
            visited.add(vertex)

            # Find the neighbors of the current vertex
            neighbors = [edge[1] for edge in self.edges if edge[0] == vertex[3]]

            # Add unvisited neighbors to the stack
            for neighbor in neighbors:
                if neighbor not in visited and neighbor not in [v[0] for v in stack]:
                    stack.append((self.get_vertex_by_label(neighbor), level + 1))

        # Display the result
        result_str = "DFS Result:\n"
        for vertex, level in self.dfs_result:
            result_str += f"Vertex: {vertex[3]}, Level: {level}\n"
        messagebox.showinfo("DFS Result", result_str)

    def get_vertex_by_label(self, label):
        for vertex in self.vertices:
            if vertex[3] == label:
                return vertex

if __name__ == "__main__":
    graph_ui = GraphUI()


# In[ ]:




