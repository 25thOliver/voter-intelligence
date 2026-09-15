import pdfplumber
import sys

PDF_PATH = "/data/raw/registered_voters_2017.pdf"
TARGET_COUNTY_CODE = "040"          
TARGET_COUNTY_NAME_PREFIX = "BUSI"  # backup check, tolerant of truncation


def row_matches_target(row):
    if not row or len(row) < 2:
        return False
    code = (row[0] or "").strip()
    name = (row[1] or "").strip().upper()
    return code == TARGET_COUNTY_CODE or name.startswith(TARGET_COUNTY_NAME_PREFIX)


def find_county_rows(pdf_path):
    matched_pages = []
    sample_rows = []
    in_block = False
    consecutive_misses = 0

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")

        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()  # ALL tables on the page, not just first
            page_has_match = False

            for table in tables:
                for row in table:
                    if row_matches_target(row):
                        page_has_match = True
                        if len(sample_rows) < 10:
                            sample_rows.append((i + 1, row))

            if page_has_match:
                matched_pages.append(i + 1)
                in_block = True
                consecutive_misses = 0
            elif in_block:
                consecutive_misses += 1
                if consecutive_misses >= 3:
                    print(f"Exiting block — 3 consecutive non-matching pages after page {i + 1}")
                    break

            if i % 50 == 0:
                print(f"Scanned {i + 1}/{total_pages}...")

    return matched_pages, sample_rows


if __name__ == "__main__":
    pages, samples = find_county_rows(PDF_PATH)

    if pages:
        is_contiguous = pages == list(range(pages[0], pages[-1] + 1))
        print(f"\nMatched pages: {pages[0]} to {pages[-1]} ({len(pages)} pages, contiguous={is_contiguous})")
        print("\nSample matched rows:")
        for p, r in samples:
            print(f"  page {p}: {r}")
    else:
        print("No matches found.")
        sys.exit(1)