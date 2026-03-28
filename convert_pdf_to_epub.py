#!/usr/bin/env python3
"""
PDF to EPUB Converter
Converts Arabic PDFs (scanned or text-based) to EPUB format with RTL support.

This script automatically detects whether a PDF is scanned (needs OCR) or text-based,
extracts the content, and creates a properly formatted EPUB3 file.
"""

import os
import sys
from pathlib import Path

# ============================================================================
# USER CONFIGURATION - Edit these values
# ============================================================================

# Path to your input PDF file
INPUT_PDF = "D:\\books\\podcast-code.pdf"

# Path where the EPUB file will be saved
OUTPUT_EPUB = "test_output\mybook.epub"

# Book metadata
BOOK_TITLE = "شيفره البودكاست المفقوده"
AUTHOR_NAME = "محمد موسي"

# Force OCR mode (set to True if PDF has custom font encoding issues)
# Set to True if you're getting garbled text in the output
FORCE_OCR = False

# ============================================================================
# END OF USER CONFIGURATION
# ============================================================================


def check_dependencies():
    """Check if all required packages are installed."""
    missing_packages = []
    
    try:
        import pdf2image
    except ImportError:
        missing_packages.append("pdf2image")
    
    try:
        import pytesseract
    except ImportError:
        missing_packages.append("pytesseract")
    
    try:
        import PyPDF2
    except ImportError:
        missing_packages.append("PyPDF2")
    
    try:
        import ebooklib
    except ImportError:
        missing_packages.append("ebooklib")
    
    try:
        from PIL import Image
    except ImportError:
        missing_packages.append("Pillow")
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\nPlease install them by running:")
        print("   pip3 install -r requirements.txt")
        print("   or")
        print("   ./install.sh")
        return False
    
    # Check if Tesseract is installed
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
    except Exception:
        print("⚠️  Warning: Tesseract OCR is not installed or not in PATH.")
        print("   For scanned PDFs, install it with: brew install tesseract tesseract-lang")
        print("   Continuing anyway for text-based PDFs...")
    
    # Check if Poppler is available (for pdf2image)
    try:
        from pdf2image import convert_from_path
        # Try a test conversion to check Poppler
        test_path = Path(INPUT_PDF)
        if test_path.exists():
            # Just check if the command would work
            pass
    except Exception as e:
        print(f"⚠️  Warning: Poppler utilities may not be installed: {e}")
        print("   Install with: brew install poppler")
    
    return True


def has_garbled_text(text):
    """
    Check if extracted text contains garbled characters (private use area Unicode).
    This indicates custom font encoding issues.
    """
    if not text or len(text.strip()) < 10:
        return False  # Too short to determine
    
    # Check for private use area characters (U+F000-U+FFFF)
    # These indicate custom font encoding issues
    sample = text[:1000]  # Check first 1000 chars
    private_use_chars = sum(1 for c in sample if '\uf000' <= c <= '\uffff')
    total_non_space = len([c for c in sample if not c.isspace()])
    
    if total_non_space > 0:
        garbled_ratio = private_use_chars / total_non_space
        # If more than 20% are private use characters, text is likely garbled
        if garbled_ratio > 0.2:
            return True
    
    # Also check: if we have many private use chars (even if ratio is lower)
    # and the text doesn't look like normal Arabic/English, it's garbled
    if private_use_chars > 20:
        # Count proper Arabic and Latin characters
        proper_chars = sum(1 for c in sample if 
                          ('\u0600' <= c <= '\u06FF') or  # Arabic
                          ('\u0000' <= c <= '\u007F'))    # Basic Latin
        if proper_chars < private_use_chars:
            return True
    
    return False


def is_scanned_pdf(pdf_path):
    """
    Detect if a PDF is scanned (image-based) or text-based.
    Also checks if text extraction produces garbled output (custom font encoding).
    
    Returns:
        True if PDF appears to be scanned OR has garbled text (needs OCR)
        False if PDF contains extractable, properly encoded text
    """
    try:
        # Try pdfplumber first for better detection
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                pages_to_check = min(2, len(pdf.pages))
                text_content = ""
                
                for i in range(pages_to_check):
                    page = pdf.pages[i]
                    text = page.extract_text()
                    if text:
                        text_content += text
                
                # Check if text is garbled
                if text_content and has_garbled_text(text_content):
                    print("   ⚠️  Detected garbled text (custom font encoding) - will use OCR")
                    return True
                
                # If we found meaningful, non-garbled text, it's text-based
                if len(text_content.strip()) > 100:
                    return False
        except ImportError:
            pass
        
        # Fallback to PyPDF2
        import PyPDF2
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check first few pages for text content
            text_content = ""
            pages_to_check = min(3, len(pdf_reader.pages))
            
            for i in range(pages_to_check):
                page = pdf_reader.pages[i]
                text = page.extract_text()
                if text and len(text.strip()) > 50:
                    text_content += text
            
            # Check if text is garbled
            if text_content and has_garbled_text(text_content):
                print("   ⚠️  Detected garbled text (custom font encoding) - will use OCR")
                return True
            
            # If we found meaningful, non-garbled text, it's text-based
            if len(text_content.strip()) > 100:
                return False
            
            # Otherwise, assume it's scanned
            return True
            
    except Exception as e:
        print(f"⚠️  Error checking PDF type: {e}")
        print("   Assuming scanned PDF (will use OCR)...")
        return True


