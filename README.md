# PDF to EPUB Converter - Arabic Support

A beginner-friendly Python script that converts Arabic PDFs (both scanned and text-based) to EPUB format with proper right-to-left (RTL) text support.

## Features

- ✅ **Automatic Detection**: Automatically detects whether your PDF is scanned (needs OCR) or text-based
- ✅ **OCR Support**: Uses Tesseract OCR to extract text from scanned PDFs with Arabic language support
- ✅ **Direct Text Extraction**: Extracts text directly from text-based PDFs
- ✅ **EPUB3 Format**: Creates EPUB3 files with proper RTL (right-to-left) support for Arabic text
- ✅ **User-Friendly**: Simple configuration at the top of the script
- ✅ **Progress Indicators**: Shows progress during conversion

## Prerequisites

Before using this script, you need to install:

1. **Python 3** (usually pre-installed on macOS)
2. **Tesseract OCR** with Arabic language support
3. **Poppler utilities** (for PDF to image conversion)

## Installation

### Step 1: Install System Dependencies

Open Terminal and run:

```bash
# Install Tesseract OCR with Arabic language support
brew install tesseract tesseract-lang

# Install Poppler utilities (for PDF processing)
brew install poppler
```

**Verify installation:**

```bash
# Check Tesseract
tesseract --version
tesseract --list-langs | grep ara

# Check Poppler
pdftoppm -v
```

You should see Arabic (`ara`) in the list of languages for Tesseract.

### Step 2: Install Python Packages

Navigate to the project folder:

```bash
cd ~/Downloads/pdf-to-epub
```

**Recommended: Using the install script (creates virtual environment)**

```bash
./install.sh
```

This will automatically:
- Create a virtual environment (`venv/` folder)
- Install all required packages
- Keep your system Python clean

**After installation, activate the virtual environment before using the script:**

```bash
source venv/bin/activate
```

**Alternative: Manual installation with virtual environment**

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

**Alternative: Install to user directory (if you prefer not to use venv)**

```bash
pip3 install --user -r requirements.txt
```

This will install:
- `pdf2image` - Converts PDF pages to images
- `pytesseract` - Python wrapper for Tesseract OCR
- `PyPDF2` - Extracts text from text-based PDFs
- `ebooklib` - Creates EPUB files
- `Pillow` - Image processing

> **Note:** On macOS, Python is externally managed, so using a virtual environment is recommended. The install script handles this automatically.

## Usage

### Step 1: Configure the Script

Open `convert_pdf_to_epub.py` in a text editor and edit the configuration section at the top:

```python
# Path to your input PDF file
INPUT_PDF = "/path/to/your/book.pdf"

# Path where the EPUB file will be saved
OUTPUT_EPUB = "test_output/book.epub"

# Book metadata
BOOK_TITLE = "My Arabic Book"
AUTHOR_NAME = "Author Name"
```

**Important:**
- Use the **full path** to your PDF file (e.g., `/Users/yourname/Downloads/mybook.pdf`)
- The output EPUB will be saved in the `test_output/` folder by default
- You can change the output path to anywhere you want

### Step 2: Activate Virtual Environment (if using venv)

If you used the install script or created a virtual environment:

