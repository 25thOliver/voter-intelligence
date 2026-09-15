import pdfplumber

PDF_PATH = "/data/raw/registered_voters_2017.pdf"
DEBUG_PAGE = 890

with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[DEBUG_PAGE - 1]
    chars = page.chars

    # First, find distinct row bands by clustering on 'top' (vertical position)
    tops = sorted(set(round(c['top'], 1) for c in chars))
    print(f"Distinct 'top' values found (first 10): {tops[:10]}")

    # Pick the first row's top value and get ONLY characters on that row
    first_row_top = tops[0]
    row_chars = [c for c in chars if abs(c['top'] - first_row_top) < 1.0]
    row_chars.sort(key=lambda c: c['x0'])

    print(f"\nCharacters on row at top={first_row_top}:")
    prev_x1 = None
    for c in row_chars:
        gap = c['x0'] - prev_x1 if prev_x1 is not None else 0
        print(f"  char='{c['text']}'  x0={c['x0']:.2f}  x1={c['x1']:.2f}  gap_from_prev={gap:.2f}")
        prev_x1 = c['x1']