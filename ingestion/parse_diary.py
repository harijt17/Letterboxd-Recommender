import pandas as pd


def parse_diary(
    diary_path
):

    df = pd.read_csv(
        diary_path
    )

    if df.empty:
        return []

    df = df.where(
        pd.notnull(df),
        None
    )

    return df.to_dict(
        orient="records"
    )