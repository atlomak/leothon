import pytest

from app.DocsGenerator import DocsGenerator

static_data = {
    "header": "Centrum Medycyny: Warszawa CM Atrium\n"
              "Medicover Opieka Ambulatoryjna 010210201201\n"
              "Poradnia medycyny pracy - 154",
    "footer": "Lek.med Josh Giibun\n"
              "specjalista medycyny pracy\n"
              "420692137"
}


@pytest.fixture
def get_patient_data():
    patien_data = {
        "name": "Jan",
        "surname": "Kowalski",
        "pesel": "12345678901",
        "address": "ul. Kowalska 1/1, 00-000 Warszawa"
    }
    return patien_data


@pytest.fixture
def get_chatgpt_response():
    return "Headache during the day. No fever. No cough. No runny nose. Pain in the throat"


@pytest.fixture
def generator():
    return DocsGenerator(static_data=static_data)


def test_generate_docs(generator, get_patient_data, get_chatgpt_response):
    file = generator.generate_docs(get_patient_data, get_chatgpt_response)
    with open("tests/output/example.docx", "wb") as f:
        f.write(file.getbuffer())
