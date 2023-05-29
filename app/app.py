import os

from flask import Flask, redirect, render_template, request, send_file, session
import whisper
from .DocsGenerator import DocsGenerator
from .gptintegrator import get_openai_response

app = Flask(__name__)


@app.route("/consultation", methods=["GET"])
def consultation():
    return render_template("consultation.html")


@app.route("/", methods=["GET", "PUT"])
def index():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    else:
        return render_template("login.html")

app.secret_key = os.getenv("SECRET_KEY")
@app.route("/login", methods=["POST"])
def login():
    login = request.form["name"]
    password = request.form["password"]
    if login == "admin" and password == "admin":
        session["user"] = {"name": "admin", "surname": "admin"}
        return render_template("index.html", user=session["user"])
    else:
        return "Wrong login or password"

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user", None)
    return render_template("login.html")

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
                                   gpt_response=get_openai_response(get_transcription()))

    return send_file(
        docs,
        as_attachment=True,
        attachment_filename='report.docx'
    )


@app.route("/upload_audio", methods=["POST"])
def get_audio():
    file = request.files["audio"]
    patient_data = {
        "name": request.form["firstName"],
        "surname": request.form["lastName"],
        "pesel": request.form["pesel"],
    }
    with open("audio.wav", "wb") as f:
        f.write(file.read())
    audio_desc = get_transcription()
    return redirect("/consultation")

def get_transcription():
    model = whisper.load_model("base")
    audio_desc = model.transcribe(audio="audio.wav", temperature=0.7, verbose=0, language="polish")["text"]
    return audio_desc

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
