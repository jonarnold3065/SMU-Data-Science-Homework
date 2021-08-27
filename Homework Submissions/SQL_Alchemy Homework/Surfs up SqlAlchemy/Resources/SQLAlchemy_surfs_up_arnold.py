%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import pandas as pd
import numpy
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

query = "SELECT max(date) from measurement"
engine.execute(query).fetchall()

db = engine.connect()


query = """
#             SELECT
#                 date,
#                 avg(prcp) as prcp
#             FROM
#                 measurement
#             WHERE
#                 date >= '2016-08-23'
#                 and prcp is not null
#             group by
#                 date
#             order by
#                 date asc
#         """

# Query All Records in the the Database
df = pd.read_sql(query, con=db)

# Preview the Data
df.head(10)


