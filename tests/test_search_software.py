from io import StringIO
from unittest.mock import patch

import pytest

from search_software import (
    find_multiple_ayahs,
    find_verses_multi,
    load_quran_txt,
    normalize_arabic,
    table,
)


SAMPLE_QURAN = {
    1: {
        1: "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ",
        2: "فَصَلِّ لِرَبِّكَ وَانْحَرْ",
        3: "إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ",
    }
}


def test_normalize_arabic_unifies_letters_and_removes_diacritics():
    assert normalize_arabic("إِنَّا كَرِيمٌ") == "انا کریم"


@pytest.mark.parametrize(
    ("mode", "words", "expected"),
    [
        ("OR", ["کوثر", "شانئک"], [(1, 1), (1, 3)]),
        ("AND", ["فصل", "ربک"], [(1, 2)]),
        ("PHRASE", ["هو", "الابتر"], [(1, 3)]),
    ],
)
def test_find_verses_multi_modes(mode, words, expected):
    assert find_verses_multi(words, SAMPLE_QURAN, mode) == expected


@pytest.mark.parametrize("mode", ["OR", "AND", "PHRASE"])
def test_empty_terms_never_match_every_verse(mode):
    assert find_verses_multi(["", "  "], SAMPLE_QURAN, mode) == []


def test_invalid_mode_is_rejected_even_for_empty_quran():
    with pytest.raises(ValueError):
        find_verses_multi(["کوثر"], {}, "INVALID")


def test_find_multiple_ayahs_maps_metadata_and_warns_for_unmapped_ayah():
    metadata = [{
        "surah": "کوثر",
        "ranges": [(1, 2)],
        "topic": "نمونه",
        "year": "سال نمونه",
        "revelation_order": 5,
    }]

    results, warnings = find_multiple_ayahs([(108, 1), (108, 3)], metadata)

    assert results[0]["سوره"] == "کوثر"
    assert results[0]["گروه آیات"] == "1 تا 2"
    assert len(warnings) == 1
    assert "آیه 3" in warnings[0]


def test_al_masad_uses_the_canonical_surah_name_in_metadata():
    results, warnings = find_multiple_ayahs([(111, 1)], table)

    assert results[0]["سوره"] == "مسد"
    assert warnings == []


def test_load_quran_txt_preserves_delimiters_in_verse_text():
    with patch("builtins.open", return_value=StringIO("1|1|part one|part two\n")):
        assert load_quran_txt("unused.txt") == {1: {1: "part one|part two"}}
