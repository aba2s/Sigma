from sqlalchemy.types import Integer
from sqlalchemy.types import Float
from sqlalchemy.types import String
from sqlalchemy.types import Date
from sqlalchemy import create_engine
from django.conf import settings

cols = [
    "date",
    "dsp",
    "advertiser",
    "insertion_order",
    "strategy",
    "creative",
    "budget",
    "impressions",
    "clicks",
    "conversions",
    "post_clicks_conversions",
    "post_views_conversions",
]
renamed_cols_dict = {
    "date": "date",
    "dsp": "dsp",
    "advertiser": "advertiser",
    "insertion_order": "insertion_order",
    "strategy": "strategy",
    "creative": "creative",
    "budget": "budget",
    "impressions": "impressions",
    "clicks": "clicks",
    "conversions": "conversions",
    "cv pc": "post_clicks_conversions",
    "cv pv": "post_views_conversions",
}
dtype = {
    "date": Date,
    "dsp": String,
    "advertiser": String,
    "insertion_order": String,
    "strategy": String,
    "creative": String,
    "budget": Float,
    "impressions": Integer,
    "clicks": Integer,
    "conversions": Integer,
    "post_clicks_conversions": Integer,
    "post_views_conversions": Integer,
}


# DEFINE THE DATABASE CREDENTIALS
user = settings.DATABASES["default"]["USER"]
password = settings.DATABASES["default"]["PASSWORD"]
database_name = settings.DATABASES["default"]["NAME"]
host = settings.DATABASES["default"]["HOST"]
port = settings.DATABASES["default"]["PORT"]


# PYTHON FUNCTION TO CONNECT TO THE POSTGRESQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    database_url = (
        "postgresql://{user}:{password}@{host}:{port}/{database_name}".format(
            user=user,
            password=password,
            host=host,
            port=port,
            database_name=database_name,
        )
    )
    engine = create_engine(database_url, echo=False)
    return engine
