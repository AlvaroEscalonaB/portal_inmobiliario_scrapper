from pathlib import Path

import pandas as pd

MIN_BEDROOMS_REQUIRED = 2
UF_TO_CLP = 38_914
TOP_PROPERTIES_N = 5


def run_summary_analysis(path: Path, min_bedrooms: int = MIN_BEDROOMS_REQUIRED) -> pd.DataFrame:
    df_properties: pd.DataFrame = pd.read_json(path_or_buf=path)  # type: ignore
    df_properties = df_properties[df_properties["bedrooms"] >= min_bedrooms]
    df_properties.loc[df_properties["currency"] == "UF", "price"] = df_properties["price"] * UF_TO_CLP

    df_top_properties = (
        df_properties.sort_values(by="price", ascending=True)  # type:ignore
        .head(n=TOP_PROPERTIES_N)
        .reset_index()
    )
    return df_top_properties


if __name__ == "__main__":
    from pathlib import Path

    df_top_properties = run_summary_analysis(Path.cwd() / "output.json")
    for i, row in df_top_properties.iterrows():  # type:ignore
        print("-" * 70)
        print(f"TOP {i}")
        print(f"{row['price']}")
        print(f"{row['url']}")
