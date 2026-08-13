import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

NAVY = colors.HexColor("#1A2B4C")
LIGHT_BG = colors.HexColor("#F4F6F9")
GREEN = colors.HexColor("#2E7D32")
RED = colors.HexColor("#C62828")
GRAY = colors.HexColor("#666666")
DARK_GRAY = colors.HexColor("#333333")

def draw_portfolio_header_footer(canvas, doc):
    canvas.saveState()
    # Header
    canvas.setFillColor(NAVY)
    canvas.rect(0, letter[1] - 40, letter[0], 40, fill=True, stroke=False)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(36, letter[1] - 25, "PORTFOLIO EXECUTIVE SUMMARY")
    canvas.drawRightString(letter[0] - 36, letter[1] - 25, "SPRINT 5 DELIVERABLE")

    # Footer
    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(36, 35, letter[0] - 36, 35)
    canvas.setFillColor(DARK_GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(36, 20, "Equity Intelligence — 92 Company Portfolio Overview")
    canvas.drawRightString(letter[0] - 36, 20, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()

def get_trend_indicator(curr_val, prev_val):
    if prev_val == 0:
        return " -> (0.0%)", GRAY
    pct_change = ((curr_val - prev_val) / abs(prev_val)) * 100
    if pct_change > 2.0:
        return f" ^ (+{pct_change:.1f}%)", GREEN
    elif pct_change < -2.0:
        return f" v ({pct_change:.1f}%)", RED
    else:
        return f" -> ({pct_change:.1f}%)", GRAY

def generate_portfolio_summary_pdf(companies_list: list, filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CompTitle', parent=styles['Heading1'], fontName='Helvetica-Bold',
        fontSize=16, leading=20, textColor=NAVY, spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        'CompSub', parent=styles['Normal'], fontName='Helvetica',
        fontSize=10, leading=13, textColor=DARK_GRAY, spaceAfter=12
    )
    sec_style = ParagraphStyle(
        'SecHeader', parent=styles['Heading2'], fontName='Helvetica-Bold',
        fontSize=12, leading=15, textColor=NAVY, spaceAfter=6
    )

    story = []

    # Sort companies alphabetically by ticker
    sorted_companies = sorted(companies_list, key=lambda x: x["ticker"])

    for idx, comp in enumerate(sorted_companies):
        story.append(Paragraph(f"{comp['name']} ({comp['ticker']})", title_style))
        story.append(Paragraph(f"Sector: <b>{comp['sector']}</b> | Company ID: #{comp['company_id']:02d}", subtitle_style))

        story.append(Paragraph("Top 6 KPI Metrics & YoY Trend Signals", sec_style))

        # Prepare Top 6 KPIs with Trend Arrows
        kpis = comp.get("kpi_trends", {})

        headers = ["Metric", "FY24 Value", "FY25 Value", "YoY Trend Signal"]
        rows = [[Paragraph(f"<b>{h}</b>", styles['Normal']) for h in headers]]

        metric_keys = [
            ("Revenue (Cr)", "rev"),
            ("Net Profit (Cr)", "pat"),
            ("ROE (%)", "roe"),
            ("ROCE (%)", "roce"),
            ("Operating Margin (%)", "opm"),
            ("D/E Ratio", "de")
        ]

        for name, key in metric_keys:
            prev_v = kpis.get(f"{key}_prev", 0)
            curr_v = kpis.get(f"{key}_curr", 0)
            signal_text, signal_color = get_trend_indicator(curr_v, prev_v)

            p_signal = Paragraph(f"<font color='{signal_color.hexval()}'><b>{signal_text}</b></font>", styles['Normal'])
            rows.append([
                Paragraph(name, styles['Normal']),
                Paragraph(f"{prev_v:.1f}", styles['Normal']),
                Paragraph(f"{curr_v:.1f}", styles['Normal']),
                p_signal
            ])

        t_kpis = Table(rows, colWidths=[150, 100, 100, 190])
        t_kpis.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        story.append(t_kpis)
        story.append(Spacer(1, 15))

        # Qualitative Executive Summary
        story.append(Paragraph("Qualitative Profile", sec_style))
        summary_rows = [
            [Paragraph("<b>CFO Quality Label:</b>", styles['Normal']), Paragraph(comp.get("cfo_quality_label", "High Quality"), styles['Normal'])],
            [Paragraph("<b>CapEx Intensity:</b>", styles['Normal']), Paragraph(comp.get("capex_label", "Asset Light"), styles['Normal'])],
            [Paragraph("<b>Capital Allocation:</b>", styles['Normal']), Paragraph(comp.get("capital_alloc_label", "Balanced Allocator"), styles['Normal'])]
        ]
        t_summary = Table(summary_rows, colWidths=[150, 390])
        t_summary.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0,0), (0,-1), LIGHT_BG),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))
        story.append(t_summary)

        # One company per page constraint
        if idx < len(sorted_companies) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=draw_portfolio_header_footer, onLaterPages=draw_portfolio_header_footer)
