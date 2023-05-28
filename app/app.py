import os

import openai
from flask import Flask, render_template, request, send_file

from app.DocsGenerator import DocsGenerator

app = Flask(__name__)
openai.api_type = "azure"
openai.api_version = "2022-12-01"
openai.api_base = "https://leothon4.openai.azure.com/"  # Your Azure OpenAI resource's endpoint value.
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/consultation", methods=["GET"])
def consultation():
    return render_template("consultation.html")


@app.route("/renderDocument", methods=["POST"])
def renderDocument():
    generator = DocsGenerator(static_data=get_static_data())
    patient_data = {
        "name": request.form["Name"],
        "surname": request.form["Surname"],
        "pesel": request.form["PESEL"],
        "address": request.form["Zip_Code"]
    }
    docs = generator.generate_docs(patient_data=patient_data, gpt_response="Test")
    return send_file(
        docs,
        as_attachment=True,
        attachment_filename='report.docx'
    )


def get_static_data():
    static_data = {
        "header": "Centrum Medycyny: Warszawa CM Atrium\n"
                  "Medicover Opieka Ambulatoryjna 010210201201\n"
                  "Poradnia medycyny pracy - 154",
        "footer": "Lek.med Josh Giibun\n"
                  "specjalista medycyny pracy\n"
                  "420692137"
    }
    return static_data
