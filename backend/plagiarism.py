from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import PyPDF2
import docx

# Read text from PDF
def extract_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# Read text from DOCX
def extract_docx(filepath):
    document = docx.Document(filepath)
    text = ""
    for para in document.paragraphs:
        text += para.text + "\n"
    return text

# Read text from TXT
def extract_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

# Detect file type and extract text
def extract_text(filepath):
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":
        return extract_pdf(filepath)

    elif extension == ".docx":
        return extract_docx(filepath)

    elif extension == ".txt":
        return extract_txt(filepath)

    else:
        return ""

# Dummy reference text
REFERENCE_TEXT = """
Academic integrity is the foundation of education.
Students should submit their own original work.
Plagiarism is copying someone else's work without proper citation.
Artificial Intelligence tools should be used responsibly.
"""

# Calculate plagiarism score
def check_plagiarism(filepath):

    uploaded_text = extract_text(filepath)

    if uploaded_text.strip() == "":
        return 0

    documents = [uploaded_text, REFERENCE_TEXT]

    vectorizer = TfidfVectorizer()

    tfidf = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])

    score = similarity[0][0] * 100

    return round(score, 2)
