# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1573Wez04QKVulLL7k55i51NpoSHOwyFf
"""

# main.py

from config import *
from data_preprocessing import load_data, preprocess_data
from outlier_detection import detect_and_plot_outliers
from model_training import train_models, evaluate_models
from visualization import plot_feature_distributions, plot_correlation_matrix, plot_dendrogram
from treatment_analysis import TreatmentAnalyzer
from treatment_optimization import TreatmentOptimizer, visualize_treatment_timeline, analyze_treatment_results

def main():
    # Load and preprocess data
    df = load_data('lung_cancer.csv')
    X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, scaler, X = preprocess_data(df)

    # Detect outliers
    numeric_columns = X.select_dtypes(include=[np.number]).columns.tolist()
    print("\nPerforming Outlier Analysis...")
    outliers = detect_and_plot_outliers(X, numeric_columns)

    # Create visualizations
    plot_feature_distributions(X)
    plot_correlation_matrix(X)
    plot_dendrogram(X)

    # Train and evaluate models
    models = train_models(X_train_scaled, y_train)
    evaluate_models(models, X_test_scaled, y_test, X)

    # Initialize treatment optimization
    print("\nInitializing Treatment Optimization System...")
    optimizer = TreatmentOptimizer()

    # Example patient data
    patient_factors = {
        'age': 65,
        'general_health': 7,
        'resilience': 6,
        'support_system': 8
    }

    # Example baseline QoL
    baseline_qol = {
        'physical_mobility': 8,
        'physical_pain': 7,
        'physical_fatigue': 8,
        'emotional_anxiety': 6,
        'functional_daily_activities': 7
    }

    # Define treatments
    treatments = ['Surgery', 'Chemotherapy', 'Radiation', 'Immunotherapy']

    # Optimize treatment timing
    print("\nOptimizing treatment schedule...")
    schedule, total_duration = optimizer.optimize_treatment_timing(
        treatments,
        patient_factors,
        start_date=datetime.now()
    )

    # Calculate QoL impact
    print("\nCalculating quality of life impact...")
    qol_scores = optimizer.calculate_qol_impact(schedule, patient_factors, total_duration)

    # Analyze QoL components
    print("\nAnalyzing QoL components...")
    qol_components = optimizer.analyze_qol_components(baseline_qol, schedule)

    # Generate visualizations
    print("\nGenerating visualizations...")
    visualize_treatment_timeline(optimizer, schedule, qol_scores)

    # Generate and print analysis report
    report = analyze_treatment_results(schedule, qol_scores, qol_components)
    print("\n" + report)

if __name__ == "__main__":
    main()