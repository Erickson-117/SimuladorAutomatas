"""Generación directa de informes técnicos PDF para AFN y AFD."""
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable
from reportlab.pdfbase.pdfmetrics import stringWidth


def _lista(valores):
    return ", ".join(sorted((str(v) for v in valores), key=str)) or "Ninguno"


def _p(texto, estilo):
    return Paragraph(escape(str(texto)).replace("\n", "<br/>"), estilo)



class DiagramaAutomata(Flowable):
    """Dibuja una vista vectorial del autómata directamente en el PDF."""

    def __init__(self, estados, transiciones, inicial, finales, alto=92*mm):
        super().__init__()
        self.estados = list(estados)
        self.transiciones = list(transiciones.items())
        self.inicial = str(inicial)
        self.finales = {str(e) for e in finales}
        self.height = alto
        self.width = 174*mm

    @staticmethod
    def _flecha(c, x1, y1, x2, y2, color):
        import math
        c.setStrokeColor(color)
        c.setFillColor(color)
        c.setLineWidth(1.1)
        c.line(x1, y1, x2, y2)
        ang = math.atan2(y2-y1, x2-x1)
        largo, apertura = 6, 0.45
        p1 = (x2-largo*math.cos(ang-apertura), y2-largo*math.sin(ang-apertura))
        p2 = (x2-largo*math.cos(ang+apertura), y2-largo*math.sin(ang+apertura))
        path = c.beginPath()
        path.moveTo(x2, y2)
        path.lineTo(*p1)
        path.lineTo(*p2)
        path.close()
        c.drawPath(path, stroke=0, fill=1)

    def draw(self):
        import math
        c = self.canv
        w, h = self.width, self.height
        azul = colors.HexColor("#1D4ED8")
        tinta = colors.HexColor("#1E293B")
        gris = colors.HexColor("#64748B")
        fondo = colors.HexColor("#EFF6FF")
        borde = colors.HexColor("#3B82F6")
        c.saveState()
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.roundRect(0, 0, w, h, 8, stroke=1, fill=1)

        n = len(self.estados)
        if not n:
            c.setFillColor(gris)
            c.setFont("Helvetica-Oblique", 10)
            c.drawCentredString(w/2, h/2, "No hay estados para representar.")
            c.restoreState()
            return

        # Distribución circular adaptable al número de estados.
        cx, cy = w/2, h/2
        rx = max(35, min(w*0.39, 260))
        ry = max(24, h*0.32)
        radio = 15
        posiciones = {}
        for i, estado in enumerate(self.estados):
            ang = math.pi/2 + (2*math.pi*i/n)
            posiciones[str(estado)] = (cx + rx*math.cos(ang), cy + ry*math.sin(ang))

        # Flecha de entrada para el estado inicial.
        if self.inicial in posiciones:
            x, y = posiciones[self.inicial]
            self._flecha(c, x-radio-20, y, x-radio, y, azul)

        # Agrupar transiciones por par para rotular una sola arista por dirección.
        aristas = {}
        bucles = {}
        for (origen, simbolo), destinos in self.transiciones:
            origen, simbolo = str(origen), str(simbolo)
            if isinstance(destinos, (set, frozenset, list, tuple)):
                lista = [str(d) for d in destinos]
            else:
                lista = [str(destinos)]
            for destino in lista:
                if origen == destino:
                    bucles.setdefault(origen, []).append(simbolo)
                elif origen in posiciones and destino in posiciones:
                    aristas.setdefault((origen, destino), []).append(simbolo)

        # Aristas rectas, recortadas para que no atraviesen los círculos.
        for (origen, destino), simbolos in aristas.items():
            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]
            dx, dy = x2-x1, y2-y1
            distancia = max(1, math.hypot(dx, dy))
            ux, uy = dx/distancia, dy/distancia
            sx, sy = x1+ux*radio, y1+uy*radio
            ex, ey = x2-ux*(radio+2), y2-uy*(radio+2)
            # Desplazamiento pequeño para diferenciar flechas opuestas.
            if (destino, origen) in aristas:
                px, py = -uy*5, ux*5
                sx, sy, ex, ey = sx+px, sy+py, ex+px, ey+py
            self._flecha(c, sx, sy, ex, ey, gris)
            etiqueta = ", ".join(simbolos)
            ancho = stringWidth(etiqueta, "Helvetica", 7)
            mx, my = (sx+ex)/2, (sy+ey)/2
            c.setFillColor(colors.white)
            c.roundRect(mx-ancho/2-3, my+2, ancho+6, 11, 3, stroke=0, fill=1)
            c.setFillColor(tinta)
            c.setFont("Helvetica", 7)
            c.drawCentredString(mx, my+4, etiqueta)

        # Bucles de transición.
        for estado, simbolos in bucles.items():
            x, y = posiciones[estado]
            c.setStrokeColor(gris)
            c.setLineWidth(1)
            c.arc(x-9, y+7, x+17, y+29, 15, 300)
            self._flecha(c, x+11, y+23, x+7, y+17, gris)
            c.setFillColor(tinta)
            c.setFont("Helvetica", 7)
            c.drawCentredString(x+5, y+32, ", ".join(simbolos))

        # Estados encima de las aristas.
        for estado, (x, y) in posiciones.items():
            es_inicial = estado == self.inicial
            es_final = estado in self.finales
            c.setFillColor(fondo if es_inicial else colors.white)
            c.setStrokeColor(azul if es_inicial else (colors.HexColor("#15803D") if es_final else borde))
            c.setLineWidth(1.5)
            c.circle(x, y, radio, stroke=1, fill=1)
            if es_final:
                c.circle(x, y, radio-4, stroke=1, fill=0)
            c.setFillColor(tinta)
            c.setFont("Helvetica-Bold", 7.5 if len(estado) > 5 else 8.5)
            c.drawCentredString(x, y-3, estado[:12])

        c.setFillColor(gris)
        c.setFont("Helvetica", 7)
        c.drawString(10, 8, "Flecha azul: estado inicial · Doble círculo: estado final")
        c.restoreState()


