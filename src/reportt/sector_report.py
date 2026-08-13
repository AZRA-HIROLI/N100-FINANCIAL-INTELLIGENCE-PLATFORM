import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

NAVY = colors.HexColor("#1A2B4C")
LIGHT_BG = colors.HexColor("#F4F6F9")
DARK_GRAY = colors.HexColor("#333333")

def draw_sector_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, letter[1] - 40, letter[0], 40, fill=True, stroke=False)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(36, letter[1] - 25, f"SECTOR INTELLIGENCE: {doc.sector_name.upper()}")

    canvas.setStrokeColor(colors.lightgrey)
    canvas.line(36, 35, letter[0] - 36, 35)
    canvas.setFillColor(DARK_GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(36, 20, "Equity Intelligence Report — Sector Benchmark")
    canvas.drawRightString(letter[0] - 36, 20, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()

def generate_sector_pdf(sector_name: str, df_sector: pd.DataFrame, filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    doc.sector_name = sector_name

    styles = getSampleStyleSheet()
    style_section = ParagraphStyle(
        'SectorSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=NAVY,
        spaceAfter=8
    )

    story = []

    # Section 1: Sector Median KPIs
    story.append(Paragraph("Sector Executive Benchmark (Medians)", style_section))

    med_rev = df_sector["rev_cagr"].median()
    med_pat = df_sector["pat_cagr"].median()
    med_roe = df_sector["roe"].median()
    med_roce = df_sector["roce"].median()

    summary_data = [
        [Paragraph("<b>Metric</b>", styles['Normal']), Paragraph("<b>Sector Median</b>", styles['Normal'])],
        [Paragraph("Revenue 5Y CAGR", styles['Normal']), Paragraph(f"{med_rev:.1f}%", styles['Normal'])],
        [Paragraph("Net Profit 5Y CAGR", styles['Normal']), Paragraph(f"{med_pat:.1f}%", styles['Normal'])],
        [Paragraph("ROE", styles['Normal']), Paragraph(f"{med_roe:.1f}%", styles['Normal'])],
        [Paragraph("ROCE", styles['Normal']), Paragraph(f"{med_roce:.1f}%", styles['Normal'])],
    ]
    t_summary = Table(summary_data, colWidths=[200, 320])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('PADDING', (0,0), (-1,-1), 5)
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 15))

    # Section 2: Company Level Details Matrix (8 metrics per company)
    story.append(Paragraph(f"Company List ({len(df_sector)} Constituent Companies)", style_section))

    headers = ["Ticker", "Company", "Rev 5Y%", "PAT 5Y%", "ROE%", "ROCE%", "D/E", "CFO Quality"]
    matrix_data = [[Paragraph(f"<b>{h}</b>", styles['Normal']) for h in headers]]

    for _, row in df_sector.iterrows():
        matrix_data.append([
            Paragraph(str(row["ticker"]), styles['Normal']),
            Paragraph(str(row["name"])[:18], styles['Normal']),
            Paragraph(f"{row['rev_cagr']:.1f}%", styles['Normal']),
            Paragraph(f"{row['pat_cagr']:.1f}%", styles['Normal']),
            Paragraph(f"{row['roe']:.1f}%", styles['Normal']),
            Paragraph(f"{row['roce']:.1f}%", styles['Normal']),
            Paragraph(f"{row['de_ratio']:.2f}", styles['Normal']),
            Paragraph(str(row["cfo_quality"]), styles['Normal'])
        ])

    t_matrix = Table(matrix_data, colWidths=[60, 110, 55, 55, 50, 50, 40, 100])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_matrix)

    doc.build(story, onFirstPage=draw_sector_header_footer, onLaterPages=draw_sector_header_footer)
