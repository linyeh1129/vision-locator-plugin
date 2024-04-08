from importlib.util import find_spec
import re
import cv2
import pytesseract
from vloc.config.catalog import VL
from vloc.exception.catalog import OcrException
if PLUGIN_SELENIUM := find_spec('vloc_plugin_selenium'):
    from vloc_plugin_selenium.__info__ import Action as SeleniumAction


class DetectInfo:
    x: int = None
    y: int = None
    label: str = None
    conf: float = None
    crop: str = None
    ocr: str = None

    def __init__(self,
                 x: int,
                 y: int,
                 label: str,
                 conf: float,
                 crop: str,
                 ocr=None):

        if any(x in ['selenium', 'appium'] for x in str(VL.screenshot_method.__self__)):
            action = SeleniumAction(x, y, VL.screenshot_method.__self__)

            self.click = action.click
            self.input = action.input

    def click(self):
        ...

    def input(self, value: str):
        ...

    def text(self,
             search: re.Pattern = None,
             remove: re.Pattern = None,
             segment: bool = True) -> str:

        img = cv2.imread(self.crop)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        config = '--psm 4' if segment else '--psm 7'

        txt = str(pytesseract.image_to_string(img, config=config)).replace('\n', '')

        if search:
            txt = re.search(search, txt)
            if not txt:
                raise OcrException(f'text search pattern not contains:{search}')
            txt = txt.group(0)

        txt = re.sub(remove, '', txt).strip() if remove else txt
        return txt



