"""Application services shared by the desktop UI and automated tests."""

from __future__ import annotations

import csv
from collections.abc import Mapping, Sequence
from pathlib import Path

from openpyxl import Workbook

from search_software import (
    QURAN_TEXT,
    SURAH_NAME_TO_NO,
    find_multiple_ayahs,
    find_verses_multi,
    table,
)


RESULT_COLUMNS = [
    "سوره",
    "آیه",
    "متن آیه",
    "گروه آیات",
    "موضوع",
    "سال نزول",
    "ترتیب نزول",
]


def parse_search_terms(value: str) -> list[str]:
    """Split search terms entered with Persian or ASCII commas."""
    return [
        term.strip()
        for term in value.replace(",", "،").split("،")
        if term.strip()
    ]


def search_quran(value: str, mode: str) -> tuple[list[dict], list[str]]:
    """Search the Quran and return display-ready results plus mapping warnings."""
    terms = parse_search_terms(value)
    if not terms:
        return [], []

    queries = find_verses_multi(terms, QURAN_TEXT, mode=mode)
    results, warnings = find_multiple_ayahs(queries, table)

    display_rows = []
    for result in results:
        surah_number = SURAH_NAME_TO_NO[result["سوره"]]
        ayah_number = result["آیه"]
        display_rows.append(
            {
                "سوره": result["سوره"],
                "آیه": ayah_number,
                "متن آیه": QURAN_TEXT[surah_number][ayah_number],
                "گروه آیات": result["گروه آیات"],
                "موضوع": result["موضوع"],
                "سال نزول": result["سال نزول"],
                "ترتیب نزول": result["ترتیب نزول"],
            }
        )

    return display_rows, warnings


def export_results(
    results: Sequence[Mapping], destination: str | Path
) -> Path:
    """Export results to CSV or Excel based on the destination extension."""
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)

    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("w", encoding="utf-8-sig", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=RESULT_COLUMNS)
            writer.writeheader()
            writer.writerows(results)
    elif suffix == ".xlsx":
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "نتایج جست‌وجو"
        worksheet.sheet_view.rightToLeft = True
        worksheet.append(RESULT_COLUMNS)
        for result in results:
            worksheet.append([result.get(column, "") for column in RESULT_COLUMNS])
        worksheet.freeze_panes = "A2"
        workbook.save(path)
    else:
        raise ValueError("فرمت خروجی باید CSV یا Excel باشد.")

    return path
