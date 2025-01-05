import functools
import os
from supabase import create_client, Client

"""
NOTE:
Not sure if creating a client on each use is efficient
My reference point is SQLAlchemy, where you create a single engine / client for the server's entire lifetime
and you spin up connections / sessions for each use

But given the serverless nature of my frontned, I think better safe than sorry to do it this way
"""


def get_db_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


def use_db_client(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db_client = kwargs.get("db_client", None)
        if not db_client:
            db_client = get_db_client()
        return func(db_client=db_client, *args, **kwargs)

    return wrapper
