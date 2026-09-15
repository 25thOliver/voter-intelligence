import pdfplumber

PDF_PATH = "/data/raw/registered_voters_2017.pdf"
DEBUG_PAGE = 890

with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[DEBUG_PAGE - 1]
    chars = page.chars

    # Look at the character sequence around where "BUNGOMA224" was formed
    # (roughly x0=90 to x1=152 based on earlier word extraction)
    relevant = [c for c in chars if 85 <= c['x0'] <= 160]
    relevant.sort(key=lambda c: c['x0'])

    print(f"Characters between x=85 and x=160 on page {DEBUG_PAGE}:")
    prev_x1 = None
    for c in relevant:
        gap = c['x0'] - prev_x1 if prev_x1 is not None else 0
        print(f"  char='{c['text']}'  x0={c['x0']:.2f}  x1={c['x1']:.2f}  gap_from_prev={gap:.2f}")
        prev_x1 = c['x1']