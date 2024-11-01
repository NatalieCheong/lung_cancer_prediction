# -*- coding: utf-8 -*-
"""outlier_detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1573Wez04QKVulLL7k55i51NpoSHOwyFf
"""

# outlier_detection.py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from config import *

def detect_and_plot_outliers(df, numeric_columns):
    """Detect and visualize outliers using IQR method."""
    outliers_dict = {}

    # Create a figure for box plots
    n_cols = 3
    n_rows = (len(numeric_columns) + n_cols - 1) // n_cols
    fig = plt.figure(figsize=(15, 5 * n_rows))

    for idx, column in enumerate(numeric_columns, 1):
        # Calculate Q1, Q3, and IQR
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        # Define outlier boundaries
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Find outliers
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)][column]
        outliers_dict[column] = outliers.index.tolist()

        # Create subplot
        plt.subplot(n_rows, n_cols, idx)
        sns.boxplot(x=df[column])

        if len(outliers) > 0:
            plt.scatter(outliers, [0] * len(outliers),
                       color='red', label='Outliers', alpha=0.5)

        plt.title(f'Box Plot of {column}\n({len(outliers)} outliers)')
        plt.xlabel(column)

    plt.tight_layout()
    plt.show()

    print("\nOutlier Summary:")
    for column in numeric_columns:
        n_outliers = len(outliers_dict[column])
        if n_outliers > 0:
            print(f"{column}: {n_outliers} outliers detected")
            print(f"Outlier values: {df.loc[outliers_dict[column], column].tolist()}\n")

    return outliers_dict