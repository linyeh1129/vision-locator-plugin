from importlib.util import find_spec
from vloc.module import VlocModule
from vloc.plugin.__info__ import DetectInfo
if find_spec('vloc.plugin.__selenium__'):
    from vloc.plugin.__slelenium__.__selenium__ import Action as SeleniumAction


class VlocAction:
    if any(cls in str(VlocModule.screenshot_method.__self__) for cls in ['selenium', 'appium']):
        action = SeleniumAction

    @classmethod
    def slide_up(cls, start: float = 0.8, end: float = 0.1, duration=0):
        return cls.action.slide_up(start, end, duration)

    @classmethod
    def slide_down(cls, start: float = 0.1, end: float = 0.8, duration=0):
        return cls.action.slide_down(start, end, duration)

    @classmethod
    def slide_e2e(cls, start: DetectInfo, end: DetectInfo, duration=1000):
        return cls.action.slide_e2e(start, end, duration)
