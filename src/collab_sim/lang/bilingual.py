from __future__ import annotations

from typing import Literal

Language = Literal["en", "ar", "bilingual"]


def say_hello(language: Language) -> str:
    if language == "ar":
        return "مرحبا"
    if language == "bilingual":
        return "Hello / مرحبا"
    return "Hello"


def to_language(text_en: str, text_ar: str, language: Language) -> str:
    if language == "ar":
        return text_ar
    if language == "bilingual":
        return f"{text_en} / {text_ar}"
    return text_en
