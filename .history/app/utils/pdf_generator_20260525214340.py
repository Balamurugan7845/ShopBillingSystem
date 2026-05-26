import io
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_invoice_pdf(bill, items):
    import decimal
    
    # Handle both dict and list formats for bill
    if isinstance(bill, dict):
        bill_dict = bill
        bill_number = bill_dict.get('bill_number', '')
        total_amount = float(bill_dict.get('total_amount', 0) or 0)
        gst_amount = float(bill_dict.get('gst_amount', 0) or 0)
        final_amount = float(bill_dict.get('final_amount', 0) or 0)
        payment_method = bill_dict.get('payment_method', '')
        created_at = bill_dict.get('created_at', datetime.datetime.now())
        customer_name = bill_dict.get('name', 'Walk-in Customer')
        phone = bill_dict.get('phone', '')
        email = bill_dict.get('email', '')
        address = bill_dict.get('address', '')
    else:
        bill = list(bill)
        for i, v in enumerate(bill):
            if isinstance(v, decimal.Decimal):
                try:
                    bill[i] = float(v)
                except Exception:
                    pass

        created_at = None
        for val in bill:
            if isinstance(val, datetime.datetime):
                created_at = val
                break

        if created_at is None:
            created_at = datetime.datetime.now()

        while len(bill) <= 11:
            bill.append(None)
        bill[7] = created_at

        for idx in (3, 4, 5):
            if idx < len(bill):
                try:
                    bill[idx] = float(bill[idx]) if bill[idx] is not None else 0.0
                except Exception:
                    bill[idx] = 0.0
        
        bill_number = bill[2]
        total_amount = bill[3]
        gst_amount = bill[4]
        final_amount = bill[5]
        payment_method = bill[6]
        customer_name = bill[8] if len(bill) > 8 else 'Walk-in Customer'
        phone = bill[9] if len(bill) > 9 else ''
        email = bill[10] if len(bill) > 10 else ''
        address = bill[11] if len(bill) > 11 else ''

    processed_items = []
    for it in items:
        if isinstance(it, dict):
            processed_items.append(it)
        else:
            row = list(it)
            for j, val in enumerate(row):
                if isinstance(val, decimal.Decimal):
                    try:
                        row[j] = float(val)
                    except Exception:
                        pass
            processed_items.append(row)
    
    items = processed_items

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    elements = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    styles.add(ParagraphStyle(name='Right', alignment=2))

    elements.append(Paragraph("SHOP BILLING SYSTEM", styles['Title']))
    elements.append(Paragraph("TAX INVOICE", styles['Heading1']))
    elements.append(Spacer(1, 12))

    company_data = [
        [Paragraph("<b>From:</b>", styles['Normal']), 
         Paragraph("<b>Invoice Details:</b>", styles['Normal'])],
        [Paragraph("Shop Billing System<br/>"
                  "123 College Street<br/>"
                  "Academic City, AC 12345<br/>"
                  "Phone: (555) 123-4567<br/>"
                  "Email: shop@college.edu", styles['Normal']),
         Paragraph(f"Bill No: {bill_number}<br/>"
                  f"Date: {created_at.strftime('%B %d, %Y')}<br/>"
                  f"Time: {created_at.strftime('%I:%M %p')}<br/>"
                  f"Payment Method: {payment_method}", styles['Normal'])]
    ]
    
    company_table = Table(company_data, colWidths=[3*inch, 3*inch])
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>Bill To:</b> {customer_name}", styles['Normal']))
    if phone:
        elements.append(Paragraph(f"Phone: {phone}", styles['Normal']))
    if email:
        elements.append(Paragraph(f"Email: {email}", styles['Normal']))
    if address:
        elements.append(Paragraph(f"Address: {address}", styles['Normal']))
    
    elements.append(Spacer(1, 12))
    
    data = [['Item', 'Product', 'Unit Price (₹)', 'Qty', 'Total (₹)']]
    
    for i, item in enumerate(items, 1):
        if isinstance(item, dict):
            product_name = item.get('name', '')
            unit_price = float(item.get('unit_price', 0) or 0)
            qty = int(item.get('quantity', 1) or 1)
            item_total = float(item.get('total', 0) or 0)
        else:
            product_name = item[6] if len(item) > 6 else ''
            unit_price = float(item[4]) if len(item) > 4 else 0
            qty = int(item[3]) if len(item) > 3 else 1
            item_total = float(item[5]) if len(item) > 5 else 0
        
        data.append([
            str(i),
            product_name,
            f"₹{unit_price:.2f}",
            str(qty),
            f"₹{item_total:.2f}"
        ])

    data.append(['', '', '', 'Subtotal:', f"₹{total_amount:.2f}"])
    data.append(['', '', '', 'GST (18%):', f"₹{gst_amount:.2f}"])
    data.append(['', '', '', '<b>Grand Total:</b>', f"<b>₹{final_amount:.2f}</b>"])
    
    items_table = Table(data, colWidths=[0.5*inch, 2.5*inch, 1.2*inch, 0.8*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('ALIGN', (-2, -3), (-1, -1), 'RIGHT'),
        ('FONTNAME', (-2, -3), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (-2, -1), (-1, -1), 1, colors.black),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 24))
    
    elements.append(Paragraph("Thank you for your business!", styles['Heading2']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Terms & Conditions: Goods once sold cannot be returned or exchanged unless defective. "
                            "This is a computer generated invoice.", styles['Normal']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                            styles['Normal']))
    
    doc.build(elements)
    
    buffer.seek(0)
    return buffer