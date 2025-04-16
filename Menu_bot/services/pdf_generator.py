from xhtml2pdf import pisa
import os

def generate_pdf(html_content, filename='proposal.pdf'):
    with open(filename, "wb") as f:
        pisa.CreatePDF(html_content, dest=f)
    return os.path.abspath(filename)
