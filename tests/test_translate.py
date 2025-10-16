from collabllm_sim.translate.translator import Translator
from collabllm_sim.types import Language


def test_translator_noop_same_language() -> None:
    t = Translator()
    text = "hello"
    assert t.translate(text, Language.EN, Language.EN) == text


def test_translator_tagged_cross_language() -> None:
    t = Translator()
    text = "hello"
    out = t.translate(text, Language.EN, Language.AR)
    assert out.startswith("[en->ar] ")
