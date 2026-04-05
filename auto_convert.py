import os
import shutil
from pypdf import PdfWriter, PdfReader
from ebooklib import epub

# ============================================================
# CONFIGURE THESE
# ============================================================
INPUT_PDF = r"D:\books\mybook.pdf"  # ← your PDF path
OUTPUT_EPUB = r"D:\books\mybook.epub"  # ← final merged EPUB
BOOK_TITLE = "اعمل بذكاء وليس بجهد"  # ← book title
AUTHOR_NAME = "كيفين بول"  # ← author name
PAGES_PER_CHUNK = 50  # ← pages per chunk
# ============================================================

CHUNKS_FOLDER = "chunks"
EPUB_FOLDER = "epub_chunks"


# ── Step 1: Split PDF ────────────────────────────────────────
def split_pdf():
    os.makedirs(CHUNKS_FOLDER, exist_ok=True)
    reader = PdfReader(INPUT_PDF)
    total = len(reader.pages)
    print(f"\n📄 Total pages: {total}")
    print(f"✂️  Splitting into chunks of {PAGES_PER_CHUNK} pages...\n")

    chunk_files = []
    for i in range(0, total, PAGES_PER_CHUNK):
        writer = PdfWriter()
        end = min(i + PAGES_PER_CHUNK, total)
        for j in range(i, end):
            writer.add_page(reader.pages[j])
        chunk_name = os.path.join(CHUNKS_FOLDER, f"chunk_{i+1}_to_{end}.pdf")
        with open(chunk_name, "wb") as f:
            writer.write(f)
        print(f"  ✅ Saved: {chunk_name}")
        chunk_files.append(chunk_name)

    print(f"\n✅ Split complete! {len(chunk_files)} chunks created.\n")
    return chunk_files


# ── Step 2: Convert each chunk to EPUB ──────────────────────
def convert_chunks(chunk_files):
    os.makedirs(EPUB_FOLDER, exist_ok=True)
    epub_files = []

    for i, chunk_pdf in enumerate(chunk_files):
        chunk_epub = os.path.join(
            EPUB_FOLDER, os.path.basename(chunk_pdf).replace(".pdf", ".epub")
        )
        print(f"📚 Converting chunk {i+1}/{len(chunk_files)}: {chunk_pdf}")

        # Temporarily patch the config in convert_pdf_to_epub
        import convert_pdf_to_epub as converter

        converter.INPUT_PDF = chunk_pdf
        converter.OUTPUT_EPUB = chunk_epub
        converter.BOOK_TITLE = BOOK_TITLE
        converter.AUTHOR_NAME = AUTHOR_NAME
        converter.FORCE_OCR = True

        try:
            converter.main()
            if os.path.exists(chunk_epub):
                print(f"  ✅ Done: {chunk_epub}\n")
                epub_files.append(chunk_epub)
            else:
                print(f"  ⚠️ EPUB not created for chunk {i+1}\n")
        except Exception as e:
            print(f"  ❌ Error on chunk {i+1}: {e}\n")

    return epub_files


# ── Step 3: Merge all EPUBs ──────────────────────────────────
def merge_epubs(epub_files):
    print(f"\n🔗 Merging {len(epub_files)} EPUB files...\n")

    merged_book = epub.EpubBook()
    merged_book.set_title(BOOK_TITLE)
    merged_book.set_language("ar")
    merged_book.add_author(AUTHOR_NAME)

    spine = ["nav"]
    all_items = []
    chapter_num = 0

    for epub_file in epub_files:
        if not os.path.exists(epub_file):
            print(f"  ⚠️ Skipping missing file: {epub_file}")
            continue

        print(f"  📖 Merging: {epub_file}")
        book = epub.read_epub(epub_file)

        for item in book.get_items():
            if item.get_type() == 9:  # ITEM_DOCUMENT
                chapter_num += 1
                item.id = f"chapter_{chapter_num}"
                item.file_name = f"chapter_{chapter_num}.xhtml"
                merged_book.add_item(item)
                all_items.append(item)
                spine.append(item)

    merged_book.toc = all_items
    merged_book.add_item(epub.EpubNcx())
    merged_book.add_item(epub.EpubNav())
    merged_book.spine = spine

    epub.write_epub(OUTPUT_EPUB, merged_book)
    print(f"\n✅ Final EPUB saved: {OUTPUT_EPUB}")


# ── Run everything ───────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  AUTO PDF TO EPUB CONVERTER")
    print("=" * 60)

    chunk_files = split_pdf()
    epub_files = convert_chunks(chunk_files)
    merge_epubs(epub_files)

    print("\n" + "=" * 60)
    print("  ✅ ALL DONE!")
    print(f"  📚 Your EPUB: {OUTPUT_EPUB}")
    print("=" * 60)
