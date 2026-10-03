import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from app.services.kpi_engine import compute_dataset_kpis
from app.services.insight_engine import generate_ai_business_insights
from app.services.anomaly_detector import detect_anomalies_in_dataset

def generate_pdf_report(
    file_path: str,
    output_pdf_path: str,
    report_title: str = "Executive Sales Intelligence Report",
    report_type: str = "Executive Monthly"
) -> str:
    
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Colors
    navy_blue = colors.HexColor("#1E293B")
    accent_blue = colors.HexColor("#2563EB")
    emerald_green = colors.HexColor("#059669")
    light_bg = colors.HexColor("#F8FAFC")
    text_dark = colors.HexColor("#0F172A")
    border_color = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=navy_blue,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=15
    )
    
    heading2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=navy_blue,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark
    )

    insight_title_style = ParagraphStyle(
        'InsightTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=navy_blue
    )
    
    insight_desc_style = ParagraphStyle(
        'InsightDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )

    story = []
    
    # 1. Header Banner
    story.append(Paragraph(report_title, title_style))
    today_str = datetime.now().strftime("%d %B %Y - %I:%M %p")
    story.append(Paragraph(f"<b>Type:</b> {report_type} Report &nbsp;&nbsp;|&nbsp;&nbsp; <b>Generated:</b> {today_str} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Status:</b> Automated Confidential BI", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=accent_blue, spaceBefore=0, spaceAfter=15))

    # 2. Key Metrics Summary Grid
    kpi_res = compute_dataset_kpis(file_path)
    kpis = kpi_res.get("kpis", [])
    
    story.append(Paragraph("1. Executive Metrics Snapshot", heading2_style))
    
    if kpis:
        table_data = [["Metric", "Value", "Growth / Trend", "Status"]]
        for k in kpis:
            status_color = emerald_green if k.get("status") == "positive" else colors.HexColor("#DC2626")
            table_data.append([
                k.get("name", ""),
                k.get("value", ""),
                k.get("trend", "N/A"),
                k.get("status", "").upper()
            ])
            
        kpi_table = Table(table_data, colWidths=[180, 120, 120, 120])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), navy_blue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9.5),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('TOPPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND', (0,1), (-1,-1), light_bg),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('BOTTOMPADDING', (0,1), (-1,-1), 5),
            ('TOPPADDING', (0,1), (-1,-1), 5),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 15))

    # 3. AI Business Insights
    insights = generate_ai_business_insights(file_path)
    story.append(Paragraph("2. AI Business Intelligence & Strategic Insights", heading2_style))
    
    if insights:
        ins_table_data = []
        for ins in insights[:4]:
            t_cell = Paragraph(f"<b>{ins.get('title', '')}</b> ({ins.get('metric', '')})", insight_title_style)
            d_cell = Paragraph(f"{ins.get('description', '')}<br/><font color='#2563EB'><b>Action:</b> {ins.get('recommendation', '')}</font>", insight_desc_style)
            ins_table_data.append([t_cell, d_cell])
            
        ins_table = Table(ins_table_data, colWidths=[160, 380])
        ins_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), light_bg),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(ins_table)
        story.append(Spacer(1, 15))

    # 4. Detected Anomalies Alert
    anomalies = detect_anomalies_in_dataset(file_path)
    if anomalies:
        story.append(Paragraph("3. Operational Anomalies & Outlier Flags", heading2_style))
        anom_data = [["Date / Location", "Metric", "Actual Value", "Expected Value", "Severity"]]
        for a in anomalies[:4]:
            anom_data.append([
                f"{a.get('date', '')}\n({a.get('region', 'N/A')})",
                a.get('metric_name', ''),
                f"₹{a.get('actual_value', 0):,.2f}",
                f"₹{a.get('expected_value', 0):,.2f}",
                a.get('severity', '').upper()
            ])
            
        anom_table = Table(anom_data, colWidths=[140, 100, 100, 100, 100])
        anom_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#991B1B")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,1), (-1,-1), 8.5),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(anom_table)
        story.append(Spacer(1, 15))

    # 5. Footer Sign-off
    story.append(HRFlowable(width="100%", thickness=1, color=border_color, spaceBefore=10, spaceAfter=10))
    story.append(Paragraph("<i>This executive BI report was automatically compiled by AI BI Reporting Platform. All underlying calculations were verified against raw dataset records.</i>", body_style))

    doc.build(story)
    return output_pdf_path
