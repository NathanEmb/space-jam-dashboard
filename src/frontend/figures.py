import math

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import src.constants as const


def create_cat_bar_charts(agg: pd.DataFrame) -> list[plt.Figure]:
    """Create a bar chart for each column in the DataFrame."""
    # Create a figure with subplots
    num_columns = len(agg.columns)
    root = np.ceil(math.sqrt(num_columns)).astype(int)
    fig, axes = plt.subplots(root, root, figsize=(15, 10), constrained_layout=True)

    # Plot each column as a bar chart in its own subplot
    colors = cm.viridis(np.linspace(0, 1, 3))  # You can use any colormap
    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            column_data = const.NINE_CATS[index]
            axes[i, j].bar(agg.index, agg[column_data], color=colors)  # Bar chart
            axes[i, j].set_title(column_data)  # Set title to column name
            axes[i, j].set_xticks(range(len(agg.index)))  # Position the ticks
            axes[i, j].set_xticklabels(agg.index, rotation=45)  # Rotate for readability
            axes[i, j].set_ylabel("Avg Per Game")  # Label for y-axis
    return fig
