"""Generador de reportes en PDF"""

from typing import Optional, List
from datetime import datetime
from loguru import logger

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


class GeneradorPDF:
    """Generador de reportes en formato PDF"""

    def __init__(self, titulo: str = "YeraPOV", tamano: str = "A4"):
        """
        Inicializar generador de PDF
        
        Args:
            titulo: Título del reporte
            tamano: Tamaño de página (A4, letter)
        """
        self.titulo = titulo
        self.tamano = A4 if tamano == "A4" else letter
        logger.info(f"Generador PDF inicializado. Tímano: {tamano}")

    def generar_reporte_ventas(
        self,
        ruta_salida: str,
        ventas: List,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
    ) -> bool:
        """
        Generar reporte de ventas en PDF
        
        Args:
            ruta_salida: Ruta donde guardar el PDF
            ventas: Lista de ventas
            fecha_inicio: Fecha de inicio del reporte
            fecha_fin: Fecha de fin del reporte
            
        Returns:
            True si se generó exitosamente
        """
        try:
            doc = SimpleDocTemplate(ruta_salida, pagesize=self.tamano)
            elements = []
            
            # Estilos
            styles = getSampleStyleSheet()
            titulo_style = ParagraphStyle(
                "Titulo",
                parent=styles["Heading1"],
                fontSize=18,
                textColor=colors.HexColor("#1f4788"),
                spaceAfter=12,
                alignment=1,  # Centrado
            )
            
            # Título
            elements.append(Paragraph(f"{self.titulo} - Reporte de Ventas", titulo_style))
            elements.append(Spacer(1, 0.3 * inch))
            
            # Período
            if fecha_inicio and fecha_fin:
                periodo = f"Período: {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}"
            else:
                periodo = f"Reporte generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            
            elements.append(Paragraph(periodo, styles["Normal"]))
            elements.append(Spacer(1, 0.2 * inch))
            
            # Tabla de ventas
            data = [["N° Venta", "Fecha", "Vendedor", "Cliente", "Monto"]]
            total_ventas = 0
            
            for venta in ventas:
                data.append([
                    venta.numero_venta,
                    venta.fecha_venta.strftime("%d/%m/%Y %H:%M"),
                    venta.vendedor.nombre_completo if venta.vendedor else "-",
                    venta.cliente_nombre or "-",
                    f"${venta.total:.2f}",
                ])
                total_ventas += venta.total
            
            # Agregar fila de totales
            data.append(["", "", "", "TOTAL:", f"${total_ventas:.2f}"])
            
            # Crear tabla
            tabla = Table(data, colWidths=[1.2*inch, 1.2*inch, 1.5*inch, 1.5*inch, 1*inch])
            tabla.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4788")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(tabla)
            
            # Generar PDF
            doc.build(elements)
            logger.info(f"Reporte PDF generado: {ruta_salida}")
            return True
            
        except Exception as e:
            logger.error(f"Error generando PDF: {e}")
            return False
