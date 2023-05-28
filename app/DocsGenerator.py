from io import BytesIO

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches


class DocsGenerator:
    def __init__(self, static_data: dict):
        self.header = static_data["header"]
        self.footer = static_data["footer"]

    def generate_docs(self, patient_data: dict, gpt_response: str):
        document = Document()

        sections = document.sections
        for section in sections:
            section.bottom_margin = Inches(0.5)

        logo_paragraph = document.add_paragraph()
        logo_run = logo_paragraph.add_run()
        logo_run.add_picture("app/static/example_logo.jpg", width=Inches(1))

        title_paragraph = document.add_paragraph()
        title_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        title_run = title_paragraph.add_run("APPOINTMENT CARD")
        title_run.bold = True

        patient = document.add_paragraph()
        patient.add_run("Name: ").bold = True
        patient.add_run(patient_data["name"] + "\n")
        patient.add_run("Surname: ").bold = True
        patient.add_run(patient_data["surname"] + "\n")
        patient.add_run("PESEL: ").bold = True
        patient.add_run(patient_data["pesel"] + "\n")
        patient.add_run("Address: ").bold = True
        patient.add_run(patient_data["address"] + "\n")

        document.add_heading("SYMPTHOMS/PATIENT INTERVIEW", level=1)
        document.add_paragraph(gpt_response)

        document.add_heading("RECOMMENDATIONS", level=1)
        document.add_paragraph("***** TO BE FILLED BY THE DOCTOR *****")

        footer_paragraph = document.sections[-1].footer.paragraphs[0]
        footer_paragraph.text = self.footer
        footer_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        document_buffer = BytesIO()
        document.save(document_buffer)
        return document_buffer
