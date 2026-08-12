import csv

from openpyxl import load_workbook

from app_core import export_results, parse_search_terms, search_quran


def test_parse_search_terms_accepts_persian_and_ascii_commas():
    assert parse_search_terms(" انسان، ناس, بشر ") == ["انسان", "ناس", "بشر"]


def test_parse_search_terms_discards_empty_values():
    assert parse_search_terms(" ، ,  ") == []


def test_search_results_include_verse_text_without_external_links():
    results, _ = search_quran("انسان", "OR")

    assert results
    assert "متن آیه" in results[0]
    assert "مشاهده آیه" not in results[0]


def test_export_results_supports_csv_and_excel(tmp_path):
    results = [{"سوره": "کوثر", "آیه": 2, "متن آیه": "فصل لربک"}]

    csv_path = export_results(results, tmp_path / "results.csv")
    excel_path = export_results(results, tmp_path / "results.xlsx")

    assert csv_path.exists()
    assert excel_path.exists()
    with csv_path.open(encoding="utf-8-sig") as input_file:
        csv_row = next(csv.DictReader(input_file))
    excel_sheet = load_workbook(excel_path).active

    assert csv_row["سوره"] == "کوثر"
    assert excel_sheet["B2"].value == 2
