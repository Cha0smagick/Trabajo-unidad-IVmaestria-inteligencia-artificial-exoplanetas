import pdfplumber
import os

base_path = r"D:\UNIVERSIDADES\0. maestria Politecnico gran colombiano\II sem II - inteligencia artificial\Trabajo unidad IV"

files = [
    "U4_Actividad_Sumativa.pdf",
    "U4_Lectura_Fundamental (1).pdf"
]

for fname in files:
    fpath = os.path.join(base_path, fname)
    print(f"=== {fname} ===")
    try:
        with pdfplumber.open(fpath) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    print(f"--- Page {i+1} ---")
                    print(text)
        print()
    except Exception as e:
        print(f"Error reading {fname}: {e}")
        print()