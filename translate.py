import pytesseract
from PIL import Image
from googletrans import Translator


async def translate_text(image, lg):
    img = Image.open(image)
    ocr_result = pytesseract.image_to_string(img, lang=lg)
    translator = Translator()
    translated = await translator.translate(ocr_result)

    if translated:
        return translated
    else:
        return "Image cannot be processed."
