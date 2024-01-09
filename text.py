

class Text:

    def __init__(self):
        self.german = True

    def greeting(self):
        return "Herzlich Willkommen!\n\nWähle Level 1, um das Spiel zu beginnen." if self.german else \
            "Welcome!\n\nSelect level 1 to start the game."

    def click_to_start(self):
        return "Klicke, um zu starten" if self.german else \
            "Click to start"

    def click_to_continue(self):
        return "Klicke, um weiter zu spielen" if self.german else \
            "Click to continue playing"

    def all_obj_recognized(self):
        return "Sehr gut!\nAlle Objekte wurden richtig erkannt!" if self.german else \
            "Excellent!\nAll objects were detected correctly!"

    def tutorial_start(self):
        return "Das Ziel dieses Spieles ist es, die Netzwerke zu zerschneiden, sodass\n"\
               "möglichst viele blaue und möglichst wenig grüne Linen geschnitten werden.\n"\
               "Dieses Level ist eine Anleitung. Klicke, um zu starten." if self.german else \
            "The goal of the game is to cut the networks into multiple parts,\n"\
            "such that as many blue lines and as few green lines as possible\n"\
            "are cut. This level is a tutorial. Click to begin."

    def tutorial_first_cut(self):
        return "Ziehe von links nach\nrechts über die blaue Line,\num diese zu schneiden.\n" if self.german else \
            "Drag the mouse across\nthe blue line to cut it."

    def tutorial_plus_point(self):
        return "Das Schneiden von blauen\nLinien gibt einen Pluspunkt.\n" \
               "Die Gesamtpunktzahl wird\noben angezeigt.\n" \
               "Klicke, um fortzufahren" if self.german else \
            "Cutting a blue line gives\none plus point.\n" \
            "The total number of points\nis displayed on top.\n" \
            "Click to continue."

    def tutorial_second_cut(self):
        return "Schneide nun die grüne Linie.\nDas gibt einen Minuspunkt." if self.german else \
            "Now, cut the green line.\nThis gives a minus point."

    def tutorial_first_join(self):
        return "Durch einen Doppelklick\nauf die Line wird diese\nwieder verbunden." if self.german else \
            "By a double click on this\nline, it gets reconnected."

    def tutorial_false_cut(self):
        return "Versuche nun diese\nblaue Linie zu schneiden." if self.german else \
            "Now, try to cut\bthis blue line."

    def tutorial_info_false_cut(self):
        return "Das Schneiden einer Linie\nist ungültig, wenn das Netzwerk\ndadurch nicht geteilt wird.\n" \
               "Klicke, um fortzufahren." if self.german else \
            "Cutting a line is not valid\nif the network is not split\ninto two parts.\nClick to continue."

    def tutorial_correct_cut(self):
        return "Um dieses Netzwerk zu\nteilen, müssen zwei Linien\n" \
               "gleichzeitig geschnitten werden." if self.german else \
            "To split this network\ninto two, two lines need to\nbe cut simultaneously."

    def tutorial_bad_cut(self):
        return "Manchmal kann eine blaue Line nur geschnitten\nwerden, indem auch grüne Linien geschnitten\n" \
               "werden. Schneide die drei mit den Pfeilen\nmarkierten Linien." if self.german else \
            "Sometimes, a blue line can only\nbe cut by also cutting green lines.\n" \
            "Cut the three lines that are\nmarked by the arrows."

    def tutorial_re_join(self):
        return "Das gab einen Plus- und zwei Minuspunkte.\nDurch einen Doppelklick auf eine der Linien,\n"\
               "werden diese wieder verbunden" if self.german else \
            "This gave one plus and two minus points.\nBy double clicking on one of the lines,\nthe lines will be " \
            "reconnected."

    def tutorial_good_cut(self):
        return "Dieses Netzwerk kann geteilt werden, indem zwei\n"\
               "blaue und eine grüne Linie geschnitten werden.\n"\
               "Das gibt zwei Plus- und einen Minuspunkt.\n"\
               "Zusammen gerechnet also einen Pluspunkt" if self.german else \
            "This network can be split into two by\n" \
            "cutting two blue and one green line.\n" \
            "This gives two plus and one minus point.\n" \
            "Together, this gives one plus point."

    def tutorial_next_level(self):
        return "Wähle unten das nächste Level aus." if self.german else \
            "Select the next level below."

    def congrats(self):
        return "Glückwunsch!\nDu hast eine optimale Lösung gefunden!" if self.german else \
            "Congratulations!\nYou have found an optimal solution!"

    def tree_first_cut(self):
        return "Schneide die fünf unteren blauen Linien. Dafür erhälst du fünf Pluspunkte." if self.german else \
            "Cut the bottom five blue lines. For this, you get five plus points."

    def tree_second_cut(self):
        return "Schneide als nächstes die mit den Pfeilen markierten Linien.\n" \
               "Für diesen Schnitt erhälst du sechs Plus- und einen Minuspunkt." if self.german else \
            "Next, cut the lines that are marked with the arrows.\n" \
            "For this cut you get six plus and one minus point."

    def tree_third_cut(self):
        return "Sehr gut! Schneide als nächstes diese beiden Linien." if self.german else \
            "Excellent! Next, cut these two lines."

    def tree_fourth_cut(self):
        return "Schneide nun diese Linien um drei Plus- und einen Minuspunkt zu erhalten." if self.german else \
            "Now, cut these lines to get three plus and one minus point."

    def tree_join(self):
        return "Verbinde nun die markierte Line mit einem Doppelklick.\n" \
               "Dafür erhälst du einen Pluspunkt." if self.german else \
            "Now, reconnect the marked line with a double click.\n" \
            "For this you get one plus point."

    def click_to_show_img(self):
        return "Klicke auf das Bild Symbol unten links, um das Ergebnis zu sehen." if self.german else \
            "Click on the image icon in the bottom left to see the result."

    def try_without_help(self):
        return "Versuche dieses Level eigenständig zu Lösen.\n"\
               "Wenn du einen Tip benötigst kannst du auf die Glühbirne unten links klicken.\n" if self.german else \
            "Try to solves this Level without help.\n" \
            "If you need a hint you can click on the lightbulb in the bottom left."

    def click_to_compute_segments_tree(self):
        return "In diesem Level helfen wir dem Computer die Objekte in diesem\n" \
               "Bild zu erkennen. Wir Menschen sehen in diesem Bild einen Baum\n" \
               "der auf einer Wiese steht mit einem blauen Himmel im Hintergrund.\n" \
               "Für einen Computer ist ein digitales Bild nur eine Ansammlung von\n" \
               "Nullen und Einsen. Um die Objekte in diesem Bild zu erkennen,\n" \
               "kann der Computer wie folgt vorgehen: Als Erstes wird das Bild in\n" \
               "viele Segmente zerlegt. (Klicke zum Fortfahren)" if self.german else \
            "In this level, we help the computer to recognize the objects\n" \
            "in this image. We humans see a tree that is standing in a meadow\n" \
            "in front of a blue sky. For a computer, a digital image is just\n" \
            "a set of zeros and ones. To recognize the objects in this image\n" \
            "the computer may proceed as follows: Firstly, the image gets\n" \
            "decomposed into multiple segments. (Click to continue)"

    def click_to_compute_network_tree(self):
        return "Als Nächstes werden die Segmente zu einem Netzwerk\n" \
               "miteinander verbunden. (Klicke zum Fortfahren)" if self.german else \
            "Next up, the segments are connected together to\n" \
            "create a network. (Click to continue)"

    def click_to_start_playing_tree(self):
        return "Nun kann das Multicut Problem gelöst werden, um zu entscheiden,\n" \
               "welche Segmente zum gleichen Objekt gehören und welche Segmente\n" \
               "zu verschiedenen Objekten gehören. (Klicke zum Fortfahren)" if self.german else \
            "Now, the multicut problem can be solved to decide which segments\n" \
            "belong to the same object and which segments belong to different\n" \
            "objects (Click to continue)"

    def connectomics_description(self):
        return "Dies ist ein kleiner Ausschnitt von einem Elektronenmikroskopie Bild\n" \
               "von dem neuronalen Gewebe des Maus Neocortex welches vom Lichtman Lab\n" \
               "an der Harvard Universität aufgenommen wurde. Das Lösen des Multicut\n" \
               "Problems kann dabei helfen die einzelen Zellen in diesem Bild\n" \
               "automatisiert zu erkennen. Klicke, um zu starten" if self.german else \
            "This is a small section of an electron microscopy image of neural\n" \
            "tissue from the mouse neocortex which was obtained by the Lichtman\n" \
            "Lab at the Harvard university. Solving the multicut problem can help\n" \
            "with automatically identifying the individual cells in this image.\n" \
            "Click to start."
