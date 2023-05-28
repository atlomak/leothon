import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_type = "azure"
openai.api_version = "2022-12-01"
openai.api_base = "https://leothon4.openai.azure.com/"  # Your Azure OpenAI resource's endpoint value.
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        results = dict()
        results["Name"] = request.form["Name"]
        results["Surname"] = request.form["Surname"]
        results["PESEL"] = request.form["PESEL"]
        results["Zip_code"] = request.form["Zip_Code"]
        print(results)
        return redirect(url_for("", result=results))

    result = request.args.get("result")
    return render_template("consultation.html", result=result)
