# app_search.py   how to use: streamlit run app_search.py

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# import your existing functions
from search_software import (
    QURAN_TEXT,
    table,
    find_verses_multi,
    find_multiple_ayahs,
    SURAH_NAME_TO_NO,
)


def parse_search_terms(value):
    """Split terms entered with either Persian or ASCII commas."""
    return [term.strip() for term in value.replace(",", "،").split("،") if term.strip()]


def add_quran_links(df):
    """
    Adds a clickable Quran.com link for each row
    """
    df = df.copy()

    df["مشاهده آیه"] = df.apply(
        lambda r: f"https://quran.com/{SURAH_NAME_TO_NO[r['سوره']]}/{r['آیه']}",
        axis=1
    )

    return df




st.set_page_config(page_title="جستجوی قرآن", layout="wide")

st.title("🔍 جستجوی هوشمند قرآن")

# -------- Inputs --------
words_input = st.text_input(
    "کلمات جستجو (با ویرگول جدا کنید)",
    placeholder="انسان، ناس"
)

mode = st.selectbox(
    "حالت جستجو",
    ["OR", "AND", "PHRASE"]
)

submit = st.button("جستجو")

# -------- Search --------
if submit and words_input.strip():

    # --- parse words ---
    words = parse_search_terms(words_input)

    # --- search ---
    queries = find_verses_multi(words, QURAN_TEXT, mode=mode)
    results, warnings = find_multiple_ayahs(queries, table)

    # --- warnings ---
    if warnings:
        print("We had warning. Be careful")
        for w in warnings:
            st.warning(w)

    if results:
        df = pd.DataFrame(results)

        # 🔗 ADD CLICKABLE LINKS HERE
        df = add_quran_links(df)

        st.success(f"{len(df)} آیه یافت شد")

        # --- clickable table ---
        st.dataframe(
            df,
            column_config={
                "مشاهده آیه": st.column_config.LinkColumn(
                    label="مشاهده آیه",
                    help="باز کردن آیه در Quran.com",
                    display_text="🔗 مشاهده"
                )
            },
            use_container_width=True
        )

        # --- save outputs ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = Path("outputs") / timestamp
        out_dir.mkdir(parents=True, exist_ok=True)

        df.to_csv(out_dir / "results.csv", index=False, encoding="utf-8-sig")
        df.to_excel(out_dir / "results.xlsx", index=False)

        st.info(f"📁 فایل‌ها ذخیره شدند در: {out_dir}")

    else:
        st.error("هیچ آیه‌ای یافت نشد")


## how to use this: streamlit run app_search.py --server.port 8502
## or streamlit run app_search.py --server.port 8600
