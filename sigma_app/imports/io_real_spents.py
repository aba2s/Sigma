from datetime import date
from sqlalchemy.types import Integer
from sqlalchemy.types import Float
from sqlalchemy.types import String
from sqlalchemy.types import Date
import pandas as pd
from sigma_app.models import *
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from django_q.tasks import async_task
from sigma_app import q_services
import traceback
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
    
def import_files(path, cols, dtype, etc):
    pass

def task_upload_io_real_spents(file_path):
    '''
    Insertion orders real spents
    '''

    # Read file with pandas.
    try:
        df_import = pd.read_csv(
            file_path, sep=';',
            header=0,
            usecols=cols,
            index_col=False,
            on_bad_lines='skip',
        )
    except Exception as e:
        msg = "Cannot read file.\n\nError message:\n{}".format(e)
        raise Exception(msg)
    else:
        df_import.rename(columns_to_rename, inplace=True)
     # Check that all mandatory keys are here.
    if not all(field in df_import.columns for field in cols):
        msg = "Cannot import file.\n\nError message:\nThe following fields \
            are mandatory: {}".format(", ".join(cols))
        raise Exception(msg)

    msg = ''
    if not len(df_import):
        msg += 'No valid line to import.\n'
        raise Exception(msg)
        
    # Get user insertion orders data
    user_insertion_orders = UserInsertionOrder.objects.all()
    user_insertion_orders_instances =[
        (user_insertion_order.__str__(), user_insertion_order.id)
        for user_insertion_order in user_insertion_orders
    ]
    user_insertion_orders_instances_df = pd.DataFrame(
        user_insertion_orders_instances,
        columns = ['insertion_order', 'insertion_order_id'])
  
    df = pd.merge(df_import, user_insertion_orders_instances_df,
        on='insertion_order', how='left')
    df.drop('insertion_order', axis=1, inplace=True)
    df.rename({'insertion_order_id': 'insertion_order'}, axis=1, inplace=True)
   # Remove line that does not match (na values)
    df = df[~df['insertion_order'].isna()]
    if df.empty:
        msg = "Dataframe is Empty. No insertion order is uploaded"
        # return msg
        print(traceback.print_exception)
        raise Exception(msg)

    try:
        df.to_sql(
            InsertionOrdersRealSpents._meta.db_table,
            if_exists='append',
            index=False,
            dtype=dtype,
            chunksize=1000,
            con=engine
        )
    except IntegrityError as e:
        # qs = InsertionOrdersRealSpents.objects.all()
        # df_qs = pd.DataFrame(qs.values(*cols))
        # df.to_sql(
        #     InsertionOrdersRealSpents._meta.db_table,
        #     if_exists='append',
        #     index=False,
        #     dtype=dtype,
        #     chunksize=1000,
        #     con=engine
        # )
        msg = "Duplicated rows are not authorized"
        raise Exception(msg)
       
    except Exception as e:
        msg = e.__cause__
        raise Exception(msg)
    else:
        msg += "Data successfully imported {} insertions orders \
            sur un total de {}".format(df.shape[0], df_import.shape[0]
        )
        return msg
    

def upload_io_real_spents(request):
    batch_name = get_object_or_404(BatchName,
        pk="00000000-0000-0000-0000-000000000001"
     )
    file_path = settings.IMPORTS_PATH + 'dbm.csv'
    task_id = async_task(
        task_upload_io_real_spents,
        file_path,
        hook=q_services.str_hook,
    )
    asynchrone_task = AsynchroneTask(
        id=task_id,
        title= 'Importing Consolidated DSPs data',
        dsp=batch_name,
        user=request.user
    )
    asynchrone_task.save() 
    messages.success(request, "Task successfully started.")
    #time.sleep(5)
    return redirect('imports')
