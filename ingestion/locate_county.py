import pdfplumber
import sys

PDF_PATH = "/data/raw/registered_voters_2017.pdf"
TARGET_COUNTY_CODE = "040"          
TARGET_COUNTY_NAME_PREFIX = "BUSI"  # backup check, tolerant of truncation

def find_county_pages(pdf_path, target_county, max_pages_to_scan=None):
    """
    Scans the PDF page by page, checking the first table's rows for the
    target county name. Prints page numbers where it appears.
    Stops scanning once we've found the county AND then left it
    (since counties appear to be in contiguous blocks).
    """
    found_pages = []
    in_target_block = False

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages in PDF: {total_pages}")

        pages_to_scan = total_pages if not max_pages_to_scan else min(max_pages_to_scan, total_pages)

        for i in range(pages_to_scan):
            page = pdf.pages[i]
            text = page.extract_text() or ""

            if target_county in text.upper():
                found_pages.append(i+1)
                in_target_block = True
            elif in_target_block:
                print(f"Appears to exit {target_county} block after page {i}")
                break

            if i % 50 == 0:
                print(f"Scanned page {i+1}/{pages_to_scan}...")

    return found_pages

if __name__ == "__main__":
    pages = find_county_pages(PDF_PATH, TARGET_COUNTY)

    if pages:
        print(f"\n{TARGET_COUNTY} found on pages: {pages[0]} to {pages[-1]} ({len(pages)} pages)")

        with pdfplumber.open(PDF_PATH) as pdf:
            sample_page = pdf.pages[pages[0] - 1]
            table = sample_page.extract_table()

            if table:
                print(f"\nSample table from page {pages[0]} (first 5 rows):")
                for row in table[:5]:
                    print(row)
            else:
                print("No table detected on this page — may need different extraction settings.")
    else:
        print(f"{TARGET_COUNTY} not found. You may need to check spelling/encoding, or scan full document.")
        sys.exit(1)
