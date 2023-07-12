from sqlalchemy.types import Integer
from sqlalchemy.types import Float
from sqlalchemy.types import String
from sqlalchemy.types import Date
from datetime import datetime
import pandas as pd
from sigma_app.models import *
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
# from django.db import IntegrityError # django ORM

# DEFINE THE DATABASE CREDENTIALS
user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
database_name = settings.DATABASES['default']['NAME']
host = settings.DATABASES['default']['HOST']
port = settings.DATABASES['default']['PORT']

# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
    database_url = "postgresql://{user}:{password}@{host}:{port}/{database_name}".format(
        user=user,
        password=password,
        host = 'localhost',
        port = 5432,
        database_name=database_name,
    )
    engine = create_engine(database_url, echo=False)
    return engine

try:    
    # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
    engine = get_connection()
    # print("Connection to the {host} for user {user} created successfully.")
except Exception as e:
    print("Connection could not be made due to the following error: \n", e)

def upload_io_real_spents(request):
    '''
    Insertion orders real spents
    '''
    file_path = '/Users/sigma/Desktop/campaigns/data/imports/dbm.csv'
    cols = [
        'date',
        'dsp',
        'advertiser',
        'insertion_order',
        'strategy',
        'creative',
        'budget',
        'impressions',
        'clicks',
        'conversions',
        'post_clicks_conversions',
        'post_views_conversions',
    ]
    columns_to_rename = {
        'date': 'date',
        'dsp': 'dsp',
        'advertiser': 'advertiser',
        'insertion_order': 'insertion_order',
        'strategy': 'strategy',
        'creative': 'creative',
        'budget': 'budget',
        'impressions': 'impressions',
        'clicks': 'clicks',
        'conversions': 'conversions',
        'cv pc': 'post_clicks_conversions',
        'cv pv': 'post_views_conversions',
    }
    dtype = {
        'date': Date,
        'dsp': String,
        'advertiser': String,
        'insertion_order': String,
        'strategy': String,
        'creative': String,
        'budget': Float,
        'impressions': Integer,
        'clicks': Integer,
        'conversions': Integer,
        'post_clicks_conversions': Integer,
        'post_views_conversions': Integer
    }

    # Read file with pandas.
    try:
        df = pd.read_csv(
            file_path, sep=';',
            header=0,
            usecols=cols,
            index_col=False,
            on_bad_lines='skip',
        )
    except Exception as e:
        msg = "Cannot read file.\n\nError message:\n{}".format(e)
        messages.error(request, msg)
        return redirect('imports')
    else:
        df.rename(columns_to_rename, inplace=True)
        
     # Check that all mandatory keys are here.
    if not all(field in df.columns for field in cols):
        msg = "Cannot import file.\n\nError message:\nThe following fields \
            are mandatory: {}".format(", ".join(cols))
        messages.error(request, msg)
        return redirect('imports')

    message = ''
    if not len(df):
        message += 'No valid line to import.\n'
        return message
    # Get user insertion orders data
    user_insertion_orders = UserInsertionOrder.objects.all()
    user_insertion_orders_instances =[
        (user_insertion_order.__str__(), user_insertion_order.id)
        for user_insertion_order in user_insertion_orders
    ]
    user_insertion_orders_instances_df = pd.DataFrame(
        user_insertion_orders_instances,
        columns = ['insertion_order', 'insertion_order_id'])
  
    df = pd.merge(df, user_insertion_orders_instances_df,
        on='insertion_order', how='left')
    df.drop('insertion_order', axis=1, inplace=True)
    df.rename({'insertion_order_id': 'insertion_order'}, axis=1, inplace=True)
   
    df = df[~df['insertion_order'].isna()]

    try:
        df.to_sql(
            InsertionOrdersRealSpents._meta.db_table,
            if_exists='append',
            index=False,
            dtype=dtype,
            con=engine
        )
    except IntegrityError as e:
        msg = "Duplicated rows are not authorized"
        messages.error(request, msg) # e._message
      
        # C'est ici par la suite qu'il faudra gérer les lignes identiques
        # pour ne garder que celle qui est la plus à jour (impressions 
        # ou dépenses plus élevées)
        return redirect('imports')
    except Exception as e:
        messages.error(request, e.__cause__) # e.__class__
        return redirect('imports')
    else:
        message += "Data successfully imported {} nodes."
        messages.success(request, message)
        return redirect('imports')


# def task_upload_io_real_spents(request):
#     pass
