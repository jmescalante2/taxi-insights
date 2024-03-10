def load(
    table, df, engine, if_exists="append", index=False, schema="public", verbose=True
):
    df.to_sql(table, engine, if_exists=if_exists, index=index, schema=schema)

    if verbose:
        print("Loaded a chunk of size", len(df))
