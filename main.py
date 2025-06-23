from src.utils.ocr import ocr_page
from pathlib import Path
from src.utils.llm import gemini_extract
from src.utils.llm import cv_to_base64_png
from src.models import DrivingLicense, shop_receipt

path = Path("/Users/pushkar1713/Projects/firstwork-assignment/Drivers_license/generated_license_1071.png")

ans = ocr_page(path)
print(ans[0])
print("confidence", ans[1])

cv_img_b64 = cv_to_base64_png(ans[2])

new_ans = gemini_extract(
    cv_img_b64=cv_img_b64,
    ocr_text=ans[0],
    pydantic_model=DrivingLicense,
)

print(new_ans.model_dump_json(indent=2))

shop_ans = ocr_page(Path("/Users/pushkar1713/Projects/firstwork-assignment/shop_receipts/10.jpg"))
print(shop_ans[0])
print("confidence", shop_ans[1])

shop_cv_img_b64 = cv_to_base64_png(shop_ans[2])

shop_new_ans = gemini_extract(
    cv_img_b64=shop_cv_img_b64,
    ocr_text=shop_ans[0],
    pydantic_model=shop_receipt,
)
print(shop_new_ans.model_dump_json(indent=2))


def main():
    print("Hello from firstwork-assignment!")


if __name__ == "__main__":
    main()
