import matplotlib.pyplot as plt
import numpy as np


class Plot_Truss:
    """Class plot the truss with the member thickness propotional to the damage condition and to visualise the results"""

    cordinates = {1: [0, 0], 2: [4, 0], 3: [4, 3], 4: [8, 0], 5: [8, 3], 6: [12, 0]}

    elements = {
        1: [1, 2],
        2: [1, 3],
        3: [2, 3],
        4: [2, 4],
        5: [3, 4],
        6: [3, 5],
        7: [4, 5],
        8: [4, 6],
        9: [5, 6],
    }

    def __init__(self, damage_dict):
        self.damages = damage_dict

    def plotTruss(self):
        x = [i[0] for i in self.cordinates.values()]
        y = [i[1] for i in self.cordinates.values()]
        plt.figure(figsize=(12, 4))
        size = 600
        offset = size / 6000
        plt.scatter(x, y, c="#f1f3f5", s=size, zorder=5)
        for i, location in enumerate(zip(x, y)):
            plt.text(
                location[0] - offset,
                location[1] - offset,
                str(i + 1),
                fontsize=12,
                fontweight=600,
                zorder=10,
                color="#212529",
            )

        for element, nodenums in self.elements.items():
            fromnode = nodenums[0]
            tonode = nodenums[1]
            x1 = self.cordinates[fromnode][0]
            y1 = self.cordinates[fromnode][1]
            x2 = self.cordinates[tonode][0]
            y2 = self.cordinates[tonode][1]
            midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)
            print(midpoint)
            if (x2 - x1) == 0:
                angle = "vertical"
            else:
                angle = "horizontal"
                # angle = np.rad2deg(np.arctan((y1 - y2) / (x1 - x2)))
            plt.plot(
                [x1, x2],
                [y1, y2],
                color="#adb5bd",
                linestyle="-",
                linewidth=20 * (self.damages[element] - 1),
                zorder=1,
            )
            plt.text(
                midpoint[0],
                midpoint[1],
                f"{round(self.damages[element] * 100, 2)} % damage",
                rotation=angle,
                ha="center",
                va="center",
                fontsize=12,
                fontweight=600,
                color="#212529",
            )
        plt.axis("off")
        plt.savefig("static/images/damageplot.png", format="png", dpi=300)
        # plt.show()