def extract_with_ocr(pdf_path):
    """
    Extract text from scanned PDF using Tesseract OCR with Arabic language support.
    
    Returns:
        List of text strings, one per page
    """
    try:
        from pdf2image import convert_from_path
        import pytesseract
        
        print("📄 Converting PDF pages to images...")
        # Convert PDF pages to images
        images = convert_from_path(pdf_path, dpi=300)
        
        print(f"🔍 Performing OCR on {len(images)} pages (this may take a while)...")
        extracted_texts = []
        
        for i, image in enumerate(images, 1):
            print(f"   Processing page {i}/{len(images)}...", end='\r')
            
            # Use Arabic language for OCR
            # Tesseract language code: 'ara' for Arabic
            text = pytesseract.image_to_string(image, lang='ara')
            extracted_texts.append(text)
        
        print(f"\n✅ OCR complete! Extracted text from {len(images)} pages.")
        return extracted_texts
        
    except ImportError:
        print("❌ Error: pdf2image or pytesseract not installed.")
        print("   Install with: pip3 install pdf2image pytesseract")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during OCR: {e}")
        print("   Make sure Tesseract is installed: brew install tesseract tesseract-lang")
        sys.exit(1)


def extract_text_directly(pdf_path):
    """
    Extract text directly from text-based PDF.
    Uses pdfplumber for better Arabic text extraction, falls back to PyPDF2.
    
    Returns:
        List of text strings, one per page
    """
    # Try pdfplumber first (better Arabic support)
    try:
        import pdfplumber
        
        print("📖 Extracting text from PDF (using pdfplumber for better Arabic support)...")
        extracted_texts = []
        
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages, 1):
                print(f"   Processing page {i}/{total_pages}...", end='\r')
                text = page.extract_text()
                if text:
                    # Ensure proper UTF-8 encoding
                    if isinstance(text, bytes):
                        text = text.decode('utf-8', errors='ignore')
                    extracted_texts.append(text)
                else:
                    extracted_texts.append("")
        
        print(f"\n✅ Text extraction complete! Processed {total_pages} pages.")
        return extracted_texts
        
    except ImportError:
        # Fallback to PyPDF2 if pdfplumber not available
        print("📖 Extracting text from PDF (using PyPDF2)...")
        print("   Note: For better Arabic support, install pdfplumber: pip install pdfplumber")
    except Exception as e:
        print(f"⚠️  pdfplumber extraction failed: {e}")
        print("   Falling back to PyPDF2...")
    
    # Fallback to PyPDF2
    try:
        import PyPDF2
        
        extracted_texts = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            for i, page in enumerate(pdf_reader.pages, 1):
                print(f"   Processing page {i}/{total_pages}...", end='\r')
                text = page.extract_text()
                if text:
                    # Try to fix encoding issues
                    if isinstance(text, bytes):
                        text = text.decode('utf-8', errors='ignore')
                    # Try alternative encodings if UTF-8 fails
                    elif not all(ord(c) < 128 or '\u0600' <= c <= '\u06FF' for c in text[:100] if text):
                        # Text might be in wrong encoding, try to fix
                        try:
                            text = text.encode('latin-1', errors='ignore').decode('utf-8', errors='ignore')
                        except:
                            pass
                    extracted_texts.append(text)
                else:
                    extracted_texts.append("")
        
        print(f"\n✅ Text extraction complete! Processed {total_pages} pages.")
        return extracted_texts
        
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        sys.exit(1)


def format_arabic_html(text, page_number):
    """
    Format Arabic text with proper RTL HTML structure.
    
    Args:
        text: The text content for this page
        page_number: Page number for the chapter
    
    Returns:
        HTML string with RTL support
    """
    import html
    
    # Ensure text is properly decoded
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='ignore')
    
    # Clean up the text
    text = text.strip()
    
    # Split into paragraphs (double newlines)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    # If no paragraphs found, split by single newlines
    if not paragraphs:
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    # Build HTML
    html_content = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Page """ + str(page_number) + """</title>
    <style>
        body {
            font-family: 'Arial', 'DejaVu Sans', 'Tahoma', sans-serif;
            font-size: 1.2em;
            line-height: 1.8;
            direction: rtl;
            text-align: right;
            margin: 2em;
            padding: 0;
            unicode-bidi: bidi-override;
        }
        p {
            margin: 1em 0;
            text-align: justify;
            unicode-bidi: embed;
        }
        .page-break {
            page-break-after: always;
        }
    </style>
