from pathlib import Path
from src.utils.ocr import  ocr_page, pdf_to_images, needs_llm
from src.utils.llm import gemini_extract, cv_to_base64_png
from src.models import shop_receipt, DrivingLicense, resume 

DOC_TYPE_MAP = {
    "receipt": shop_receipt,
    "licence": DrivingLicense,
    "resume": resume,
}

def process_folder(root: Path, out_dir: Path, doc_type: str):
    exts = {".pdf", ".png", ".jpg", ".jpeg", ".tiff"}
    files = [fp for fp in root.rglob("*") if fp.suffix.lower() in exts]
    if not files:
        raise RuntimeError(f"No PDF/image files under {root}")

    out_dir.mkdir(parents=True, exist_ok=True)

    for fp in files:
        models = process_document(fp, doc_type)
        save_outputs(models, (out_dir / fp.stem).as_posix())

def save_outputs(objs, stem: str):
    base = Path(stem).parent
    base.mkdir(parents=True, exist_ok=True)

    for idx, obj in enumerate(objs):
        (base / f"{Path(stem).name}.p{idx}.json").write_text(
            obj.model_dump_json(indent=2)
        )

def process_document(file_path: Path, doc_type: str):
    model_cls = DOC_TYPE_MAP[doc_type]
    pages = (
        pdf_to_images(file_path) if file_path.suffix.lower() == ".pdf" else [file_path]
    )

    out = []
    for img in pages:
        text, conf, img_np = ocr_page(img)

        obj = (
            gemini_extract(
                cv_img_b64=cv_to_base64_png(img_np),
                ocr_text=text,
                pydantic_model=model_cls,
            )
            if needs_llm(conf)
            else gemini_extract(
                cv_img_b64=cv_to_base64_png(img_np),
                ocr_text=text,
                pydantic_model=model_cls,
            )
        )
        out.append(obj)
    return out


if __name__ == "__main__":
    process_folder(Path("dataset"), Path("output"))