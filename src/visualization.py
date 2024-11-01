# -*- coding: utf-8 -*-
"""visualization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1573Wez04QKVulLL7k55i51NpoSHOwyFf
"""

# visualization.py
from config import *

def plot_feature_distributions(data):
    """Plot distribution of all features."""
    plt.figure(figsize=(20, 15))
    num_cols = len(data.columns[:-1])
    num_rows = (num_cols + 3) // 4

    for i, col in enumerate(data.columns[:-1], 1):
        plt.subplot(num_rows, 4, i)
        sns.histplot(data=data, x=col, bins=3)
        plt.title(f'Distribution of {col}')

    plt.tight_layout()
    plt.show()

def plot_correlation_matrix(data):
    """Plot correlation matrix."""
    plt.figure(figsize=(15, 12))
    sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Feature Correlation Matrix')
    plt.show()

def plot_dendrogram(data):
    """Plot feature clustering dendrogram."""
    plt.figure(figsize=(12, 8))
    linkage_matrix = hierarchy.linkage(data.iloc[:, :-1].corr(), method='ward')
    dendrogram_labels = data.columns[:-1]
    hierarchy.dendrogram(linkage_matrix, labels=dendrogram_labels, leaf_rotation=90)
    plt.title('Feature Clustering Dendrogram')
    plt.tight_layout()
    plt.show()