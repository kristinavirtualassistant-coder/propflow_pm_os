import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_lease_pdf_bytes(
    tenant_name: str,
    property_address: str,
    unit: str,
    lease_start: str,
    lease_end: str,
    monthly_rent: float,
    security_deposit: float,
    landlord_name: str = "PropFlow Asset Management LLC",
    state: str = "Texas"
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
        spaceAfter=6
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
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#334155'),
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6
    )

    story = []

    # Document Header
    story.append(Paragraph("RESIDENTIAL LEASE AGREEMENT", title_style))
    story.append(Paragraph(f"State of {state} • Standard Residential Tenancy Contract", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#CBD5E1'), spaceAfter=15))

    # Introduction
    intro_text = (
        f"This Residential Lease Agreement (the <b>\"Agreement\"</b>) is entered into between "
        f"<b>{landlord_name}</b> (<i>\"Landlord\"</i>) and <b>{tenant_name}</b> (<i>\"Tenant\"</i>). "
        f"Landlord hereby leases to Tenant, and Tenant leases from Landlord, the real property located at the address below under the following legally binding terms."
    )
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 10))

    # Summary Table
    table_data = [
        [Paragraph("<b>Property Address:</b>", body_style), Paragraph(f"{property_address} (Unit: {unit or 'N/A'})", body_style)],
        [Paragraph("<b>Lease Term:</b>", body_style), Paragraph(f"{lease_start} to {lease_end}", body_style)],
        [Paragraph("<b>Monthly Rent:</b>", body_style), Paragraph(f"${monthly_rent:,.2f} USD (Due 1st of month)", body_style)],
        [Paragraph("<b>Security Deposit:</b>", body_style), Paragraph(f"${security_deposit:,.2f} USD", body_style)],
        [Paragraph("<b>Governing Jurisdiction:</b>", body_style), Paragraph(f"State of {state}", body_style)]
    ]

    summary_table = Table(table_data, colWidths=[150, 350])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 15))

    # Terms & Conditions
    story.append(Paragraph("1. Rent & Late Fees", h2_style))
    story.append(Paragraph(
        "Tenant agrees to pay monthly rent in advance on or before the first day of each calendar month. "
        "A late fee of $75.00 shall be assessed if full payment is not received within five (5) calendar days of the due date.",
        body_style
    ))

    story.append(Paragraph("2. Maintenance & Operations", h2_style))
    story.append(Paragraph(
        "Tenant shall maintain the premises in a clean and sanitary condition. All emergency and routine maintenance requests "
        "must be submitted directly through the PropFlow PM OS Maintenance Portal.",
        body_style
    ))

    story.append(Paragraph("3. Occupancy & Pet Policy", h2_style))
    story.append(Paragraph(
        "Occupancy is strictly limited to named occupants on this agreement. Pets are subject to prior written approval "
        "and payment of a non-refundable pet deposit.",
        body_style
    ))

    story.append(Spacer(1, 25))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=20))

    # Signatures
    sig_data = [
        [
            Paragraph("<b>LANDLORD / AGENT:</b><br/><br/><br/>____________________________________<br/>Authorized Representative<br/>PropFlow Asset Management LLC", body_style),
            Paragraph("<b>TENANT:</b><br/><br/><br/>____________________________________<br/>" + tenant_name + "<br/>Primary Lessee", body_style)
        ]
    ]
    sig_table = Table(sig_data, colWidths=[250, 250])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(sig_table)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