</head>
<body>
"""
    
    # Add paragraphs with proper HTML escaping
    for para in paragraphs:
        # Escape HTML entities but preserve Arabic characters
        escaped_para = html.escape(para)
        html_content += f"    <p>{escaped_para}</p>\n"
    
    html_content += """</body>
</html>
"""
    
    return html_content


def create_epub(text_pages, output_path, title, author):
    """
    Create an EPUB3 file with Arabic RTL support.
    
    Args:
        text_pages: List of text strings (one per page)
        output_path: Path where EPUB file will be saved
        title: Book title
        author: Author name
    """
    try:
        import ebooklib
        from ebooklib import epub
        
        print(f"📚 Creating EPUB file: {output_path}")
        
        # Create EPUB book
        book = epub.EpubBook()
        
        # Set metadata
        book.set_identifier('pdf-to-epub-' + str(hash(title)))
        book.set_title(title)
        book.set_language('ar')  # Arabic language
        book.add_author(author)
        
        # Create table of contents
        chapters = []
        
        # Create a chapter for each page
        for i, page_text in enumerate(text_pages, 1):
            if not page_text.strip():
                continue  # Skip empty pages
            
            # Format HTML for this page
            html_content = format_arabic_html(page_text, i)
            
            # Create chapter
            chapter_id = f'chapter_{i}'
            chapter = epub.EpubHtml(
                title=f'Page {i}',
                file_name=f'{chapter_id}.xhtml',
                lang='ar'
            )
            chapter.content = html_content.encode('utf-8')
            chapter.set_language('ar')
            
            # Add to book
            book.add_item(chapter)
            chapters.append(chapter)
        
        # Create table of contents
        book.toc = [(chapter, f'Page {i+1}') for i, chapter in enumerate(chapters)]
        
        # Add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Define spine (reading order)
        book.spine = ['nav'] + chapters
        
        # Write EPUB file
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        epub.write_epub(str(output_path_obj), book, {})
        
        print(f"✅ EPUB file created successfully!")
        print(f"   Location: {output_path}")
        print(f"   Pages: {len(chapters)}")
        
    except Exception as e:
        print(f"❌ Error creating EPUB: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main conversion function."""
    print("=" * 60)
    print("PDF to EPUB Converter - Arabic Support")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies found!")
    print()
    
    # Check if input PDF exists
    input_path = Path(INPUT_PDF)
    if not input_path.exists():
        print(f"❌ Error: Input PDF not found: {INPUT_PDF}")
        print()
        print("Please edit the script and set INPUT_PDF to your PDF file path.")
        sys.exit(1)
    
    print(f"📄 Input PDF: {INPUT_PDF}")
    print(f"📚 Output EPUB: {OUTPUT_EPUB}")
    print()
    
    # Detect PDF type
    print("🔍 Detecting PDF type...")
    
    # Check if user forced OCR mode
    if FORCE_OCR:
        print("   Using OCR mode (FORCE_OCR is enabled)")
        print("   This is recommended for PDFs with custom font encoding")
        print()
        extracted_texts = extract_with_ocr(str(input_path))
    else:
        is_scanned = is_scanned_pdf(str(input_path))
        
        if is_scanned:
            print("   Detected: Scanned PDF (will use OCR)")
            print()
            extracted_texts = extract_with_ocr(str(input_path))
        else:
            print("   Detected: Text-based PDF (direct extraction)")
            print()
            extracted_texts = extract_text_directly(str(input_path))
            
            # Check if extracted text is garbled (custom font encoding)
            # Sample first few pages to check
            sample_text = "".join(extracted_texts[:min(3, len(extracted_texts))])
            if has_garbled_text(sample_text):
                print()
                print("⚠️  Warning: Extracted text appears garbled (custom font encoding detected)")
                print("   Re-extracting using OCR for better results...")
                print("   (You can set FORCE_OCR = True to skip this check)")
                print()
                extracted_texts = extract_with_ocr(str(input_path))
    
    print()
    
    # Create EPUB
    output_path = Path(OUTPUT_EPUB)
    if not output_path.is_absolute():
        # If relative path, make it relative to script location
        script_dir = Path(__file__).parent
        output_path = script_dir / output_path
    
    create_epub(extracted_texts, str(output_path), BOOK_TITLE, AUTHOR_NAME)
    
    print()
    print("=" * 60)
    print("✅ Conversion complete!")
    print("=" * 60)
    print()
    print("You can now open the EPUB file in:")
    print("  - Apple Books (macOS)")
    print("  - Calibre (recommended for validation)")
    print("  - Any EPUB reader")
    print()


if __name__ == "__main__":
    main()
