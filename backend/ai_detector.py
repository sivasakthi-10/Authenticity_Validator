import os
import PyPDF2
import docx

# Read PDF
def extract_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# Read DOCX
def extract_docx(filepath):
    document = docx.Document(filepath)
    text = ""
    for para in document.paragraphs:
        text += para.text + "\n"
    return text

# Read TXT
def extract_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

# Extract text based on file type
def extract_text(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":
        return extract_pdf(filepath)

    elif extension == ".docx":
        return extract_docx(filepath)

    elif extension == ".txt":
        return extract_txt(filepath)

    return ""

# Basic AI detection
def detect_ai_text(filepath):

    text = extract_text(filepath)

    if len(text.strip()) == 0:
        return 0

    words = text.split()
    sentences = text.split(".")

    if len(sentences) == 0:
        return 0

    avg_words = len(words) / len(sentences)

    ai_score = 0

    # Rule 1
    if avg_words > 20:
        ai_score += 30

    # Rule 2
    repeated = len(words) - len(set(words))

    if repeated > len(words) * 0.30:
        ai_score += 20

    # Rule 3
    ai_keywords = [
        "therefore",
        "furthermore",
        "moreover",
        "in conclusion",
        "overall",
        "consequently"
    ]

    for keyword in ai_keywords:
        if keyword.lower() in text.lower():
            ai_score += 10

    if ai_score > 100:
        ai_score = 100

    return round(ai_score, 2)
