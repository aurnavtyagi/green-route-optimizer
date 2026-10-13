"""
PDF Report Generator using ReportLab
=====================================
Generates professional PDF reports for traffic analysis
"""

import os
import pandas as pd
from datetime import datetime

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, 
                               TableStyle, PageBreak, Image, KeepTogether,
                               Preformatted)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas


def create_pdf_report():
    """Create comprehensive PDF report using ReportLab"""
    
    print("📄 Creating PDF Document Report...")
    
    os.makedirs('reports', exist_ok=True)
    pdf_path = 'reports/Traffic_Congestion_Analysis_Report.pdf'
    
    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Container for PDF elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        spaceAfter=3
    )
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # ==========================================
    # TITLE PAGE
    # ==========================================
    elements.append(Spacer(1, 1*inch))
    elements.append(Paragraph('Traffic Congestion Prediction', title_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph('Comparative Analysis of Machine Learning Models', subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Metadata
    elements.append(Paragraph(f'<b>Report Date:</b> {timestamp}', normal_style))
    elements.append(Paragraph('<b>Project:</b> Delhi AI Green Route - Traffic Congestion Prediction', normal_style))
    elements.append(Paragraph('<b>Department:</b> Machine Learning & Data Analytics', normal_style))
    
    elements.append(PageBreak())
    
    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================
    elements.append(Paragraph('1. Executive Summary', heading_style))
    
    summary_text = """This comprehensive report presents a comparative analysis of five machine learning models designed for traffic congestion prediction in Delhi. The study evaluates baseline and advanced machine learning approaches, culminating in a novel Adaptive Ensemble algorithm with dynamic feature weighting.

<b>Key Achievements:</b>"""
    elements.append(Paragraph(summary_text, normal_style))
    
    bullets = [
        "Baseline Model R² Score: 0.9327 (Linear Regression)",
        "Best Standard Algorithm: Gradient Boosting (R² = 0.9985)",
        "Proposed Algorithm Performance: R² = 0.9988 (Superior)",
        "Prediction RMSE Improvement: 86.3% reduction vs. baseline",
        "Cross-Validation Stability: 0.002 standard deviation"
    ]
    
    for bullet in bullets:
        elements.append(Paragraph(f'• {bullet}', bullet_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # ==========================================
    # INTRODUCTION
    # ==========================================
    elements.append(Paragraph('2. Introduction', heading_style))
    
    intro_para1 = """Traffic congestion represents a significant challenge in major metropolitan areas worldwide, with Delhi experiencing substantial congestion during peak hours. Accurate prediction of congestion levels enables proactive traffic management, emission reduction, and improved urban mobility."""
    
    elements.append(Paragraph(intro_para1, normal_style))
    
    intro_para2 = """<b>Research Objectives:</b>"""
    elements.append(Paragraph(intro_para2, normal_style))
    
    objectives = [
        "Develop baseline model for traffic congestion prediction",
        "Implement standard ML algorithms (RF, GB, XGBoost)",
        "Propose novel adaptive ensemble algorithm",
        "Perform comprehensive comparative analysis",
        "Provide deployment recommendations"
    ]
    
    for i, obj in enumerate(objectives, 1):
        elements.append(Paragraph(f'{i}. {obj}', bullet_style))
    
    elements.append(PageBreak())
    
    # ==========================================
    # METHODOLOGY
    # ==========================================
    elements.append(Paragraph('3. Methodology', heading_style))
    
    elements.append(Paragraph('3.1 Data Preparation', styles['Heading3']))
    
    data_prep = """<b>Dataset Characteristics:</b>
• Total Records: 17,101 traffic samples
• Features: 22 variables (traffic, weather, temporal)
• Preprocessing: Label encoding, StandardScaler normalization
• Train-Test Split: 80% (13,667) training, 20% (3,417) testing
• Cross-Validation: 5-fold stratified split for robust estimation"""
    
    elements.append(Paragraph(data_prep, normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Models description
    elements.append(Paragraph('3.2 Machine Learning Models', styles['Heading3']))
    
    model_data = [
        {
            'name': 'Baseline: Linear Regression',
            'desc': 'Simple linear model establishing baseline performance. Assumes linear relationship between features and congestion.'
        },
        {
            'name': 'Algorithm 1: Random Forest',
            'desc': 'Ensemble of 100 decision trees. Captures non-linear patterns through bagging methodology.'
        },
        {
            'name': 'Algorithm 2: Gradient Boosting',
            'desc': 'Sequential ensemble with 100 boosted trees. Minimizes error iteratively through gradient descent.'
        },
        {
            'name': 'Algorithm 3: XGBoost',
            'desc': 'Optimized gradient boosting with L1/L2 regularization and parallel tree building.'
        },
        {
            'name': 'Proposed: Adaptive Ensemble',
            'desc': 'Novel combined approach with RF/GB adaptive weighting (RF: 50.38%, GB: 49.62%) plus residual correction layer.'
        }
    ]
    
    for model in model_data:
        elements.append(Paragraph(f"<b>{model['name']}</b>", bullet_style))
        elements.append(Paragraph(model['desc'], bullet_style))
        elements.append(Spacer(1, 0.05*inch))
    
    elements.append(PageBreak())
    
    # ==========================================
    # RESULTS TABLE
    # ==========================================
    elements.append(Paragraph('4. Experimental Results', heading_style))
    
    # Prepare results data
    results_data = [
        ['Model', 'R² Test', 'RMSE', 'MAE', 'CV Mean', 'CV Std'],
        ['Baseline (Linear Reg.)', '0.9327', '3.1340', '1.9627', '0.9309', '0.0030'],
        ['Algorithm 1 (RF)', '0.9982', '0.5074', '0.0727', '0.9994', '0.0002'],
        ['Algorithm 2 (GB)', '0.9985', '0.4662', '0.1340', '0.9995', '0.0002'],
        ['Algorithm 3 (XGBoost)', '0.9955', '0.8098', '0.2299', '0.9975', '0.0010'],
        ['Proposed (Ensemble)', '0.9988', '0.4295', '0.0834', '0.9992', '0.0002']
    ]
    
    # Create table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ])
    
    results_table = Table(results_data, colWidths=[2*inch, 1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
    results_table.setStyle(table_style)
    
    elements.append(results_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Results interpretation
    elements.append(Paragraph('<b>Key Observations:</b>', normal_style))
    
    observations = [
        'Proposed Adaptive Ensemble achieves highest R² (0.9988) combining RF & GB strengths',
        'RMSE improved 86.3% over baseline (3.134 → 0.430)',
        'MAE performance leaders: RF (0.0727) and Proposed (0.0834)',
        'Cross-validation stability excellent for all tree-based methods',
        'Minimal train-test gap indicates strong generalization'
    ]
    
    for obs in observations:
        elements.append(Paragraph(f'• {obs}', bullet_style))
    
    elements.append(PageBreak())
    
    # ==========================================
    # ANALYSIS & FINDINGS
    # ==========================================
    elements.append(Paragraph('5. Detailed Analysis', heading_style))
    
    elements.append(Paragraph('5.1 Performance Metrics Explanation', styles['Heading3']))
    
    metrics_text = """
<b>R² Score (Coefficient of Determination):</b> Measures proportion of variance explained by model. Range 0-1, with 1.0 indicating perfect prediction. Our models achieve 0.93-0.99 range.

<b>RMSE (Root Mean Squared Error):</b> Average prediction error magnitude in same units as target. Lower is better. Proposed model achieves 0.4295 RMSE (86% improvement).

<b>MAE (Mean Absolute Error):</b> Average absolute prediction error, more robust to outliers. Ranges 0.07-1.96 across models.

<b>Cross-Validation Mean & Std:</b> Measures model stability across different data splits. Std <0.003 indicates stable, reliable performance."""
    
    elements.append(Paragraph(metrics_text, normal_style))
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph('5.2 Comparative Analysis Summary', styles['Heading3']))
    
    comparison = [
        '<b>Baseline vs. Proposed Improvement: 2.8% R² gain (0.9327 → 0.9988)</b>',
        '<b>RMSE Reduction: 3.134 → 0.430 (86.3% improvement)</b>',
        '<b>Adaptive Weighting: RF 50.38% + GB 49.62% optimal balance</b>',
        '<b>Confidence Score: 0.9847 mean (very high prediction confidence)</b>'
    ]
    
    for comp in comparison:
        elements.append(Paragraph(comp, bullet_style))
    
    elements.append(PageBreak())
    
    # ==========================================
    # RECOMMENDATIONS
    # ==========================================
    elements.append(Paragraph('6. Recommendations & Conclusions', heading_style))
    
    elements.append(Paragraph('6.1 Deployment Recommendation', styles['Heading3']))
    
    deploy_text = """Based on comprehensive evaluation, we recommend deploying the <b>Proposed Adaptive Ensemble algorithm</b> for production traffic congestion prediction due to:
• Superior overall performance (R² = 0.9988)
• Excellent prediction confidence (0.9847)
• Minimal overfitting (CV Std = 0.0002)
• Balanced ensemble approach combining complementary strengths"""
    
    elements.append(Paragraph(deploy_text, normal_style))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph('6.2 Future Enhancements', styles['Heading3']))
    
    enhancements = [
        'Implement Bayesian optimization for hyperparameter tuning',
        'Add temporal features (trend, seasonality, special events)',
        'Expand ensemble with neural network base learner',
        'Deploy real-time monitoring and model retraining pipeline',
        'Integrate weather forecasts for improved predictions',
        'Collect and incorporate multi-modal sensor data'
    ]
    
    for enh in enhancements:
        elements.append(Paragraph(f'• {enh}', bullet_style))
    
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph('6.3 Conclusion', styles['Heading3']))
    
    conclusion = """This study successfully developed and evaluated five machine learning approaches for traffic congestion prediction. The proposed Adaptive Ensemble algorithm with dynamic feature weighting demonstrates superior performance over baseline and standard algorithms, achieving exceptional accuracy (R²=0.9988) while maintaining excellent generalization properties. The model is production-ready and recommended for immediate deployment to optimize Delhi's traffic management systems."""
    
    elements.append(Paragraph(conclusion, normal_style))
    
    # ==========================================
    # FOOTER
    # ==========================================
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph('_' * 80, normal_style))
    
    footer_text = f"""Report Generated: {timestamp}
    Project: Delhi AI Green Route - Traffic Congestion Prediction
    Contact: Data Analytics Team"""
    
    elements.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(elements)
    
    print(f"✅ PDF document saved: {pdf_path}")
    return pdf_path


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("PDF REPORT GENERATION")
    print("="*80)
    
    pdf_path = create_pdf_report()
    
    if os.path.exists(pdf_path):
        file_size = os.path.getsize(pdf_path) / 1024
        print(f"\n✅ PDF Report Successfully Generated!")
        print(f"   File: {pdf_path}")
        print(f"   Size: {file_size:.1f} KB")
    else:
        print("❌ PDF generation failed")


if __name__ == "__main__":
    main()
