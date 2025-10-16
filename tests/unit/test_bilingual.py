from __future__ import annotations

from collab_sim.lang.bilingual import say_hello, to_language


def test_say_hello_variants():
    assert say_hello("en") == "Hello"
    assert say_hello("ar") == "مرحبا"
    assert say_hello("bilingual").startswith("Hello")


def test_to_language_switch():
    assert to_language("A", "ب", "en") == "A"
    assert to_language("A", "ب", "ar") == "ب"
    assert to_language("A", "ب", "bilingual") == "A / ب"
