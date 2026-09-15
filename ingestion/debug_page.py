import pdfplumber

PDF_PATH = "/data/raw/registered_voters_2017.pdf"
DEBUG_PAGE = 890 # An indexed page I know has Busia rows

with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[DEBUG_PAGE - 1]

    # Save a visual snapshot with detected table lines drawn on it
    im = page.to_image(resolution=200)
    im.debug_tablefinder().save("/data/processed/debug_page_890.png")

    # Print raw words with their x-coordinates so we can see actual column boundaries
    words = page.extract_words()
    print(f"First 30 words with positions on page {DEBUG_PAGE}:")
    for w in words[:30]:
        print(f"  x0={w['x0']:.1f} x1={w['x1']:.1f}  text='{w['text']}'")
