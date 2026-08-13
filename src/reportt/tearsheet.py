import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Group, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot

NAVY = colors.HexColor("#1A2B4C")
LIGHT_BG = colors.HexColor("#F4F6F9")
GREEN = colors.HexColor("#2E7D32")
RED = colors.HexColor("#C62828")
DARK_GRAY = colors.HexColor("#333333")

def draw_header_footer(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, letter[1] - 40, letter[0], 40, fill=True, stroke=False)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(36, letter[1] - 25, doc.company_name.upper())
    canvas.setFont("Helvetica", 10)
    canvas.drawRightString(letter[0] - 36, letter[1] - 25, f"Ticker: {doc.ticker} | Sector: {doc.sector}")

    # Footer
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(36, 35, letter[0] - 36, 35)
    canvas.setFillColor(DARK_GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(36, 20, "Equity Intelligence Report — Confidential")
    canvas.drawRightString(letter[0] - 36, 20, f"Page {canvas.getPageNumber()} of 2")
    canvas.restoreState()

def create_kpi_tile(label, value, subtext="", width=170, height=50):
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=LIGHT_BG, strokeColor=NAVY, strokeWidth=0.5, rx=4, ry=4))
    d.add(String(10, height - 16, label, fontName="Helvetica-Bold", fontSize=8, fillColor=DARK_GRAY))
    d.add(String(10, height - 32, value, fontName="Helvetica-Bold", fontSize=13, fillColor=NAVY))
    if subtext:
        d.add(String(10, 8, subtext, fontName="Helvetica", fontSize=7, fillColor=GREEN if "+" in subtext else RED))
    return d

def create_bar_chart(years, rev_data, pat_data, width=520, height=140):
    d = Drawing(width, height)
    chart = VerticalBarChart()
    chart.x = 30
    chart.y = 20
    chart.height = height - 40
    chart.width = width - 40
    chart.data = [rev_data, pat_data]
    chart.categoryAxis.categoryNames = years
    chart.categoryAxis.labels.fontSize = 7
    chart.bars[0].fillColor = NAVY
    chart.bars[1].fillColor = colors.HexColor("#4A90E2")

    # Legend
    d.add(Rect(width - 130, height - 12, 10, 8, fillColor=NAVY, strokeColor=None))
    d.add(String(width - 115, height - 10, "Revenue (Cr)", fontName="Helvetica", fontSize=7))
    d.add(Rect(width - 60, height - 12, 10, 8, fillColor=colors.HexColor("#4A90E2"), strokeColor=None))
    d.add(String(width - 45, height - 10, "PAT (Cr)", fontName="Helvetica", fontSize=7))
    d.add(chart)
    return d

def generate_tearsheet_pdf(company_info: dict, filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    doc.company_name = company_info.get("name", "Company Name")
    doc.ticker = company_info.get("ticker", "TICKER")
    doc.sector = company_info.get("sector", "General")

    styles = getSampleStyleSheet()

    style_section = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=NAVY,
        spaceAfter=6,
        spaceBefore=8
    )

    style_bullet_pro = ParagraphStyle(
        'ProBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=GREEN,
        wordWrap='CJK'
    )

    style_bullet_con = ParagraphStyle(
        'ConBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=RED,
        wordWrap='CJK'
    )

    story = []

    # --- PAGE 1 CONTENT ---
    story.append(Paragraph("Key Financial Metrics", style_section))

    # KPI Grid (2 rows x 3 columns)
    kpis = company_info.get("kpis", {})
    row1 = [
        create_kpi_tile("REVENUE (5Y CAGR)", f"{kpis.get('rev_cagr', 0)}%", "+Strong"),
        create_kpi_tile("NET PROFIT (5Y CAGR)", f"{kpis.get('pat_cagr', 0)}%", "+Healthy"),
        create_kpi_tile("ROE (LATEST)", f"{kpis.get('roe', 0)}%", "High Return")
    ]
    row2 = [
        create_kpi_tile("ROCE (LATEST)", f"{kpis.get('roce', 0)}%", "Efficient"),
        create_kpi_tile("D/E RATIO", f"{kpis.get('de_ratio', 0)}x", "Low Debt"),
        create_kpi_tile("CFO QUALITY SCORE", f"{kpis.get('cfo_quality', 'High')}", "High Conversion")
    ]

    t_kpi = Table([row1, row2], colWidths=[175, 175, 175])
    t_kpi.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 10))

    # 10-Year Financial Growth Chart
    story.append(Paragraph("10-Year Revenue & Net Profit Trajectory", style_section))
    years = [str(y) for y in range(2016, 2026)]
    rev_data = company_info.get("rev_history", [100 + i*15 for i in range(10)])
    pat_data = company_info.get("pat_history", [15 + i*2.5 for i in range(10)])
    story.append(create_bar_chart(years, rev_data, pat_data))
    story.append(Spacer(1, 10))

    # Financial Ratios Table
    story.append(Paragraph("Ratio Engine Snapshot", style_section))
    ratio_headers = ["Metric", "FY22", "FY23", "FY24", "FY25", "Benchmark"]
    ratio_rows = [
        ["OPM (%)", "21.5%", "22.0%", "23.1%", "24.0%", "> 15.0%"],
        ["NPM (%)", "14.2%", "15.0%", "15.8%", "16.5%", "> 10.0%"],
        ["Asset Turnover", "1.1x", "1.2x", "1.2x", "1.3x", "> 1.0x"],
        ["Interest Coverage", "12.4x", "14.1x", "15.8x", "18.2x", "> 4.0x"]
    ]

    table_data = [[Paragraph(f"<b>{col}</b>", styles['Normal']) for col in ratio_headers]]
    for r in ratio_rows:
        table_data.append([Paragraph(cell, styles['Normal']) for cell in r])

    t_ratios = Table(table_data, colWidths=[120, 80, 80, 80, 80, 80])
    t_ratios.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_ratios)

    # Force PageBreak to ensure strict 2-page boundary
    story.append(PageBreak())

    # --- PAGE 2 CONTENT ---
    story.append(Paragraph("Pros & Cons Intelligence", style_section))

    pros = company_info.get("pros", ["Sustained high capital efficiency", "Debt free balance sheet"])
    cons = company_info.get("cons", ["Valuation multiples at historical highs", "Input cost inflation risks"])

    pros_content = [Paragraph(f"• {p}", style_bullet_pro) for p in pros]
    cons_content = [Paragraph(f"• {c}", style_bullet_con) for c in cons]

    t_pc = Table([[pros_content, cons_content]], colWidths=[255, 255])
    t_pc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#E8F5E9")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#FFEBEE")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_pc)
    story.append(Spacer(1, 15))

    # Cash Flow Intelligence Summary
    story.append(Paragraph("Cash Flow & Capital Allocation Profile", style_section))
    cf_summary = [
        ["CFO Quality Label:", company_info.get("cfo_quality_label", "High Quality")],
        ["CapEx Intensity Label:", company_info.get("capex_label", "Asset Light")],
        ["Capital Allocation Pattern:", company_info.get("capital_alloc_label", "Balanced Capital Allocator")]
    ]
    t_cf = Table([[Paragraph(f"<b>{r[0]}</b>", styles['Normal']), Paragraph(r[1], styles['Normal'])] for r in cf_summary], colWidths=[180, 340])
    t_cf.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,0), (0,-1), LIGHT_BG),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_cf)

    # Build Document
    doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
