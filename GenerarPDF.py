
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm

def crear_pdf_ati(nombre_pdf="reporte_ATI_logistica.pdf"):
    doc = SimpleDocTemplate(
        nombre_pdf,
        pagesize=landscape(A4),
        leftMargin=12*mm,
        rightMargin=12*mm,
        topMargin=12*mm,
        bottomMargin=12*mm
    )

    styles = getSampleStyleSheet()
    empresa_style = ParagraphStyle(
        "empresa",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=16,
        leading=18,
        alignment=TA_CENTER
    )
    titulo_style = ParagraphStyle(
        "titulo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER
    )
    sub_style = ParagraphStyle(
        "sub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=12,
        alignment=TA_CENTER
    )
    meta_label = ParagraphStyle(
        "meta_label",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=12,
        alignment=TA_LEFT
    )
    meta_value = ParagraphStyle(
        "meta_value",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=12,
        alignment=TA_LEFT
    )

    elementos = []

    elementos.append(Paragraph("ATI LOGÍSTICA ADUANERA S.A.", empresa_style))
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("Reporte de productos por costo total", titulo_style))
    elementos.append(Spacer(1, 2))
    elementos.append(Paragraph("Orden descendente por costo total", sub_style))
    elementos.append(Spacer(1, 4))

    linea = Table([[""]], colWidths=[270*mm], rowHeights=[1.1*mm])
    linea.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.black),
        ("BOX", (0, 0), (-1, -1), 0, colors.black),
    ]))
    elementos.append(linea)
    elementos.append(Spacer(1, 5))

    filtros = [
        [Paragraph("País:", meta_label), Paragraph("[País seleccionado]", meta_value),
         Paragraph("Moneda:", meta_label), Paragraph("[Moneda seleccionada]", meta_value)],
    ]
    tabla_filtros = Table(filtros, colWidths=[24*mm, 58*mm, 30*mm, 58*mm])
    tabla_filtros.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elementos.append(tabla_filtros)
    elementos.append(Spacer(1, 4))

    linea2 = Table([[""]], colWidths=[270*mm], rowHeights=[0.8*mm])
    linea2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.black),
        ("BOX", (0, 0), (-1, -1), 0, colors.black),
    ]))
    elementos.append(linea2)
    elementos.append(Spacer(1, 4))

    data = [
        ["#", "Producto", "País", "Precio", "Impuesto", "Costo total", "Moneda"],
        ["1", "Laptop", "México", "1000.00", "25%", "1250.00", "USD"],
        ["2", "Monitor", "México", "800.00", "22%", "976.00", "USD"],
        ["3", "Mouse", "México", "40.00", "15%", "46.00", "USD"],
        ["4", "Teclado", "México", "35.00", "12%", "39.20", "USD"],
    ]

    col_widths = [12*mm, 72*mm, 35*mm, 30*mm, 28*mm, 36*mm, 24*mm]
    tabla = Table(data, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ("LINEABOVE", (0, 0), (-1, 0), 1, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),

        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("VALIGN", (0, 1), (-1, -1), "MIDDLE"),

        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (1, 1), (2, -1), "LEFT"),
        ("ALIGN", (3, 1), (-1, -1), "CENTER"),

        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),

        ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.lightgrey),
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 8))

    resumen = Table([
        [Paragraph("Total de productos en el reporte:", meta_label), Paragraph("[Cantidad]", meta_value)],
        [Paragraph("Observación:", meta_label), Paragraph("Los productos se muestran ordenados de mayor a menor según su costo total.", meta_value)]
    ], colWidths=[58*mm, 170*mm])
    resumen.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elementos.append(resumen)

    doc.build(elementos)

if __name__ == "__main__":
    crear_pdf_ati()
    print("PDF ATI generado correctamente.")