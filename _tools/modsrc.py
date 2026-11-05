MODULE_V1 = r'''
"""Reusable helpers for the variant-abundance analysis."""

BINS = ["bin1_count", "bin2_count", "bin3_count", "bin4_count"]


def add_scores(df, weights=(1, 2, 3, 4), min_reads=0):
    """Add total_reads and a weighted-average bin score.

    score = sum(weight_i * count_i) / total_reads. Rows with fewer than
    `min_reads` total reads get score = NaN. Returns a new DataFrame.
    """
    out = df.copy()
    out["total_reads"] = out[BINS].sum(axis=1)
    out["score"] = (out[BINS] * list(weights)).sum(axis=1) / out["total_reads"]
    out.loc[out["total_reads"] < min_reads, "score"] = float("nan")
    return out
'''

MODULE_ADD_PARSE = r'''
def parse_hgvs(df, column="hgvs_pro"):
    """Split names like 'p.Asn12Ile' into ref, position and alt columns.

    ref = 'Asn', position = 12 (nullable integer), alt = 'Ile'.
    Synonymous names like 'p.Asn12=' get alt = '='. Anything that does not
    match (for example the wild-type row '_wt') gets missing values.
    """
    pattern = r"^p\.(?P<ref>[A-Za-z]{3})(?P<position>\d+)(?P<alt>[A-Za-z]{3}|=)$"
    parts = df[column].str.extract(pattern)
    out = df.copy()
    out["ref"] = parts["ref"]
    out["position"] = pd.to_numeric(parts["position"]).astype("Int64")
    out["alt"] = parts["alt"]
    return out
'''

MODULE_ADD_REGION = r'''
def label_regions(df, regions, position_column="position"):
    """Add a 'region' column from a table with region, start and end columns.

    Positions outside every region are labelled 'other'; rows without a
    position are labelled 'no_position'.
    """
    def find(position):
        if pd.isna(position):
            return "no_position"
        for r in regions.itertuples():
            if r.start <= position <= r.end:
                return r.region
        return "other"

    out = df.copy()
    out["region"] = out[position_column].map(find)
    return out
'''

MODULE_FULL = r'''
"""Reusable helpers for the variant-abundance analysis."""
import pandas as pd

BINS = ["bin1_count", "bin2_count", "bin3_count", "bin4_count"]


def add_scores(df, weights=(1, 2, 3, 4), min_reads=0):
    """Add total_reads and a weighted-average bin score.

    score = sum(weight_i * count_i) / total_reads. Rows with fewer than
    `min_reads` total reads get score = NaN. Returns a new DataFrame.
    """
    out = df.copy()
    out["total_reads"] = out[BINS].sum(axis=1)
    out["score"] = (out[BINS] * list(weights)).sum(axis=1) / out["total_reads"]
    out.loc[out["total_reads"] < min_reads, "score"] = float("nan")
    return out


def parse_hgvs(df, column="hgvs_pro"):
    """Split names like 'p.Asn12Ile' into ref, position and alt columns.

    ref = 'Asn', position = 12 (nullable integer), alt = 'Ile'.
    Synonymous names like 'p.Asn12=' get alt = '='. Anything that does not
    match (for example the wild-type row '_wt') gets missing values.
    """
    pattern = r"^p\.(?P<ref>[A-Za-z]{3})(?P<position>\d+)(?P<alt>[A-Za-z]{3}|=)$"
    parts = df[column].str.extract(pattern)
    out = df.copy()
    out["ref"] = parts["ref"]
    out["position"] = pd.to_numeric(parts["position"]).astype("Int64")
    out["alt"] = parts["alt"]
    return out


def label_regions(df, regions, position_column="position"):
    """Add a 'region' column from a table with region, start and end columns.

    Positions outside every region are labelled 'other'; rows without a
    position are labelled 'no_position'.
    """
    def find(position):
        if pd.isna(position):
            return "no_position"
        for r in regions.itertuples():
            if r.start <= position <= r.end:
                return r.region
        return "other"

    out = df.copy()
    out["region"] = out[position_column].map(find)
    return out
'''
