import pdfplumber

PDF_PATH = "/data/raw/registered_voters_2017.pdf"
DEBUG_PAGE = 890

with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[DEBUG_PAGE - 1]

    for tol in [3, 2, 1, 0.5, 0.3, 0.1]:
        words = page.extract_words(x_tolerance=tol)
        first_row_words = [w['text'] for w in words[:8]]
        print(f"x_tolerance={tol}: {first_row_words}")