from __future__ import annotations
from pathlib import Path
from typing import Tuple

import cv2
import fitz
import numpy as np
import pytesseract
from rich import print

def pdf_to_images(pdf_path:Path, dpi:int=300) -> list[Path]:
    doc = fitz.open(pdf_path)

    outpaths : list[Path] = []

    for page_index, page in enumerate(doc):
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        outpath = pdf_path.parent / f"{pdf_path.stem}_{page_index}.png"
        pix.save(outpath)
        outpaths.append(outpath)

    return outpaths

def run_tesseract(cv_img: np.ndarray) -> Tuple[str, float]:

    tess_config = "-l eng --oem 3 --psm 6"
    df = pytesseract.image_to_data(
        cv_img, output_type=pytesseract.Output.DATAFRAME, config=tess_config
    )

    text = " ".join(df.text.dropna())
    confidence = float(df.conf.mean())

    return text, confidence

def light_preprocess(img_path: Path) -> np.ndarray:
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.medianBlur(gray, 3)
    return denoised

def needs_llm(conf: float) -> bool:
    return conf < 60

def ocr_page(page_path: Path) -> tuple[str, float, np.ndarray]:
    img_np = light_preprocess(page_path)
    text, conf = run_tesseract(img_np)
    return text, conf, img_np

