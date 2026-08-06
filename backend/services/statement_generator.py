import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_owner_statement_pdf_bytes(
    owner_name: str,
    statement_period: str,
    properties_count: int,
    total_gross: float,
    total_mgmt: float,
    total_reserve: float,
    total_maintenance: float,
    net_distribution: float,
    line_items: list
) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=6
    )

    story = []

    # Document Header
    story.append(Paragraph("MONTHLY OWNER DISTRIBUTION STATEMENT", title_style))
    story.append(Paragraph(f"PropFlow Asset Management OS • Statement Period: {statement_period}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#CBD5E1'), spaceAfter=15))

    # Statement Meta
    meta_data = [
        [Paragraph(f"<b>Property Owner:</b> {owner_name}", body_style), Paragraph(f"<b>Managed Properties:</b> {properties_count}", body_style)],
        [Paragraph(f"<b>Statement ID:</b> STMT-{owner_name.replace(' ', '').upper()[:6]}-202608", body_style), Paragraph(f"<b>Disbursement Method:</b> ACH Direct Deposit", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 250])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Portfolio Summary Breakdown Table
    story.append(Paragraph("Portfolio Financial Summary", h2_style))
    summary_data = [
        [Paragraph("<b>Category</b>", body_style), Paragraph("<b>Amount (USD)</b>", body_style)],
        [Paragraph("Gross Rent Collected", body_style), Paragraph(f"${total_gross:,.2f}", body_style)],
        [Paragraph("Management Fees Subtotal", body_style), Paragraph(f"-${total_mgmt:,.2f}", body_style)],
        [Paragraph("Reserve Fund Withholdings", body_style), Paragraph(f"-${total_reserve:,.2f}", body_style)],
        [Paragraph("Maintenance & Repairs Deductions", body_style), Paragraph(f"-${total_maintenance:,.2f}", body_style)],
        [Paragraph("<b>NET OWNER DISBURSEMENT</b>", body_style), Paragraph(f"<b>${net_distribution:,.2f}</b>", body_style)]
    ]

    summary_table = Table(summary_data, colWidths=[300, 200])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#DCFCE7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 15))

    # Detailed Property Ledger
    story.append(Paragraph("Property Line-Item Breakdown", h2_style))

    ledger_data = [
        [
            Paragraph("<b>Property Address</b>", body_style),
            Paragraph("<b>Gross</b>", body_style),
            Paragraph("<b>Mgmt Fee</b>", body_style),
            Paragraph("<b>Reserve</b>", body_style),
            Paragraph("<b>Maint.</b>", body_style),
            Paragraph("<b>Net Payout</b>", body_style)
        ]
    ]

    for item in line_items:
        ledger_data.append([
            Paragraph(item["property_address"], body_style),
            Paragraph(f"${item['gross_rent']:,.2f}", body_style),
            Paragraph(f"${item['mgmt_fee']:,.2f}", body_style),
            Paragraph(f"${item['reserve_fund']:,.2f}", body_style),
            Paragraph(f"${item['maintenance']:,.2f}", body_style),
            Paragraph(f"<b>${item['net']:,.2f}</b>", body_style)
        ])

    ledger_table = Table(ledger_data, colWidths=[180, 64, 64, 64, 64, 64])
    ledger_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(ledger_table)

    story.append(Spacer(1, 25))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=15))
    story.append(Paragraph("This automated distribution statement was generated by PropFlow PM OS. Funds are initiated via ACH transfer.", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
