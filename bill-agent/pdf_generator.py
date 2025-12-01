"""AWS Bill Invoice PDF Generator."""

from datetime import datetime, timedelta
from typing import List
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

from schema import SpendingAnalysis


def generate_aws_bill_pdf(analysis: SpendingAnalysis) -> bytes:
    """Generate a fake AWS bill invoice PDF.

    Args:
        analysis: Spending analysis data

    Returns:
        PDF file as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#FF9900'),  # AWS Orange
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#232F3E'),  # AWS Dark Blue
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = styles['Normal']
    
    # Calculate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=analysis.timeline_days)
    invoice_number = f"INV-{end_date.strftime('%Y%m%d')}-{hash(analysis.total_amount) % 10000:04d}"
    
    # Header - AWS Logo placeholder and title
    elements.append(Paragraph("Amazon Web Services", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Invoice header
    elements.append(Paragraph("INVOICE", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Invoice details table
    invoice_data = [
        ['Invoice Number:', invoice_number],
        ['Invoice Date:', end_date.strftime('%B %d, %Y')],
        ['Billing Period:', f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"],
        ['Account ID:', '114713347049'],
        ['Payment Status:', '⚠️ OVERDUE'],
    ]
    
    invoice_table = Table(invoice_data, colWidths=[2*inch, 4*inch])
    invoice_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (1, 4), (1, 4), colors.red),
        ('FONTNAME', (1, 4), (1, 4), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(invoice_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Analysis summary
    elements.append(Paragraph("Spending Analysis Summary", heading_style))
    summary_data = [
        ['Efficiency Level:', analysis.efficiency_level],
        ['Architecture Type:', analysis.architecture_type.title()],
        ['Burning Style:', analysis.burning_style.title()],
        ['Timeline:', f"{analysis.timeline_days} days"],
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Services breakdown
    elements.append(Paragraph("Service Charges", heading_style))
    
    # Services table header
    service_data = [['Service', 'Type', 'Qty', 'Days', 'Unit Cost', 'Total']]
    
    # Add each service
    for service in analysis.services_deployed:
        duration_days = service.duration_used.split()[0] if 'entire' not in service.duration_used else str(analysis.timeline_days)
        service_data.append([
            service.service_name,
            service.instance_type[:20] + '...' if len(service.instance_type) > 20 else service.instance_type,
            str(service.quantity),
            duration_days,
            f"${service.unit_cost:.4f}",
            f"${service.total_cost:.2f}"
        ])
    
    # Add subtotal row
    service_data.append(['', '', '', '', 'Subtotal:', f"${analysis.total_calculated_cost:.2f}"])
    service_data.append(['', '', '', '', 'Tax (0%):', '$0.00'])
    service_data.append(['', '', '', '', 'Total Due:', f"${analysis.total_calculated_cost:.2f}"])
    
    services_table = Table(service_data, colWidths=[1.2*inch, 1.8*inch, 0.5*inch, 0.6*inch, 0.9*inch, 1*inch])
    services_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#232F3E')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -4), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -4), [colors.white, colors.HexColor('#F5F5F5')]),
        ('GRID', (0, 0), (-1, -4), 0.5, colors.grey),
        
        # Subtotal rows
        ('FONTNAME', (4, -3), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (4, -3), (-1, -1), 10),
        ('ALIGN', (4, -3), (-1, -1), 'RIGHT'),
        ('LINEABOVE', (4, -3), (-1, -3), 1, colors.black),
        
        # Total row
        ('BACKGROUND', (4, -1), (-1, -1), colors.HexColor('#FF9900')),
        ('TEXTCOLOR', (4, -1), (-1, -1), colors.white),
        ('FONTSIZE', (4, -1), (-1, -1), 12),
        ('LINEABOVE', (4, -1), (-1, -1), 2, colors.black),
        
        # Alignment
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'CENTER'),
        ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),
    ]))
    
    elements.append(services_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Key mistakes section
    elements.append(Paragraph("⚠️ Cost Optimization Opportunities", heading_style))
    mistakes_text = "<br/>".join([f"• {mistake}" for mistake in analysis.key_mistakes])
    elements.append(Paragraph(mistakes_text, normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Recommendations section
    elements.append(Paragraph("💡 Recommendations", heading_style))
    recommendations_text = "<br/>".join([f"• {rec}" for rec in analysis.recommendations])
    elements.append(Paragraph(recommendations_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Roast section (in a box)
    elements.append(Paragraph("🔥 Cost Analysis Commentary", heading_style))
    roast_style = ParagraphStyle(
        'Roast',
        parent=normal_style,
        fontSize=10,
        textColor=colors.HexColor('#D13212'),  # AWS Red
        leftIndent=10,
        rightIndent=10,
        spaceAfter=10,
        spaceBefore=10,
        borderColor=colors.HexColor('#D13212'),
        borderWidth=1,
        borderPadding=10,
    )
    elements.append(Paragraph(analysis.roast, roast_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Payment Options (Roast Style)
    elements.append(Paragraph("💳 Suggested Payment Options", heading_style))
    
    # Calculate payment tier based on cost
    cost = analysis.total_calculated_cost
    if cost < 1000:
        payment_options = [
            "☐ Sell your gaming PC (you won't need it after this bill)",
            "☐ Start a GoFundMe titled 'I Learned About AWS The Hard Way'",
            "☐ Return all those unused AWS certifications for a refund",
            "☐ Convince your manager this was 'research'",
            "☐ Raid your kid's college fund (they can learn to code instead)",
        ]
    elif cost < 5000:
        payment_options = [
            "☐ Take out a second mortgage on your house",
            "☐ Sell the CFO's shares (they'll understand... eventually)",
            "☐ Start an OnlyFans for cloud architecture disasters",
            "☐ Liquidate your 401(k) - retirement is overrated anyway",
            "☐ Organize a company bake sale (you'll need about 10,000 cupcakes)",
            "☐ Apply for AWS's 'Most Creative Waste' scholarship",
        ]
    else:
        payment_options = [
            "☐ Sell the company (it's worth less than this bill now)",
            "☐ Fake your own death and start fresh in another country",
            "☐ Convince investors this is 'aggressive growth spending'",
            "☐ Sell naming rights to your firstborn child",
            "☐ Start a cryptocurrency called 'RegretCoin'",
            "☐ Apply for witness protection and a new identity",
            "☐ Negotiate a payment plan spanning multiple generations",
        ]
    
    payment_style = ParagraphStyle(
        'Payment',
        parent=normal_style,
        fontSize=9,
        leftIndent=20,
        spaceAfter=4,
    )
    
    for option in payment_options:
        elements.append(Paragraph(option, payment_style))
    
    elements.append(Spacer(1, 0.1*inch))
    
    payment_note_style = ParagraphStyle(
        'PaymentNote',
        parent=normal_style,
        fontSize=8,
        textColor=colors.grey,
        fontName='Helvetica-Oblique',
        leftIndent=20,
    )
    elements.append(Paragraph(
        "* Payment plans available for those who still have assets remaining after this billing cycle.",
        payment_note_style
    ))
    
    # Footer
    elements.append(Spacer(1, 0.3*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=normal_style,
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph(
        "This is a simulated AWS bill for educational and demonstration purposes only.<br/>"
        "Amazon Web Services, Inc. | 410 Terry Avenue North, Seattle, WA 98109-5210<br/>"
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        footer_style
    ))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
