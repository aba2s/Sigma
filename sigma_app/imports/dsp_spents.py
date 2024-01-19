import pandas as pd
from django.db import connection
from sqlalchemy.exc import IntegrityError
from . import static # static variables
from .static import get_connection
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django_q.tasks import async_task
from sigma_app import q_services
from sigma_app.models import UserInsertionOrder
from sigma_app.models import AsynchroneTask
from sigma_app.models import BatchName


# GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
try:
    engine = get_connection()
except Exception as e:
    print("Connection could not be made due to the following error: \n", e)


def task_upload_dsp_spents(file_path, pk):
    """
    This function will be common to all DSPs for importing data.
    """

    cols = static.cols
    dtype = static.dtype

    batch_name = get_object_or_404(BatchName, pk=pk)
    dsp =batch_name.dsp

    try:
        # df_import is initial imported file
        df = pd.read_csv(
            file_path,
            sep=';',
            header=0,
            usecols=cols,
            index_col=False,
            on_bad_lines="skip",
        )
    
    except Exception as e:
        msg = "Cannot read file.\n\nError message:\n{}".format(e)
        raise Exception(msg)
    else:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        df.rename(static.renamed_cols_dict, inplace=True)
        df["dsp"] = dsp

        # Check that all mandatory keys are here.
        if not all(field in df.columns for field in cols):
            msg = "Cannot import file.\n\nError message:\nThe following fields \
                are mandatory: {}".format(
                ", ".join(cols)
            )
            raise Exception(msg)
    
    msg = ""

    # Making sure data is correctly read
    if not len(df):
        msg += "No valid line to import.\n"
        raise Exception(msg)
    
    # Get user insertion orders data
    user_insertion_orders = UserInsertionOrder.objects.all()
    if not user_insertion_orders:
        msg = "No user insertion order exists or saved"
        raise Exception(msg)
    
    user_insertion_orders_instances = [
        (user_insertion_order.__str__(), user_insertion_order.id)
        for user_insertion_order in user_insertion_orders
    ]
    user_insertion_orders_instances_df = pd.DataFrame(
        user_insertion_orders_instances,
        columns=["insertion_order", "insertion_order_id"],
    )

    df = pd.merge(
        df, user_insertion_orders_instances_df, on="insertion_order", how="left"
    )
    df.drop("insertion_order", axis=1, inplace=True)
    df.rename({"insertion_order_id": "insertion_order"}, axis=1, inplace=True)
    # Remove line that does not match (na values)
    df = df[~df["insertion_order"].isna()]

    if df.empty:
        msg = "Dataframe is Empty. No insertion order is uploaded.\
            Make sure user insertion orders are setted up."
        # print(traceback.print_exception)
        raise Exception(msg)

    try:    
        df.to_sql(
            dsp, # Xandr._meta.db_table,
            if_exists="append",
            index=False,
            dtype=dtype,
            chunksize=1000,
            con=engine,
        )
    except IntegrityError as e:
        # msg = "{}: Duplicated rows are not authorized".format(e.__cause__)
        msg = "Duplicated rows are not authorized."
        raise Exception(msg)
    
    except Exception as e:
        msg = e.__cause__
        raise Exception(msg)
    else:
        msg += "Data successfully imported."
        return msg
    

def upload_dsp_spents(request, pk):
    """
    This function is for uploading DSP media spents
    """
   
    batch_name = get_object_or_404(BatchName, pk=pk)
    dsp =batch_name.dsp

    # Beofre going further, let's check if the table name exists and
    # created by the models.py    
    tables = connection.introspection.table_names()
    if dsp not in tables:
        msg = "{} is not a models.py table. \
            Please inform administrator.".format(dsp)
        messages.error(request, msg)
        return redirect('imports')

    file_path = settings.IMPORTS_PATH + "dsps" + ".csv"

    task_id = async_task(
        task_upload_dsp_spents,
        file_path,
        pk,
        hook=q_services.str_hook,
    )
    asynchrone_task = AsynchroneTask(
        id=task_id,
        title="Importing {} data".format(dsp),
        batch_name=batch_name,
        user=request.user
    )
    asynchrone_task.save()

    msg = "{} media spents successully uploaded".format(dsp)
    messages.success(request, msg)
    return redirect('imports')

 