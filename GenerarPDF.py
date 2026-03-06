from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import mm

MARGEN = 12 * mm
ANCHO_TOTAL = 270 * mm


def definirEstilos():
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
        fontSize=18,
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

    return empresa_style, titulo_style, sub_style, meta_label, meta_value


def crearEncabezado(empresa_style, titulo_style, sub_style):
    elementos = []

    logo = Image("Logo.png", width=50 * mm, height=25 * mm)

    encabezado = Table(
        [[logo, Paragraph("ATI LOGÍSTICA ADUANERA S.A.", empresa_style)]],
        colWidths=[5 * mm, 260 * mm]
    )

    encabezado.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    elementos.append(encabezado)
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("Reporte de productos por costo total", titulo_style))
    elementos.append(Spacer(1, 2))
    elementos.append(Paragraph("Orden descendente por costo total", sub_style))
    elementos.append(Spacer(1, 4))

    return elementos


def crearLinea(alto):
    linea = Table([[""]], colWidths=[ANCHO_TOTAL], rowHeights=[alto])
    linea.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.black),
        ("BOX", (0, 0), (-1, -1), 0, colors.black),
    ]))
    return linea


def crearFiltros(meta_label, meta_value, pais, moneda):
    filtros = [
        [
            Paragraph("País:", meta_label),
            Paragraph(pais, meta_value),
            Paragraph("Moneda:", meta_label),
            Paragraph(moneda, meta_value)
        ],
    ]

    tabla_filtros = Table(filtros, colWidths=[24 * mm, 58 * mm, 30 * mm, 58 * mm])
    tabla_filtros.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    return tabla_filtros


def generarDatosPrueba(cantidad=80):
    data = [["#", "Producto", "País", "Precio", "Impuesto", "Costo total", "Moneda"]]

    for i in range(1, cantidad + 1):
        data.append([
            str(i),
            f"Producto {i}",
            "México",
            "100.00",
            "15%",
            "115.00",
            "USD"
        ])

    return data


def crearTablaProductos(data):
    col_widths = [12 * mm, 72 * mm, 35 * mm, 30 * mm, 28 * mm, 36 * mm, 24 * mm]

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

    return tabla


def crearResumen(meta_label, meta_value, cantidad_productos):
    resumen = Table([
        [Paragraph("Total de productos en el reporte:", meta_label), Paragraph(str(cantidad_productos), meta_value)],
        [Paragraph("Observación:", meta_label), Paragraph("Los productos se muestran ordenados de mayor a menor según su costo total.", meta_value)]
    ], colWidths=[58 * mm, 170 * mm])

    resumen.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    return resumen


def agregarNumeroPagina(canvas, doc):
    canvas.setFont("Helvetica", 9)
    texto = f"Página {doc.page}"
    canvas.drawRightString(280 * mm, 10 * mm, texto)


def crearPdf(nombre_pdf="reporte_ATI_logistica.pdf", pais="México", moneda="USD"):
    doc = SimpleDocTemplate(
        nombre_pdf,
        pagesize=landscape(A4),
        leftMargin=MARGEN,
        rightMargin=MARGEN,
        topMargin=MARGEN,
        bottomMargin=MARGEN
    )

    empresa_style, titulo_style, sub_style, meta_label, meta_value = definirEstilos()

    elementos = []

    elementos.extend(crearEncabezado(empresa_style, titulo_style, sub_style))
    elementos.append(crearLinea(1.1 * mm))
    elementos.append(Spacer(1, 5))
    elementos.append(crearFiltros(meta_label, meta_value, pais, moneda))
    elementos.append(Spacer(1, 4))
    elementos.append(crearLinea(0.8 * mm))
    elementos.append(Spacer(1, 4))

    data = generarDatosPrueba(80)
    tabla = crearTablaProductos(data)
    elementos.append(tabla)
    elementos.append(Spacer(1, 8))

    resumen = crearResumen(meta_label, meta_value, len(data) - 1)
    elementos.append(resumen)

    doc.build(
        elementos,
        onFirstPage=agregarNumeroPagina,
        onLaterPages=agregarNumeroPagina
    )


if __name__ == "__main__":
    crearPdf()
    print("PDF ATI generado correctamente.")