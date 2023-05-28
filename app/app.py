from flask import Flask, render_template, request, send_file

from .DocsGenerator import DocsGenerator
from .gptintegrator import get_openai_response

app = Flask(__name__)


@app.route("/consultation", methods=["GET"])
def consultation():
    return render_template("consultation.html")

@app.route("/", methods=["GET", "PUT"])
def index():
    return render_template("index.html")

@app.route("/renderDocument", methods=["POST"])
def renderDocument():
    generator = DocsGenerator(static_data=get_static_data())
    patient_data = {
        "name": request.form["Name"],
        "surname": request.form["Surname"],
        "pesel": request.form["PESEL"],
        "address": request.form["Zip_Code"]
    }
    audio_desc = request.form["audio_desc"]
    docs = generator.generate_docs(patient_data=patient_data,
                                   gpt_response=get_openai_response(audio_desc))

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