```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Run the Conversion

```bash
python3 convert_pdf_to_epub.py
```

> **Note:** If you installed packages with `--user` flag instead of using a virtual environment, you can skip the activation step.

The script will:
1. Check all dependencies
2. Detect if your PDF is scanned or text-based
3. Extract text (using OCR for scanned PDFs, direct extraction for text-based)
4. Create an EPUB file with proper Arabic RTL support

### Step 4: Verify the EPUB

Open the generated EPUB file in:

- **Apple Books** (macOS default): Double-click the EPUB file
- **Calibre** (recommended): Download from [calibre-ebook.com](https://calibre-ebook.com/)
- Any other EPUB reader

**What to check:**
- ✅ Text displays correctly in Arabic
- ✅ Text direction is right-to-left (RTL)
- ✅ All pages are present
- ✅ Arabic characters render properly

## Example

Here's a complete example:

1. **Place your PDF** in a convenient location, e.g., `~/Downloads/my-arabic-book.pdf`

2. **Edit the script:**
   ```python
   INPUT_PDF = "/Users/yourname/Downloads/my-arabic-book.pdf"
   OUTPUT_EPUB = "test_output/my-arabic-book.epub"
   BOOK_TITLE = "My Arabic Book"
   AUTHOR_NAME = "Author Name"
   ```

3. **Activate virtual environment and run the script:**
   ```bash
   source venv/bin/activate
   python3 convert_pdf_to_epub.py
   ```

4. **Output:**
   ```
   ============================================================
   PDF to EPUB Converter - Arabic Support
   ============================================================
   
   🔍 Checking dependencies...
   ✅ All dependencies found!
   
   📄 Input PDF: /Users/yourname/Downloads/my-arabic-book.pdf
   📚 Output EPUB: test_output/my-arabic-book.epub
   
   🔍 Detecting PDF type...
      Detected: Text-based PDF (direct extraction)
   
   📖 Extracting text from PDF...
      Processing page 10/10...
   ✅ Text extraction complete! Processed 10 pages.
   
   📚 Creating EPUB file: test_output/my-arabic-book.epub
   ✅ EPUB file created successfully!
      Location: test_output/my-arabic-book.epub
      Pages: 10
   
   ============================================================
   ✅ Conversion complete!
   ============================================================
   ```

## Troubleshooting

### Error: "Tesseract OCR is not installed"

**Solution:**
```bash
brew install tesseract tesseract-lang
```

Then verify:
```bash
tesseract --list-langs | grep ara
```

### Error: "Poppler utilities may not be installed"

**Solution:**
```bash
brew install poppler
```

Verify:
```bash
pdftoppm -v
```

### Error: "Missing required packages"

**Solution:**
```bash
# If using virtual environment (recommended)
source venv/bin/activate
pip install -r requirements.txt

# Or use the install script (creates venv automatically)
./install.sh
```

### Error: "externally-managed-environment"

This error occurs on macOS when trying to install packages globally.

**Solution - Use virtual environment (recommended):**
```bash
# The install.sh script handles this automatically
./install.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Alternative - Install to user directory:**
```bash
pip3 install --user -r requirements.txt
```

**Note:** If you use `--user`, you don't need to activate a virtual environment, but you'll need to use `python3 -m pip` if you encounter path issues.

### Error: "Input PDF not found"

**Solution:**
- Make sure you've edited `INPUT_PDF` in the script
- Use the **full path** to your PDF file
- Check that the file exists: `ls -la /path/to/your/file.pdf`

### OCR is very slow

**This is normal!** OCR processing can take a long time, especially for:
- Large PDFs (many pages)
- High-resolution scans
- Complex layouts

**Tips:**
- Start with a small PDF (1-5 pages) to test
- The script shows progress for each page
- Be patient - quality OCR takes time

### Arabic text doesn't display correctly

**Possible causes:**
1. **Tesseract Arabic language not installed**: Run `brew install tesseract-lang` and verify with `tesseract --list-langs | grep ara`
2. **EPUB reader doesn't support RTL**: Try opening in Calibre or Apple Books
3. **Font issues**: The EPUB uses system fonts - try a different reader

### The EPUB file is empty or has no content

**Possible causes:**
1. **Scanned PDF with poor quality**: OCR may not extract text well from low-quality scans
2. **PDF is password-protected**: The script doesn't handle encrypted PDFs
3. **OCR failed**: Check the error messages in the terminal

**Solution:**
- Try with a text-based PDF first to verify the script works
- Check the PDF quality if using OCR
- Make sure the PDF is not password-protected

## Project Structure

```
pdf-to-epub/
├── convert_pdf_to_epub.py    # Main conversion script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── install.sh                # Installation helper script
├── .gitignore                # Git ignore file
├── venv/                     # Virtual environment (created by install.sh)
└── test_output/             # Output folder for EPUB files
```

## How It Works

1. **PDF Type Detection**: The script checks if the PDF contains extractable text or is image-based (scanned)

2. **Text Extraction**:
   - **Scanned PDFs**: Converts each page to an image, then uses Tesseract OCR with Arabic language support to extract text
   - **Text-based PDFs**: Directly extracts text using PyPDF2

3. **EPUB Creation**: Formats the extracted text into EPUB3 format with:
   - Proper RTL (right-to-left) HTML structure
   - Arabic language metadata
   - One chapter per page
   - Proper CSS styling for Arabic text

## Tips for Best Results

1. **Start Small**: Test with a 1-5 page PDF first
2. **Text-based PDFs**: Work faster and more accurately than scanned PDFs
3. **Quality Matters**: Higher quality scans = better OCR results
4. **Be Patient**: OCR can take several minutes for large PDFs
5. **Verify Output**: Always check the EPUB in a reader to ensure quality

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Try with a simple text-based PDF first
4. Check the terminal output for specific error messages

## License

This script is provided as-is for personal use.
