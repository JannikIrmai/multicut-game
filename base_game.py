import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


# remove the keymap
for key in plt.rcParams:
    if "keymap." in key:
        plt.rcParams[key] = []
# remove the toolbar
plt.rcParams['toolbar'] = 'None'


class BaseGame:

    def __init__(self, graph: nx.Graph, ax: plt.Axes = None, **kwargs):

        # assert that the graph is correct
        for n in graph.nodes:
            if not isinstance(n, int) or not 0 <= n < graph.number_of_nodes():
                pass
                # raise ValueError(f"The nodes of the graph have to be integers from 0 to {graph.number_of_nodes()}-1.")

        # attributes that describe the graph and the current clustering
        self._graph = graph.copy()

        # create figure and axis
        if ax is not None:
            self._ax = ax
            self._fig = ax.get_figure()
        else:
            self._fig, self._ax = plt.subplots()
        self._ax.set_aspect('equal')

        # parameters that describe the size of the different objects in the plot
        self._node_radius = kwargs.get('node_radius', 0.1)
        self._default_line_width = 2
        self._line_width_weight_factor = 2

        # list of interactive functions
        self._interactive_functions = []

        # the objective value of the current solution
        self._obj = 0
        self._opt_callback = kwargs.get("opt_callback", None)

        # handle for the popup text
        self._popup_handle = None

        self.congrats_text = None
        self.font_size = "large"

    def deactivate(self):
        # this method removes the interactive functions from the figure such that the user can no longer interact with
        # the plot.
        while len(self._interactive_functions) > 0:
            f = self._interactive_functions.pop()
            self._fig.canvas.mpl_disconnect(f)

    def set_ax_lim(self):
        # compute the min and max x and y coordinates of the node positions
        pos = np.array([self._graph.nodes[i]['pos'] for i in self._graph.nodes])
        min_coord = np.min(pos, axis=0)
        max_coord = np.max(pos, axis=0)

        min_coord -= self._node_radius * 10
        max_coord += self._node_radius * 10
        self._ax.set_xlim(min_coord[0], max_coord[0])
        self._ax.set_ylim(min_coord[1], max_coord[1])

    def make_popup(self, text: str = None, **kwargs):
        if self._popup_handle is not None:
            self._popup_handle.remove()
            self._popup_handle = None
        if text is None:
            return
        # get the center of the axis
        x = (self._ax.get_xlim()[0] + self._ax.get_xlim()[1]) / 2
        y = (self._ax.get_ylim()[0] + self._ax.get_ylim()[1]) / 2
        if "fontsize" not in kwargs:
            kwargs["fontsize"] = self.font_size
        self._popup_handle = self._ax.text(x, y, text, va='center', ha='center', zorder=10000,
                                           bbox={'facecolor': [1, 1, 1, 0.8], 'edgecolor': 'black'}, **kwargs)
