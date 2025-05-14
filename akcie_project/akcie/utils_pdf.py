# Luxusní vodoznak a branding pro PDF exporty
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor

def add_luxury_branding(pdf_canvas):
    # Luxusní vodoznak
    pdf_canvas.saveState()
    pdf_canvas.setFont("Helvetica-Bold", 48)
    pdf_canvas.setFillColor(HexColor("#e0e7ef"))
    pdf_canvas.rotate(30)
    pdf_canvas.drawString(120, 200, "Finanční Poradce Premium")
    pdf_canvas.restoreState()
    # Logo nebo další branding lze přidat zde
