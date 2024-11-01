# -*- coding: utf-8 -*-
"""utils.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1573Wez04QKVulLL7k55i51NpoSHOwyFf
"""

# utils.py
import os
import logging
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns

class Logger:
    """Custom logger for the project."""
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logging
        self.logger = logging.getLogger('LungCancerAnalysis')
        self.logger.setLevel(logging.INFO)

        # Create file handler
        log_file = f'lung_cancer_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        fh = logging.FileHandler(os.path.join(log_dir, log_file))
        fh.setLevel(logging.INFO)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

def validate_data(df):
    """
    Validate dataset for required columns and data quality.
    
    Parameters:
    df (pandas.DataFrame): Input DataFrame
    
    Returns:
    tuple: (bool, list) - (is_valid, list of issues found)
    """
    issues = []
    required_columns = [
        'Age', 'Gender', 'Air Pollution', 'Smoking', 'Level'
    ]
    
    # Check required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        issues.append(f"Missing required columns: {missing_cols}")
    
    # Check for null values
    null_cols = df.columns[df.isnull().any()].tolist()
    if null_cols:
        issues.append(f"Columns with null values: {null_cols}")
    
    # Check data types
    if 'Age' in df.columns and not np.issubdtype(df['Age'].dtype, np.number):
        issues.append("Age column should be numeric")
    
    # Check value ranges
    if 'Age' in df.columns:
        if not df['Age'].between(0, 120).all():
            issues.append("Age values out of reasonable range (0-120)")
            
    if 'Gender' in df.columns:
        if not df['Gender'].isin([1, 2]).all():
            issues.append("Gender values should be 1 or 2")
            
    if 'Air Pollution' in df.columns:
        if not df['Air Pollution'].between(1, 10).all():
            issues.append("Air Pollution values out of range (1-10)")
            
    if 'Smoking' in df.columns:
        if not df['Smoking'].between(1, 8).all():
            issues.append("Smoking values out of range (1-8)")
    
    return len(issues) == 0, issues

def plot_roc_curves(models, X_test_scaled, y_test):
    """
    Plot ROC curves for all models.

    Parameters:
    models (dict): Dictionary of trained models
    X_test_scaled (array): Scaled test features
    y_test (array): Test labels
    """
    plt.figure(figsize=(10, 8))

    for name, model in models.items():
        if hasattr(model, "predict_proba"):
            probas = model.predict_proba(X_test_scaled)

            # Compute ROC curve and AUC for each class
            n_classes = len(np.unique(y_test))
            fpr = dict()
            tpr = dict()
            roc_auc = dict()

            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(
                    (y_test == i).astype(int),
                    probas[:, i]
                )
                roc_auc[i] = auc(fpr[i], tpr[i])

                plt.plot(
                    fpr[i],
                    tpr[i],
                    label=f'{name} (Class {i}, AUC = {roc_auc[i]:.2f})'
                )

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves for All Models')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.show()

def create_results_directory():
    """
    Create directory structure for saving results.

    Returns:
    str: Path to results directory
    """
    results_dir = 'results'
    subdirs = ['models', 'plots', 'reports', 'analysis']

    # Create main results directory
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Create subdirectories
    for subdir in subdirs:
        path = os.path.join(results_dir, subdir)
        if not os.path.exists(path):
            os.makedirs(path)

    return results_dir

def save_model_results(models, results_dir, X_test, y_test):
    """
    Save model results and performance metrics.

    Parameters:
    models (dict): Dictionary of trained models
    results_dir (str): Directory to save results
    X_test (array): Test features
    y_test (array): Test labels
    """
    results = []

    for name, model in models.items():
        y_pred = model.predict(X_test)

        # Calculate metrics
        report = classification_report(y_test, y_pred, output_dict=True)

        # Store results
        results.append({
            'model_name': name,
            'accuracy': report['accuracy'],
            'macro_avg_precision': report['macro avg']['precision'],
            'macro_avg_recall': report['macro avg']['recall'],
            'macro_avg_f1': report['macro avg']['f1-score']
        })

    # Create results DataFrame
    results_df = pd.DataFrame(results)

    # Save to CSV
    results_path = os.path.join(results_dir, 'reports', 'model_comparison.csv')
    results_df.to_csv(results_path, index=False)

    return results_df

def generate_summary_report(df, models, results_df, risk_profiles):
    """
    Generate a comprehensive analysis summary report.

    Parameters:
    df (pandas.DataFrame): Original dataset
    models (dict): Trained models
    results_df (pandas.DataFrame): Model comparison results
    risk_profiles (dict): Risk profiles from analysis

    Returns:
    str: Summary report text
    """
    report = []
    report.append("Lung Cancer Risk Analysis Summary Report")
    report.append("=" * 50)

    # Dataset Statistics
    report.append("\n1. Dataset Overview")
    report.append("-" * 20)
    report.append(f"Total number of patients: {len(df)}")
    report.append(f"Number of features: {len(df.columns) - 1}")
    report.append(f"Risk level distribution:")
    for level, count in df['Level'].value_counts().items():
        report.append(f"  - Level {level}: {count} patients ({count/len(df)*100:.1f}%)")

    # Model Performance
    report.append("\n2. Model Performance Summary")
    report.append("-" * 20)
    for _, row in results_df.iterrows():
        report.append(f"\n{row['model_name']}:")
        report.append(f"  - Accuracy: {row['accuracy']:.4f}")
        report.append(f"  - Macro Avg Precision: {row['macro_avg_precision']:.4f}")
        report.append(f"  - Macro Avg Recall: {row['macro_avg_recall']:.4f}")
        report.append(f"  - Macro Avg F1: {row['macro_avg_f1']:.4f}")

    # Risk Profiles
    report.append("\n3. Risk Level Characteristics")
    report.append("-" * 20)
    for level, profile in risk_profiles.items():
        report.append(f"\nRisk Level {level}:")
        report.append(f"  - Patient Count: {profile['count']}")
        report.append(f"  - Percentage: {profile['percentage']:.1f}%")

        # Top characteristics
        characteristics = profile['characteristics']
        top_features = sorted(
            characteristics.items(),
            key=lambda x: abs(x[1]['mean']),
            reverse=True
        )[:5]

        report.append("  - Key Characteristics:")
        for feature, stats in top_features:
            report.append(
                f"    * {feature}: mean={stats['mean']:.2f}, "
                f"std={stats['std']:.2f}"
            )

    return "\n".join(report)