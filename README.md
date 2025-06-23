# Document Data Extractor

A hybrid OCR-LLM pipeline that extracts structured data from documents using Tesseract OCR and Google's Gemini Flash LLM. The system processes images through local OCR first, then leverages AI with Pydantic schema validation to ensure reliable JSON output every time.

## Overview

The system runs images through **Tesseract** for fast, local OCR then sends to **Gemini Flash** with a prompt that includes the OCR snippet and the **Pydantic-derived JSON schema**. Gemini must return JSON which is validated with Pydantic, retrying up to three times on failure - resulting in cheap offline OCR for clean scans, LLM processing and schema-guaranteed JSON every time.

## Supported Document Types

- **Receipts** - Extracts merchant info, items, prices, payment method
- **Driver's Licenses** - Extracts name, DOB, license number, state, expiry
- **Resumes** - Extracts contact info, skills, education, work experience

## Features

- 🔍 **Tesseract OCR** for local text extraction
- 🤖 **Gemini Flash integration** for AI-powered data extraction
- 📋 **Pydantic schema validation** ensures consistent JSON output
- 🔄 **Automatic retry** (up to 3 attempts) on validation failures
- 📁 **Batch processing** for folders of documents
- 🖼️ **Multi-format support** (PDF, PNG, JPG, JPEG, TIFF)

## Prerequisites

- Python 3.13+
- Google AI API key (for Gemini Flash)
- Tesseract OCR installed on your system

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/pushkar1713/ocr-llm-py.git
   cd firstwork-assignment
   ```

2. **Install dependencies:**

   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory:

   ```bash
   GEMINI_API_KEY=your_google_ai_api_key_here
   ```

## Usage

### Command Line Interface

Process a single document:

```bash
python main.py run --type receipt --path /path/to/document.pdf
```

Process a folder of documents:

```bash
python main.py run --type licence --path /path/to/folder
```

### Interactive Mode

Run without arguments for interactive prompts:

```bash
python main.py run
```

The system will prompt you for:

- Document type (receipt, licence, resume)
- Path to file or folder
- Output directory (optional, defaults to `./output`)

### Examples

**Process a receipt:**

```bash
python main.py run -t receipt -p shop_receipts/receipt_001.jpg
```

**Process driver's licenses in bulk:**

```bash
python main.py run -t licence -p Drivers_license/ -o processed_licenses/
```

**Process resume PDFs:**

```bash
python main.py run -t resume -p Resume/candidate_resume.pdf
```

## Output

The system generates JSON files in the specified output directory:

- Format: `{filename}.p{page_number}.json`
- Each page of a document gets its own JSON file
- Example: `document.pdf` → `document.p0.json`, `document.p1.json`

### Sample Output

**Driver's License:**

```json
{
  "name": "Aaron Collins",
  "dob": "1956-10-09",
  "license_number": "MKWMJO89",
  "issuing_state": "Ireland",
  "expiry_date": "1967-04-14"
}
```

## Project Structure

```
firstwork-assignment/
├── main.py                 # CLI entry point
├── src/
│   ├── config.py          # Environment configuration
│   ├── models.py          # Pydantic data models
│   ├── pipeline.py        # Main processing pipeline
│   └── utils/
│       ├── ocr.py         # Tesseract OCR functions
│       └── llm.py         # Gemini LLM integration
├── output/                # Generated JSON files
├── pyproject.toml        # Project dependencies
└── README.md
```

## How It Works

1. **Document Input** - Accepts PDF or image files
2. **OCR Processing** - Tesseract extracts text with confidence scoring
3. **LLM Enhancement** - If OCR confidence is low, Gemini Flash processes both image and OCR text
4. **Schema Validation** - Pydantic validates output against predefined models
5. **Retry Logic** - Up to 3 attempts for failed validations
6. **JSON Output** - Structured data saved as JSON files

## Configuration

### OCR Settings

- DPI: 300 (configurable in `pdf_to_images()`)
- Tesseract config: English language, PSM 6

### LLM Settings

- Model: `gemini-2.5-flash`
- Response format: JSON only
- Max retries: 3 attempts

## Error Handling

- **Validation errors** trigger retry with error context
- **API errors** are logged with detailed messages
- **File errors** show clear path and permission issues

## Dependencies

- `google-generativeai` - Gemini AI integration
- `pytesseract` - Tesseract OCR wrapper
- `pydantic` - Data validation and serialization
- `opencv-python-headless` - Image processing
- `pymupdf` - PDF processing
- `typer` - CLI framework
- `rich` - Terminal formatting