def generar_informe_pdf(automata, tipo, destino, cadena=None):
    """Genera un PDF con definición formal, tabla de transiciones y simulación opcional."""
    destino = Path(destino)
    estados = sorted((str(e) for e in automata.estados), key=str)
    alfabeto = sorted((str(a) for a in automata.alfabeto), key=str)
    finales = sorted((str(e) for e in automata.estados_finales), key=str)
    inicial = str(automata.estado_inicial)

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name="TituloInforme", parent=estilos["Title"], fontName="Helvetica-Bold", fontSize=20, leading=25, textColor=colors.HexColor("#163A63"), alignment=TA_CENTER, spaceAfter=5))
    estilos.add(ParagraphStyle(name="SubtituloInforme", parent=estilos["Normal"], alignment=TA_CENTER, textColor=colors.HexColor("#64748B"), fontSize=9, spaceAfter=15))
    estilos.add(ParagraphStyle(name="SeccionInforme", parent=estilos["Heading2"], fontSize=13, leading=17, textColor=colors.HexColor("#1D4ED8"), spaceBefore=12, spaceAfter=7, keepWithNext=True))
    estilos.add(ParagraphStyle(name="CuerpoInforme", parent=estilos["BodyText"], fontSize=9, leading=13, spaceAfter=5, wordWrap="CJK"))
    estilos.add(ParagraphStyle(name="CeldaInforme", parent=estilos["BodyText"], fontSize=8, leading=10, wordWrap="CJK"))
    estilos.add(ParagraphStyle(name="CeldaCabeceraInforme", parent=estilos["BodyText"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white))

    doc = SimpleDocTemplate(str(destino), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=17*mm, bottomMargin=17*mm, title=f"Informe técnico - {tipo}", author="SimuladorAutomatas")
    story = [
        Paragraph("SIMULADORAUTOMATAS", estilos["TituloInforme"]),
        Paragraph(f"INFORME TÉCNICO DE {escape(tipo.upper())}", estilos["SubtituloInforme"]),
        Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", estilos["SubtituloInforme"]),
        Paragraph("1. Definición formal", estilos["SeccionInforme"]),
        _p(f"Tipo de autómata: {tipo}", estilos["CuerpoInforme"]),
        _p(f"Estados ({len(estados)}): {_lista(estados)}", estilos["CuerpoInforme"]),
        _p(f"Alfabeto: {_lista(alfabeto)}", estilos["CuerpoInforme"]),
        _p(f"Estado inicial: {inicial}", estilos["CuerpoInforme"]),
        _p(f"Estados finales: {_lista(finales)}", estilos["CuerpoInforme"]),
        Paragraph("2. Diagrama del autómata", estilos["SeccionInforme"]),
        Paragraph("Representación gráfica de estados y transiciones:", estilos["CuerpoInforme"]),
        DiagramaAutomata(estados, automata.transiciones, inicial, finales),
        Spacer(1, 4*mm),
        Paragraph("3. Tabla de transiciones", estilos["SeccionInforme"]),
    ]

    datos = [[Paragraph("Estado origen", estilos["CeldaCabeceraInforme"]), Paragraph("Símbolo", estilos["CeldaCabeceraInforme"]), Paragraph("Estado(s) destino", estilos["CeldaCabeceraInforme"])]]
    for (origen, simbolo), destinos in sorted(automata.transiciones.items(), key=lambda item: (str(item[0][0]), str(item[0][1]))):
        if isinstance(destinos, (set, frozenset, list, tuple)):
            destino_txt = _lista(destinos)
        else:
            destino_txt = str(destinos)
        datos.append([_p(origen, estilos["CeldaInforme"]), _p(simbolo, estilos["CeldaInforme"]), _p(destino_txt, estilos["CeldaInforme"])])
    if len(datos) == 1:
        datos.append([Paragraph("No hay transiciones registradas.", estilos["CeldaInforme"]), "", ""])
    tabla = Table(datos, colWidths=[48*mm, 35*mm, 91*mm], repeatRows=1, hAlign="LEFT")
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D4ED8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F5F9")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([tabla, Spacer(1, 7*mm)])

    if cadena is not None:
        recorrido, aceptada = automata.obtener_recorrido(cadena)
        cadena_txt = cadena if cadena else "(cadena vacía)"
        story.append(Paragraph("4. Simulación de cadena", estilos["SeccionInforme"]))
        story.append(_p(f"Cadena evaluada: {cadena_txt}", estilos["CuerpoInforme"]))
        resultado = "ACEPTADA" if aceptada else "RECHAZADA"
        color_resultado = "#15803D" if aceptada else "#B91C1C"
        story.append(Paragraph(f'<font color="{color_resultado}"><b>Resultado: {resultado}</b></font>', estilos["CuerpoInforme"]))
        story.append(Paragraph("Recorrido de la simulación", estilos["Heading3"]))
        if recorrido:
            for i, paso in enumerate(recorrido, start=1):
                story.append(_p(f"Paso {i}: {paso}", estilos["CuerpoInforme"]))
        else:
            story.append(_p("El simulador no devolvió pasos para esta cadena.", estilos["CuerpoInforme"]))

    story.extend([
        Paragraph("Observaciones", estilos["SeccionInforme"]),
        _p("Este documento describe la definición del autómata y, cuando se indicó una cadena, el resultado de la simulación realizada por el proyecto. Verifique los datos antes de presentar o distribuir el informe.", estilos["CuerpoInforme"]),
    ])

    def pie_pagina(canvas, documento):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
        canvas.line(18*mm, 13*mm, A4[0]-18*mm, 13*mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748B"))
        canvas.drawString(18*mm, 8*mm, "SimuladorAutomatas · Informe técnico")
        canvas.drawRightString(A4[0]-18*mm, 8*mm, f"Página {documento.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=pie_pagina, onLaterPages=pie_pagina)
    return destino
