"""Native desktop interface for Quran search.

Run from source with::

    python app_search.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from app_core import RESULT_COLUMNS, export_results, parse_search_terms, search_quran


APP_TITLE = "جست‌وجوی هوشمند قرآن"


class ResultsTableModel(QAbstractTableModel):
    """A sortable Qt table model backed by result dictionaries."""

    def __init__(self, data: list[dict] | None = None) -> None:
        super().__init__()
        self._data = list(data or [])

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(RESULT_COLUMNS)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None

        column = RESULT_COLUMNS[index.column()]
        value = self._data[index.row()].get(column, "")
        if role in (Qt.DisplayRole, Qt.ToolTipRole):
            return str(value)
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignRight | Qt.AlignVCenter)
        if role == Qt.BackgroundRole and index.row() % 2:
            return QColor("#f7f9fc")
        return None

    def headerData(  # noqa: N802
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.DisplayRole,
    ):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return RESULT_COLUMNS[section]
            return str(section + 1)
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignCenter)
        return None

    def sort(self, column: int, order: Qt.SortOrder = Qt.AscendingOrder) -> None:
        if not self._data:
            return
        self.layoutAboutToBeChanged.emit()
        column_name = RESULT_COLUMNS[column]
        self._data.sort(
            key=lambda row: row.get(column_name, ""),
            reverse=order == Qt.DescendingOrder,
        )
        self.layoutChanged.emit()

    def replace_data(self, data: list[dict]) -> None:
        self.beginResetModel()
        self._data = list(data)
        self.endResetModel()

    def row(self, row_number: int) -> dict | None:
        if 0 <= row_number < len(self._data):
            return self._data[row_number]
        return None


class SearchWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[dict] = []
        self.model = ResultsTableModel(self.results)

        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(980, 680)
        self.resize(1280, 820)
        self.setLayoutDirection(Qt.RightToLeft)

        self._build_interface()
        self._apply_style()
        self.search_input.setFocus()

    def _build_interface(self) -> None:
        root = QWidget(self)
        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(22, 18, 22, 18)
        main_layout.setSpacing(14)
        self.setCentralWidget(root)

        title = QLabel("جست‌وجوی هوشمند قرآن و ترتیب نزول آیات")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel(
            "جست‌وجوی واژه یا عبارت در متن قرآن؛ کاملاً آفلاین و بدون مرورگر"
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        search_panel = QFrame()
        search_panel.setObjectName("searchPanel")
        search_layout = QGridLayout(search_panel)
        search_layout.setContentsMargins(16, 16, 16, 16)
        search_layout.setHorizontalSpacing(12)
        search_layout.setVerticalSpacing(8)

        search_layout.addWidget(QLabel("کلمات جست‌وجو:"), 0, 0)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("برای نمونه: انسان، ناس")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_input, 1, 0)

        search_layout.addWidget(QLabel("حالت جست‌وجو:"), 0, 1)
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("حداقل یکی از واژه‌ها (OR)", "OR")
        self.mode_combo.addItem("همهٔ واژه‌ها (AND)", "AND")
        self.mode_combo.addItem("عبارت دقیق (PHRASE)", "PHRASE")
        search_layout.addWidget(self.mode_combo, 1, 1)

        self.search_button = QPushButton("جست‌وجو")
        self.search_button.setObjectName("primaryButton")
        self.search_button.clicked.connect(self.perform_search)
        search_layout.addWidget(self.search_button, 1, 2)

        search_layout.setColumnStretch(0, 5)
        search_layout.setColumnStretch(1, 2)
        main_layout.addWidget(search_panel)

        action_layout = QHBoxLayout()
        self.result_count = QLabel("هنوز جست‌وجویی انجام نشده است.")
        self.result_count.setObjectName("resultCount")
        action_layout.addWidget(self.result_count, 1)

        self.export_excel_button = QPushButton("ذخیره Excel")
        self.export_excel_button.clicked.connect(self.export_excel)
        self.export_excel_button.setEnabled(False)
        action_layout.addWidget(self.export_excel_button)

        self.export_csv_button = QPushButton("ذخیره CSV")
        self.export_csv_button.clicked.connect(self.export_csv)
        self.export_csv_button.setEnabled(False)
        action_layout.addWidget(self.export_csv_button)
        main_layout.addLayout(action_layout)

        splitter = QSplitter(Qt.Vertical)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setAlternatingRowColors(False)
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.setWordWrap(True)
        self.table_view.verticalHeader().setDefaultSectionSize(54)
        self.table_view.horizontalHeader().setStretchLastSection(False)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table_view.selectionModel().currentRowChanged.connect(
            self.show_selected_verse
        )
        splitter.addWidget(self.table_view)

        detail_group = QGroupBox("متن کامل آیه")
        detail_layout = QVBoxLayout(detail_group)
        self.verse_detail = QPlainTextEdit()
        self.verse_detail.setReadOnly(True)
        self.verse_detail.setPlaceholderText(
            "برای نمایش متن آیه، یکی از نتیجه‌ها را انتخاب کنید."
        )
        detail_layout.addWidget(self.verse_detail)
        splitter.addWidget(detail_group)
        splitter.setSizes([560, 150])
        main_layout.addWidget(splitter, 1)

        self.warning_label = QLabel()
        self.warning_label.setObjectName("warningLabel")
        self.warning_label.setWordWrap(True)
        self.warning_label.hide()
        main_layout.addWidget(self.warning_label)

        self.statusBar().showMessage("آماده")

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background: #f4f6f8;
                color: #17212b;
                font-family: "Segoe UI", "Tahoma";
                font-size: 11pt;
            }
            QLabel#title {
                color: #173f35;
                font-size: 20pt;
                font-weight: 700;
            }
            QLabel#subtitle {
                color: #5d6b66;
                font-size: 10.5pt;
            }
            QFrame#searchPanel, QGroupBox {
                background: white;
                border: 1px solid #dce3e0;
                border-radius: 8px;
            }
            QGroupBox {
                margin-top: 10px;
                padding-top: 9px;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                right: 12px;
                padding: 0 5px;
            }
            QLineEdit, QComboBox, QPlainTextEdit {
                background: white;
                border: 1px solid #b8c7c1;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #2b7864;
            }
            QLineEdit:focus, QComboBox:focus, QPlainTextEdit:focus {
                border: 2px solid #2b7864;
            }
            QPushButton {
                background: #e7eeeb;
                border: 1px solid #b8c7c1;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: 600;
            }
            QPushButton:hover { background: #dbe7e2; }
            QPushButton:pressed { background: #cadbd4; }
            QPushButton:disabled { color: #929b98; background: #edf0ef; }
            QPushButton#primaryButton {
                background: #246b58;
                color: white;
                border-color: #246b58;
                min-width: 95px;
            }
            QPushButton#primaryButton:hover { background: #1d5a4a; }
            QLabel#resultCount { color: #315c50; font-weight: 600; }
            QLabel#warningLabel {
                background: #fff4cf;
                border: 1px solid #e2c86d;
                border-radius: 5px;
                color: #665113;
                padding: 8px;
            }
            QTableView {
                background: white;
                alternate-background-color: #f7f9fc;
                border: 1px solid #dce3e0;
                border-radius: 6px;
                gridline-color: #e3e8e6;
                selection-background-color: #cfe5dd;
                selection-color: #132d25;
            }
            QHeaderView::section {
                background: #e4ece9;
                border: none;
                border-left: 1px solid #cdd8d4;
                padding: 8px;
                font-weight: 700;
            }
            """
        )

    def perform_search(self) -> None:
        terms = parse_search_terms(self.search_input.text())
        if not terms:
            QMessageBox.information(
                self,
                APP_TITLE,
                "لطفاً دست‌کم یک واژه یا عبارت برای جست‌وجو وارد کنید.",
            )
            self.search_input.setFocus()
            return

        self.search_button.setEnabled(False)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.statusBar().showMessage("در حال جست‌وجو…")

        try:
            mode = self.mode_combo.currentData()
            results, warnings = search_quran(self.search_input.text(), mode)
            self.results = results
            self.model.replace_data(results)
            self.verse_detail.clear()

            has_results = bool(results)
            self.export_excel_button.setEnabled(has_results)
            self.export_csv_button.setEnabled(has_results)

            if has_results:
                self.result_count.setText(f"{len(results):,} آیه یافت شد.")
                self.statusBar().showMessage("جست‌وجو با موفقیت انجام شد.", 5000)
                self._resize_result_columns()
                self.table_view.selectRow(0)
            else:
                self.result_count.setText("هیچ آیه‌ای یافت نشد.")
                self.statusBar().showMessage("نتیجه‌ای یافت نشد.", 5000)

            self._show_warnings(warnings)
        except Exception as exc:  # keep GUI errors visible in a windowed executable
            QMessageBox.critical(
                self,
                "خطا",
                f"هنگام جست‌وجو خطایی رخ داد:\n{exc}",
            )
            self.statusBar().showMessage("خطا در جست‌وجو", 5000)
        finally:
            QApplication.restoreOverrideCursor()
            self.search_button.setEnabled(True)

    def _resize_result_columns(self) -> None:
        widths = {
            "سوره": 105,
            "آیه": 65,
            "متن آیه": 390,
            "گروه آیات": 115,
            "موضوع": 245,
            "سال نزول": 115,
            "ترتیب نزول": 110,
        }
        for index, column in enumerate(RESULT_COLUMNS):
            self.table_view.setColumnWidth(index, widths.get(column, 130))

    def _show_warnings(self, warnings: list[str]) -> None:
        if warnings:
            preview = warnings[:3]
            extra = len(warnings) - len(preview)
            message = "\n".join(preview)
            if extra:
                message += f"\n… و {extra} هشدار دیگر"
            self.warning_label.setText(message)
            self.warning_label.show()
        else:
            self.warning_label.clear()
            self.warning_label.hide()

    def show_selected_verse(self, current: QModelIndex) -> None:
        row = self.model.row(current.row())
        if row is None:
            self.verse_detail.clear()
            return
        self.verse_detail.setPlainText(
            f"سوره {row['سوره']}، آیه {row['آیه']}\n\n{row['متن آیه']}"
        )

    def export_excel(self) -> None:
        self._export("Excel (*.xlsx)", ".xlsx")

    def export_csv(self) -> None:
        self._export("CSV (*.csv)", ".csv")

    def _export(self, file_filter: str, extension: str) -> None:
        if not self.results:
            return

        initial_name = str(Path.home() / f"quran_search_results{extension}")
        destination, _ = QFileDialog.getSaveFileName(
            self,
            "ذخیره نتایج",
            initial_name,
            file_filter,
        )
        if not destination:
            return
        if not destination.lower().endswith(extension):
            destination += extension

        try:
            saved_path = export_results(self.results, destination)
            self.statusBar().showMessage(
                f"نتایج در {saved_path} ذخیره شد.", 8000
            )
            QMessageBox.information(
                self,
                "ذخیره نتایج",
                f"فایل با موفقیت ذخیره شد:\n{saved_path}",
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "خطا در ذخیره",
                f"ذخیره فایل انجام نشد:\n{exc}",
            )


def smoke_test() -> int:
    """Exercise bundled data and search logic without opening a window."""
    results, _ = search_quran("انسان", "OR")
    return 0 if results and "متن آیه" in results[0] else 1


def main() -> int:
    if "--smoke-test" in sys.argv:
        return smoke_test()

    gui_smoke_test = "--gui-smoke-test" in sys.argv
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    app.setOrganizationName("Quran Sessions Bahrampour")
    app.setLayoutDirection(Qt.RightToLeft)
    app.setStyle("Fusion")

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = SearchWindow()
    if gui_smoke_test:
        window.search_input.setText("انسان")
        window.perform_search()
        app.processEvents()
        return 0 if window.results and window.table_view.model().rowCount() else 1

    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
