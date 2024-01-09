import matplotlib.pyplot as plt
from multicut_game import MulticutGame
from colors import *
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.widgets import Button
import numpy as np
import networkx as nx
import pickle
from text import Text


class Game:

    text = Text()

    levels = [
        {
            "filename": "instances/tutorial_instance.pickle",
            "node_radius": 0.1,
            "lock_layout": True,
            "ax_limits": [-2, 8, -1, 7],
            "tutorial_steps": [
                {"edges": [], "is_info": True,
                 "text": text.tutorial_start,
                 "text_pos": (3, 6.6)},
                {"edges": [(0, 1)],
                 "overlay": [((-0.5, -0.5), (6.5, -0.5), (6.5, 6.5), (1, 6.5), (1, 3), (-0.5, 3))],
                 "text": text.tutorial_first_cut,
                 "text_pos": (0, 3.4)},
                {"edges": [], "is_info": True,
                 "overlay": [((-0.5, -0.5), (6.5, -0.5), (6.5, 6.5), (1, 6.5), (1, 3), (-0.5, 3))],
                 "text": text.tutorial_plus_point,
                 "text_pos": (0, 3.4)},
                {"edges": [(2, 3)],
                 "overlay": [((-0.5, -0.5), (6.5, -0.5), (6.5, 6.5), (3, 6.5), (3, 3), (-0.5, 3))],
                 "text": text.tutorial_second_cut,
                 "text_pos": (2, 3.4)},
                {"edges": [(2, 3)],
                 "overlay": [((-0.5, -0.5), (6.5, -0.5), (6.5, 6.5), (3, 6.5), (3, 3), (-0.5, 3))],
                 "text": text.tutorial_first_join,
                 "text_pos": (2, 3.4)},
                {"edges": [(4, 5)],
                 "overlay": [((-0.5, -0.5), (6.5, -0.5), (6.5, 3), (-0.5, 3))],
                 "text": text.tutorial_false_cut,
                 "text_pos": (4, 3.4)},
                {"edges": [], "is_info": True,
                 "overlay": [((-0.5, -0.5), (6.5, -0.5), (6.5, 3), (-0.5, 3))],
                 "text": text.tutorial_info_false_cut,
                 "text_pos": (5, 3.4)},
                {"edges": [(4, 5), (6, 7)],
                 "overlay": [((-0.5, -0.5), (6.5, -0.5), (6.5, 3), (-0.5, 3))],
                 "text": text.tutorial_correct_cut,
                 "text_pos": (5, 3.4)},
                {"edges": [(8, 9), (8, 10), (8, 11)],
                 "overlay": [((3, -0.5), (6.5, -0.5), (6.5, 3), (3, 3))],
                 "text": text.tutorial_bad_cut,
                 "text_pos": (1, -0.6)},
                {"edges": [(8, 9)],
                 "overlay": [((3, -0.5), (6.5, -0.5), (6.5, 3), (3, 3))],
                 "text": text.tutorial_re_join,
                 "text_pos": (1, -0.6)},
                {"edges": [(12, 13), (12, 14), (12, 15)],
                 "text": text.tutorial_good_cut,
                 "text_pos": (5, -0.6)},
                {"edges": [],
                 "text": text.tutorial_next_level,
                 "text_pos": (3, -0.6)}
            ]
        },
        {
            "filename": "instances/tree_tutorial_instance.pickle",
            "node_radius": 0.05,
            "lock_layout": True,
            "tutorial_steps": [
                {"edges": [(15, 20), (16, 21), (17, 22), (18, 23), (19, 24)],
                 "text": text.tree_first_cut,
                 "text_pos": (2, 4.3)},
                {"edges": [(1, 2), (2, 7), (7, 8), (8, 13), (13, 14), (13, 18), (17, 18)],
                 "text": text.tree_second_cut,
                 "text_pos": (2, 4.3)},
                {"edges": [(12, 17), (16, 17)],
                 "text": text.tree_third_cut,
                 "text_pos": (2, 4.3)},
                {"edges": [(6, 7), (6, 11), (10, 11), (11, 16)],
                 "text": text.tree_fourth_cut,
                 "text_pos": (2, 4.3)},
                {"edges": [(1, 2)],
                 "text": text.tree_join,
                 "text_pos": (2, 4.3)}
            ],
            "start_steps": [text.click_to_compute_segments_tree, text.click_to_compute_network_tree,
                            text.click_to_start_playing_tree]
        },
        {
            "filename": "instances/tree_instance.pickle",
            "node_radius": 10,
            "tutorial_steps": [
                {"edges": [], "is_info": True,
                 "text": text.try_without_help,
                 "text_pos": (500, 60)}
            ],
        },
        {
            "filename": "instances/frauenkirche_instance.pickle",
            "node_radius": 30,
            "tutorial_steps": [
                {"edges": [], "is_info": True,
                 "text": text.try_without_help,
                 "text_pos": (1000, 100)}
            ],
        },
        {
            "filename": "instances/connectomics_instance.pickle",
            "node_radius": 3,
            "start_text": text.connectomics_description
        }
    ]

    def __init__(self):
        # This method creates a game instance. It consists of a figure with two axes, one for the buttons and one for
        # playing the game.

        self.fig = plt.figure(figsize=(18, 12))
        self.fig.canvas.manager.full_screen_toggle()
        self.fig.tight_layout()

        # create game axis
        self.game_ax = self.fig.add_axes([0.18, 0.12, 0.64, 0.84])
        self.game_ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        # put scads logo in top right
        logo = plt.imread("icons/scads_logo_tiny.png")
        self.scads_logo_ax = self.fig.add_axes([0.83, 0.83, 0.16, 0.16])
        self.scads_logo_ax.set_axis_off()
        self.scads_logo_ax.imshow(logo)

        # put multicut logo in top left
        logo = plt.imread("icons/multicut-game-logo.png")
        self.game_logo_ax = self.fig.add_axes([0.01, 0.83, 0.16, 0.16])
        self.game_logo_ax.set_axis_off()
        self.game_logo_ax.imshow(logo)

        # create button for displaying the image
        image_icon = plt.imread("icons/image.png")
        self.display_ax = self.fig.add_axes([0.02, 0.03, 0.06, 0.06])
        self.display_button = Button(self.display_ax, "", image_icon)
        self.display_button.on_clicked(self.on_display_image)

        # create hint button
        lightbulb_icon = plt.imread("icons/lightbulb.png")
        self.hint_ax = self.fig.add_axes([0.1, 0.03, 0.06, 0.06])
        self.hint_button = Button(self.hint_ax, "", lightbulb_icon)
        self.hint_button.on_clicked(self.give_hint)

        # create level buttons
        level_icon = plt.imread("icons/level.png")
        self.level_ax = self.fig.add_axes([0.2, 0.03, 0.12, 0.06])
        self.level_ax.set_axis_off()
        self.level_ax.imshow(level_icon)
        self.level_buttons = []
        self.level_axis = []
        for i in range(len(self.levels)):
            num_icon = plt.imread(f"icons/{i+1}.png")
            ax = self.fig.add_axes([0.32 + i * 0.08, 0.03, 0.06, 0.06])
            button = Button(ax, "", num_icon)
            button.on_clicked(self.on_select_level)
            self.level_buttons.append(button)
            self.level_axis.append(ax)

        # create an exit button
        self.exit_ax = self.fig.add_axes([0.92, 0.03, 0.06, 0.06])
        exit_icon = plt.imread("icons/leave.png")
        self.exit_button = Button(self.exit_ax, "", exit_icon)
        self.exit_button.on_clicked(lambda arg: plt.close(self.fig))

        # create a language button
        self.language_ax = self.fig.add_axes([0.84, 0.03, 0.06, 0.06])
        self.english_icon = plt.imread("icons/english-flag.png")
        self.german_icon = plt.imread("icons/german-flag.png")
        self.language_button_image_handle = self.language_ax.imshow(
            self.english_icon if self.text.german else self.german_icon)
        self.language_button = Button(self.language_ax, "")
        self.language_button.on_clicked(self.change_language)

        self.game = None
        self.selected_level = 0

        self.img = None
        self.img_copy = None
        self.segmentation = None
        self.segment_lines = None
        self.cut_lines = None
        self.labels = None

        self.img_handle = None
        self.segmentation_handle = None
        self.segment_line_handles = {}
        self.cut_line_handles = {}
        self.continue_play_cid = None

        self.start_step = None

        self.locked = False

        self.fig.canvas.mpl_connect("button_press_event", self.on_click)

        # handle for the popup text
        self._popup_handle = None
        self.font_size = 10
        self.make_popup(self.text.greeting(), fontsize=2*self.font_size)

    def change_language(self, event: MouseEvent):
        self.text.german = not self.text.german
        self.language_button_image_handle.set(data=self.english_icon if self.text.german else self.german_icon)
        if self.game is not None:
            self.game.congrats_text = self.text.congrats() if self.img is None else \
                self.text.congrats() + "\n\n" + self.text.click_to_show_img()
            if self.img_handle is None:
                self.game.show_tutorial_step()
        else:
            self.make_popup(self.text.greeting(), fontsize=2*self.font_size)
        self.fig.canvas.draw_idle()

    def make_popup(self, message: str = None, **kwargs):
        if self._popup_handle is not None:
            self._popup_handle.remove()
            self._popup_handle = None
        if message is None:
            return
        # get the center of the axis
        x = (self.game_ax.get_xlim()[0] + self.game_ax.get_xlim()[1]) / 2
        y = (self.game_ax.get_ylim()[0] + self.game_ax.get_ylim()[1]) / 2
        if "fontsize" not in kwargs:
            kwargs["fontsize"] = self.font_size
        self._popup_handle = self.game_ax.text(x, y, message, va='center', ha='center', zorder=10000, **kwargs)

    def on_select_level(self, event: MouseEvent):
        if self.locked:
            return
        self.make_popup(None)
        self.level_buttons[self.selected_level].color = "0.85"
        self.selected_level = self.level_axis.index(event.inaxes)
        self.level_buttons[self.selected_level].color = my_green
        self.reset_level()

    def on_click(self, event: MouseEvent):
        if event.button != MouseButton.LEFT:
            return
        if event.inaxes != self.game_ax:
            return
        if self.start_step is None:
            return
        if self.locked:
            return
        self.locked = True

        def show_segments():
            if self.img is None:
                return
            update_steps = max(1, int(len(self.labels) / 10))
            self.img_copy = self.img.copy()
            cm = plt.get_cmap("tab10")
            for i, lab in enumerate(self.labels):
                msk = self.segmentation == lab
                self.img_copy[msk] = self.img[msk] * 0.8 + np.array(cm(i % 10)) * 255 * 0.2
                self.segment_line_handles[lab] = self.game_ax.plot(*self.segment_lines[lab], color="black", zorder=4,
                                                                   linewidth=3)[0]
                if (i + 1) % update_steps == 0:
                    self.img_handle.set(data=self.img_copy)
                    plt.pause(0.1)

        def show_network():
            update_steps = max(1, int(len(self.labels) / 10))
            for i, lab in enumerate(self.labels):
                self.img_copy[self.segmentation == lab] = 0
                self.segment_line_handles[lab].remove()
                if (i + 1) % update_steps == 0:
                    self.img_handle.set(data=self.img_copy)
                    plt.pause(0.2)

            self.img_handle.remove()
            self.img_handle = None
            self.segment_line_handles = {}

        if "start_steps" in self.levels[self.selected_level]:
            if self.start_step == 0:
                self.make_popup(self.levels[self.selected_level]["start_steps"][0]())
                self.start_step = 1
            elif self.start_step == 1:
                self.make_popup(None)
                show_segments()
                self.make_popup(self.levels[self.selected_level]["start_steps"][1]())
                self.start_step = 2
            elif self.start_step == 2:
                self.make_popup(None)
                show_network()
                self.make_popup(self.levels[self.selected_level]["start_steps"][2](),
                                bbox={'color': my_blue4, 'alpha': 0.85})
                self.start_step = 3
            else:
                self.make_popup(None)
                self.game.play()
                self.start_step = None
        else:
            self.make_popup(None)
            show_segments()
            show_network()
            self.game.play()
            self.start_step = None

        self.fig.canvas.draw_idle()
        self.locked = False

    def give_hint(self, event: MouseEvent):
        if event.button != MouseButton.LEFT:
            return
        if self.locked:
            return
        if self.game is None:
            return
        self.game.give_hint()

    def on_reset_button(self, event: MouseEvent):
        if event.button != MouseButton.LEFT:
            return
        self.reset_level()

    def remove_handles(self):
        if self.game is not None:
            self.game.remove_handles()
        if self.img_handle is not None:
            self.img_handle.remove()
            self.img_handle = None
        for handle in self.segment_line_handles.values():
            handle.remove()
        self.segment_line_handles = {}
        for lines in self.cut_line_handles.values():
            for handle in lines:
                handle.remove()
        self.cut_line_handles = {}
        self.make_popup(None)
        if self.continue_play_cid is not None:
            self.fig.canvas.mpl_disconnect(self.continue_play_cid)

    def reset_level(self):
        if self.locked:
            return
        self.remove_handles()

        with open(self.levels[self.selected_level]["filename"], "rb") as file:
            data = pickle.load(file)

        g = nx.Graph()
        for v, pos in data["nodes"].items():
            g.add_node(v, pos=pos)
        for (u, v), cost in data["edges"].items():
            g.add_edge(u, v, weight=cost, solution=data["solution"][(u, v)])

        if "img" in data:
            self.img = data["img"]
            self.segmentation = data["segmentation"]
            self.segment_lines = data["lines"]
            self.cut_lines = data["cut_lines"]

            self.labels = np.unique(self.segmentation)
            np.random.shuffle(self.labels)

            self.img = np.concatenate([self.img, np.ones(self.img.shape[:2] + (1,), dtype=int) * 255], axis=-1)
            self.img_handle = self.game_ax.imshow(self.img, zorder=3)
            self.game_ax.set_xlim((-0.5, self.img.shape[1] - 0.5))
            self.game_ax.set_ylim((self.img.shape[0] - 0.5, -0.5))

            start_text = self.levels[self.selected_level].get("start_text", self.text.click_to_start)()
            self.make_popup(start_text, fontsize=self.font_size, bbox={'color': my_blue4, 'alpha': 0.5})
            self.start_step = 0
        else:
            self.img = None
            self.start_step = None

        self.game = MulticutGame(g, self.game_ax, node_radius=self.levels[self.selected_level]["node_radius"])
        self.game.font_size = self.font_size
        self.game.locked_layout = self.levels[self.selected_level].get("lock_layout", False)
        self.game.congrats_text = self.text.congrats() if self.img is None else \
            self.text.congrats() + "\n\n" + self.text.click_to_show_img()

        tutorial_steps = self.levels[self.selected_level].get("tutorial_steps", None)
        if tutorial_steps is not None:
            self.game.tutorial_steps = tutorial_steps

        self.game.reset()

        if self.img is None:
            self.game_ax.set_xlim(*self.levels[self.selected_level]["ax_limits"][:2])
            self.game_ax.set_ylim(*self.levels[self.selected_level]["ax_limits"][2:])
            self.game.play()

        self.fig.canvas.draw_idle()

    def on_display_image(self, event: MouseEvent):
        if event.button != MouseButton.LEFT:
            return
        self.display_image()

    def display_image(self):
        if self.locked:
            return
        if self.img_handle is not None:
            return
        self.locked = True
        self.game.remove_point_handles()
        self.game.remove_tutorial_step()
        self.game.make_popup(None)
        self.game.reset_layout_animation()
        node2cluster = self.game.get_clustering()

        if self.img is None:
            self.locked = False
            return

        num_cuts = 0
        for u, v in self.cut_lines:
            num_cuts += node2cluster[u] != node2cluster[v]

        for u, v in self.cut_lines:
            if node2cluster[u] == node2cluster[v]:
                continue
            self.cut_line_handles[(u, v)] = []
            for line in self.cut_lines[(u, v)]:
                self.cut_line_handles[(u, v)].append(self.game_ax.plot(*line, color="black", zorder=4, linewidth=4)[0])
                plt.pause(1 / num_cuts)

        cluster2nodes = {}
        for n, c in node2cluster.items():
            if c not in cluster2nodes:
                cluster2nodes[c] = set()
            cluster2nodes[c].add(n)

        img = np.zeros_like(self.img)
        self.img_handle = self.game_ax.imshow(img, zorder=3)
        clusters = np.array(list(cluster2nodes.keys()))
        np.random.shuffle(clusters)
        update_steps = max(1, int(len(clusters) / 10))
        for i, c in enumerate(clusters):
            cm = plt.get_cmap("tab10")
            for lab in cluster2nodes[c]:
                msk = self.segmentation == lab
                img[msk] = self.img[msk] * 0.8 + np.array(cm(c % 10)) * 255 * 0.2
                img[msk, -1] = 255*0.9
            if (i + 1) % update_steps == 0:
                self.img_handle.set(data=img)
                plt.pause(0.1)
        self.fig.canvas.draw_idle()

        self.game.make_popup(self.text.click_to_continue() if self.game._opt != self.game._obj else
                             self.text.all_obj_recognized())

        def continue_play(mouse_event: MouseEvent):
            if mouse_event.button != MouseButton.LEFT:
                return
            if mouse_event.inaxes != self.game_ax:
                return
            if self.locked:
                return
            self.locked = True
            self.game.show_tutorial_step()
            self.fig.canvas.mpl_disconnect(self.continue_play_cid)

            self.img_handle.remove()
            self.img_handle = None
            for lines in self.cut_line_handles.values():
                for line_handle in lines:
                    line_handle.remove()
            self.cut_line_handles = {}
            self.fig.canvas.draw_idle()
            self.locked = False

        self.continue_play_cid = self.fig.canvas.mpl_connect("button_press_event", continue_play)

        self.locked = False


if __name__ == "__main__":
    while True:
        demo = Game()
        plt.show()

# TODO: Better start screen! Start with level 1 and show dragging animation.
# TODO: Maybe better layout? I.e. make the game axis the size of the entire figure and adjust the x and y limits
#  accordingly.
