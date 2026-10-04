import os
import pytesseract
from PIL import Image


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

# Windows:
# Use the locally installed Tesseract path.

WINDOWS_TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


if os.path.exists(WINDOWS_TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = WINDOWS_TESSERACT_PATH


# ============================================================
# OCR FUNCTION
# ============================================================

def extract_text(image):
    """
    Extract text from an uploaded image using Tesseract OCR.
    Works locally and on supported deployment environments.
    """

    try:
        text = pytesseract.image_to_string(image)
        return text.strip()

    except Exception as e:
        return f"OCR Error: {e}"