import psycopg2
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://buttz:Tritons1@localhost:5432/ucsdbb")

## just change the necessary_cols to fit what exactly you're looking for
## be careful because every column is in the form of a str, so you have to change the type of the cols if need be after querying the data
necessary_cols = ['Pitcher', 'PitcherThrows', 'PitcherTeam', 
                  "TaggedPitchType", "AutoPitchType", 
                  'RelSpeed', 'VertRelAngle', 'HorzRelAngle', 
                  'SpinRate', 'SpinAxis', 'RelHeight', 'RelSide', 
                  'Extension', 'InducedVertBreak', 'HorzBreak', 
                  'VertApprAngle', 'HorzApprAngle'
                  ]
DATASET = 'games'

cols_str = ", ".join([f'"{i}"' for i in necessary_cols])
df = pd.read_sql(f'SELECT {cols_str} FROM {DATASET};', engine)
print(df.head().dtypes)
print(df)