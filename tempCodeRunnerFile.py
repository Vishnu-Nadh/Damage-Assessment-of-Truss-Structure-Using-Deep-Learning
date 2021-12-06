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