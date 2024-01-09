import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent, MouseButton
from matplotlib.patches import Circle, Polygon
from colors import *
import numpy as np
from matplotlib.colors import ListedColormap
from base_game import BaseGame
from random import shuffle


def check_intersection(x_0, y_0, x_1, y_1, x_2, y_2, x_3, y_3):
    """
    This method checks whether the line from point (x_0, y_0) to (x_1, y_1) intersects the line from (x_2, y_2) to
    (x_3, y_3).
    https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
    """
    d = ((x_0 - x_1) * (y_2 - y_3) - (y_0 - y_1) * (x_2 - x_3))
    if d == 0:
        return False
    t = ((x_0 - x_2) * (y_2 - y_3) - (y_0 - y_2) * (x_2 - x_3)) / d
    u = ((x_0 - x_2) * (y_0 - y_1) - (y_0 - y_2) * (x_0 - x_1)) / d
    return 0 <= t <= 1 and 0 <= u <= 1


class MulticutGame(BaseGame):

    def __init__(self, graph: nx.Graph, ax: plt.Axes, **kwargs):
        super().__init__(graph, ax, **kwargs)

        # attributes that keep track of the graph and the clustering
        self._cut_graph = graph.copy()
        self._node_to_cluster = {node: 0 for node in self._graph}
        self._clustering = {0: [node for node in self._graph]}

        # attributes that describe the appearance of the plot
        self._cm = ListedColormap(["tab:red", "tab:cyan", "gold", "darkblue", "tab:orange"])
        self._pos_color = scads_green
        self._neg_color = scads_blue
        self._zero_color = "gray"
        self._cut_line_color = scads_gray

        self._width_cut_factor = 0.5
        self._width_connected_factor = 1.5

        # the line that makes the cut
        self._line = None
        # selected node for drag and drop to rearrange layout
        self._selected_node = None
        self.locked_layout = False  # If true, the nodes cannot be moved to new position

        # compute the optimal solution value
        self._opt = 0
        for u, v in self._graph.edges:
            if self._graph[u][v]['solution'] > 0.5:
                self._opt += self._graph[u][v]['weight']

        self._hint_handle = None

        self.tutorial_steps = None
        self.tutorial_step = None
        self._step_text_handle = None
        self._step_overlay_handles = []
        self._step_arrow_handles = []

        self.point_handles = []

    def remove_handles(self):
        self.make_popup(None)
        for i in self._graph.nodes:
            try:
                self._graph.nodes[i]['handle'].remove()
            except (KeyError, ValueError):
                pass
        for i, j in self._graph.edges:
            try:
                self._graph[i][j]['handle'].remove()
            except (KeyError, ValueError):
                pass
        if self._hint_handle is not None:
            self._hint_handle.remove()
            self._hint_handle = None
        self.remove_point_handles()
        self.remove_tutorial_step()

    def remove_point_handles(self):
        for handle in self.point_handles:
            handle.remove()
        self.point_handles.clear()

    def reset(self):
        self.remove_handles()

        # draw the nodes
        for node in self._graph.nodes:
            circle = Circle(self._graph.nodes[node]['pos'], radius=self._node_radius, zorder=1,
                            edgecolor='black')
            self._ax.add_artist(circle)
            self._graph.nodes[node]['handle'] = circle

        # draw the edges
        self._obj = 0
        for u, v in self._graph.edges:
            w = self._graph[u][v]['weight']
            x_u, y_u = self._graph.nodes[u]['handle'].center
            x_v, y_v = self._graph.nodes[v]['handle'].center
            width = self._default_line_width + abs(w) * self._line_width_weight_factor
            color = self._neg_color if w < 0 else self._pos_color if w > 0 else \
                self._zero_color
            is_cut = self._node_to_cluster[u] != self._node_to_cluster[v]
            line = self._ax.plot([x_u, x_v], [y_u, y_v], zorder=0,
                                 linewidth=width * (self._width_cut_factor if is_cut else self._width_connected_factor),
                                 color=color, linestyle=":" if is_cut else "-")
            if is_cut:
                self._obj += w
            self._graph[u][v]['handle'] = line[0]

        self._color_nodes()
        self._update_score()

        self.tutorial_step = 0

    def show_tutorial_step(self):
        if self.tutorial_steps is None:
            return

        self.remove_tutorial_step()
        if self.tutorial_step >= len(self.tutorial_steps):
            return
        step = self.tutorial_steps[self.tutorial_step]
        self._step_text_handle = self._ax.text(*step["text_pos"], step["text"](), va='center', ha='center',
                                               zorder=10000, fontsize=self.font_size)
        for edge in step["edges"]:
            self._step_arrow_handles.append(self.get_arrow_to_edge(edge))
        for overlay in step.get("overlay", []):
            handle = Polygon(overlay, color="white", zorder=3)
            self._ax.add_artist(handle)
            self._step_overlay_handles.append(handle)

    def remove_tutorial_step(self):
        if self._step_text_handle is not None:
            self._step_text_handle.remove()
        self._step_text_handle = None
        for handle in self._step_arrow_handles:
            handle.remove()
        self._step_arrow_handles.clear()
        for handle in self._step_overlay_handles:
            handle.remove()
        self._step_overlay_handles.clear()

    def play(self):
        # connect functions to figure that make it interactive
        self._interactive_functions = [
            self._fig.canvas.mpl_connect("button_press_event", self._on_click),
            self._fig.canvas.mpl_connect("button_release_event", self._on_release),
            self._fig.canvas.mpl_connect("motion_notify_event", self._on_move),
        ]

        self.reset()
        self.show_tutorial_step()

    def _color_nodes(self):
        # get a coloring of the component graph
        component_graph = nx.Graph()
        component_graph.add_nodes_from(self._clustering.keys())
        for u, v in self._graph.edges:
            if self._node_to_cluster[u] != self._node_to_cluster[v]:
                component_graph.add_edge(self._node_to_cluster[u], self._node_to_cluster[v])
        coloring = nx.greedy_color(component_graph)

        for u in self._graph.nodes:
            self._graph.nodes[u]["handle"].set(facecolor=self._cm(coloring[self._node_to_cluster[u]] % self._cm.N))

    def _update_clustering(self):
        components = nx.connected_components(self._cut_graph)
        self._clustering.clear()
        self._node_to_cluster.clear()
        for i, comp in enumerate(components):
            self._clustering[i] = comp
            for u in comp:
                self._node_to_cluster[u] = i

    def _add_cut(self, xy: np.ndarray):
        # find the edges that were not previously cut but are cut by the line xy
        new_cut = []
        for u, v in self._cut_graph.edges:
            x_u, y_u = self._graph.nodes[u]['handle'].center
            x_v, y_v = self._graph.nodes[v]['handle'].center
            for i in range(1, xy.shape[0]):
                if check_intersection(x_u, y_u, x_v, y_v, xy[i - 1, 0], xy[i - 1, 1], xy[i, 0], xy[i, 1]):
                    new_cut.append((u, v))
                    break
        if self.tutorial_steps is not None and self.tutorial_step < len(self.tutorial_steps):
            if set(new_cut) != set(self.tutorial_steps[self.tutorial_step]["edges"]):
                return
            else:
                self.tutorial_step += 1
                self.show_tutorial_step()
        self._cut_graph.remove_edges_from(new_cut)
        self._update_clustering()
        self._color_nodes()
        # update edges that are now cut
        for u, v in new_cut:
            if self._node_to_cluster[u] == self._node_to_cluster[v]:
                self._cut_graph.add_edge(u, v)
            else:
                w = self._graph[u][v]['weight']
                width = (self._default_line_width + abs(w) * self._line_width_weight_factor) * self._width_cut_factor
                self._graph[u][v]["handle"].set(linewidth=width, linestyle=":")
                self._obj += w
                self._show_edge_points(u, v)
        self._update_score()

    def _join_components(self, x, y):
        # check if x, y lies on an edge
        edge = None
        for u, v in self._graph.edges:
            if self._node_to_cluster[u] == self._node_to_cluster[v]:
                continue
            x_u, y_u = self._graph.nodes[u]['handle'].center
            x_v, y_v = self._graph.nodes[v]['handle'].center
            # compute the distance of x, y to the line trough u and v
            dist = abs((x_v - x_u) * (y_u - y) - (x_u - x) * (y_v - y_u))
            dist /= ((x_v - x_u) ** 2 + (y_v - y_u) ** 2) ** 0.5
            if dist > self._node_radius:
                continue
            if ((x - x_u) ** 2 + (y - y_u) ** 2) ** 0.5 + ((x - x_v) ** 2 + (y - y_v) ** 2) ** 0.5 > \
                    ((x_v - x_u) ** 2 + (y_v - y_u) ** 2) ** 0.5 + self._node_radius:
                continue
            edge = (u, v)
            break
        if edge is None:
            return
        if self.tutorial_steps is not None and self.tutorial_step < len(self.tutorial_steps):
            if [edge] != self.tutorial_steps[self.tutorial_step]["edges"]:
                return
            else:
                self.tutorial_step += 1
                self.show_tutorial_step()
        # join the clusters that are connected by the edge
        c_1 = self._node_to_cluster[edge[0]]
        c_2 = self._node_to_cluster[edge[1]]
        if c_1 == c_2:
            return
        for u, v in self._graph.edges:
            if {self._node_to_cluster[u], self._node_to_cluster[v]} == {c_1, c_2}:
                self._cut_graph.add_edge(u, v)
                w = self._graph[u][v]["weight"]
                self._obj -= w
                width = (self._default_line_width + abs(w) * self._line_width_weight_factor) * \
                    self._width_connected_factor
                self._graph[u][v]["handle"].set(linewidth=width, linestyle="-")
                self._show_edge_points(u, v)
        for node in self._clustering[c_2]:
            self._node_to_cluster[node] = c_1
        self._clustering.pop(c_2)
        self._color_nodes()
        self._update_score()

    def _show_edge_points(self, u, v):
        xu, yu = self._graph.nodes[u]["handle"].center
        xv, yv = self._graph.nodes[v]["handle"].center
        x = (xu + xv) / 2
        y = (yu + yv) / 2
        w = self._graph[u][v]["weight"]
        change = w if self._cut_graph.has_edge(u, v) else -w
        string = str(change) if change < 0 else f"+{change}"
        bbox_color = [1, 1, 1, 0.8]
        self.point_handles.append(
            self._ax.text(x, y, string, va="center", ha="center",
                          bbox={'facecolor': bbox_color, "edgecolor": bbox_color, "boxstyle": "circle"}))

    def _update_score(self):
        self._ax.set_title(f"Score: {-self._obj} / {-self._opt}")
        # make pop up if optimal solution is found
        self.make_popup(self.congrats_text if self._opt == self._obj else None)
        if self._obj == self._opt and self._opt_callback is not None:
            try:
                self._opt_callback()
            except Exception as e:
                print("Callback failed", e)

    def _on_click(self, event: MouseEvent):
        if event.button != MouseButton.LEFT:
            return
        if event.inaxes != self._ax:
            return
        self.make_popup(None)
        self.remove_point_handles()

        if self.tutorial_steps is not None \
                and self.tutorial_step < len(self.tutorial_steps) \
                and self.tutorial_steps[self.tutorial_step].get("is_info", False):
            self.tutorial_step += 1
            self.show_tutorial_step()

        if self._hint_handle is not None:
            self._hint_handle.remove()
            self._hint_handle = None

        self._select_node(event.xdata, event.ydata, event.dblclick)
        if self._selected_node is not None:
            pass
        elif event.dblclick:
            if self._line is not None:
                self._line.remove()
                self._line = None
            self._join_components(event.xdata, event.ydata)
        else:
            self._line = self._ax.plot([event.xdata], [event.ydata], color=self._cut_line_color, zorder=4)[0]

        self._fig.canvas.draw_idle()

    def _on_release(self, event: MouseEvent):
        if event.button != MouseButton.LEFT:
            return
        if self._selected_node is not None:
            self._graph.nodes[self._selected_node]["handle"].set(linewidth=1)
            self._selected_node = None
        if self._line is not None:
            self._add_cut(self._line.get_xydata())
            self._line.remove()
            self._line = None

        self._fig.canvas.draw_idle()

    def _on_move(self, event: MouseEvent):
        if event.inaxes != self._ax:
            return
        if self._line is not None:
            xy = self._line.get_xydata()
            xy = np.concatenate([xy, [[event.xdata, event.ydata]]], axis=0)
            self._line.set(xdata=xy[:, 0], ydata=xy[:, 1])
        elif self._selected_node is not None:
            self._set_selected_node_pos(event.xdata, event.ydata)
        else:
            return
        self._fig.canvas.draw_idle()

    def _set_selected_node_pos(self, x, y):
        self._graph.nodes[self._selected_node]["handle"].set(center=(x, y))
        for u in self._graph[self._selected_node]:
            xu, yu = self._graph.nodes[u]["handle"].center
            self._graph[self._selected_node][u]["handle"].set_xdata([x, xu])
            self._graph[self._selected_node][u]["handle"].set_ydata([y, yu])

    def _select_node(self, x, y, double_click):
        if self.locked_layout:
            return
        if self._selected_node is not None:
            return
        for node in self._graph.nodes:
            handle = self._graph.nodes[node]["handle"]
            xn, yn = handle.center
            if (x - xn) ** 2 + (y - yn) ** 2 <= handle.radius ** 2:
                self._selected_node = node
                break
        if self._selected_node is None:
            return
        if double_click:
            self._set_selected_node_pos(*self._graph.nodes[self._selected_node]["pos"])
            self._selected_node = None
        else:
            self._graph.nodes[self._selected_node]["handle"].set(linewidth=2)

    def get_clustering(self):
        # This method returns the current clustering
        return self._node_to_cluster.copy()

    def give_hint(self):
        if self._popup_handle is not None:
            return
        if self._hint_handle is not None:
            self._hint_handle.remove()
            self._hint_handle = None
        # search for hint edge
        hint_edge = None
        edges = list(self._graph.edges)
        shuffle(edges)
        for u, v in edges:
            is_cut = not self._cut_graph.has_edge(u, v)
            is_cut_in_opt = self._graph[u][v]["solution"] > 0.5
            if is_cut != is_cut_in_opt:
                hint_edge = (u, v)
                break
        if hint_edge is None:
            return
        self._hint_handle = self.get_arrow_to_edge(hint_edge)
        self._fig.canvas.draw_idle()

    def get_arrow_to_edge(self, edge):
        # draw arrow pointing to edge
        u, v = edge
        xu, yu = self._graph.nodes[u]["handle"].center
        xv, yv = self._graph.nodes[v]["handle"].center
        x = (xu + xv) / 2
        y = (yu + yv) / 2

        dx, dy = xu - xv, yu - yv
        norm = (dx**2 + dy**2)**0.5
        dx *= self._node_radius / norm
        dy *= self._node_radius / norm

        return self._ax.arrow(x-6*dy, y+6*dx, 5*dy, -5*dx, width=self._node_radius, length_includes_head=True,
                              head_length=3*self._node_radius, color="black", zorder=2)

    def reset_layout_animation(self, steps=24, duration=1):
        if all(self._graph.nodes[n]["pos"] == self._graph.nodes[n]["handle"].center for n in self._graph.nodes):
            return

        start_pos = {n: self._graph.nodes[n]["handle"].center for n in self._graph.nodes}
        support = np.linspace(0, 1, steps)
        support = 0.5 * (1 + np.sin((support * np.pi) - (np.pi / 2)))
        for t in support:
            for n in self._graph.nodes:
                xs, ys = start_pos[n]
                xe, ye = self._graph.nodes[n]["pos"]
                self._graph.nodes[n]["handle"].set(center=(t*xe + (1-t)*xs, t*ye + (1-t)*ys))
            for u, v in self._graph.edges:
                xu, yu = self._graph.nodes[u]["handle"].center
                xv, yv = self._graph.nodes[v]["handle"].center
                self._graph[u][v]["handle"].set_xdata([xu, xv])
                self._graph[u][v]["handle"].set_ydata([yu, yv])
            plt.pause(duration / steps)
