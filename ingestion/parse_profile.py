import pandas as pd


def parse_profile(
    profile_path
):

    df = pd.read_csv(
        profile_path
    )

    if df.empty:
        return {}

    return (
        df.iloc[0]
        .to_dict()
    )