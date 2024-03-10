from sqlalchemy import create_engine


def get_engine(**kwargs):
    db_uri = f"{kwargs["protocol"]}://{kwargs["username"]}:{kwargs["password"]}@{kwargs["host"]}:{kwargs["port"]}"
    if "database" in kwargs:
        db_uri = f"{db_uri}/{kwargs["database"]}"
    return create_engine(db_uri)

