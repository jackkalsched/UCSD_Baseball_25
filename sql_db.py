import datetime
import os
import paramiko
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd

## connects to the db with the intern role
def get_conn():
    return psycopg2.connect(dbname="ucsdbb", user="buttz", password="Tritons1", host="localhost", port=5432)

## the cursor to connect to the filezilla
SFTP_HOST = "ftp.trackmanbaseball.com"
SFTP_USER = "UCSanDiego"
SFTP_PASS = "B4pJ6szqV3"
REMOTE_BASE_DIR = "/v3"
LOCAL_DOWNLOAD_DIR = "./trackman_downloads"

## setting up the directory to download the files
os.makedirs(LOCAL_DOWNLOAD_DIR, exist_ok=True)
transport = paramiko.Transport((SFTP_HOST, 22))
transport.connect(username=SFTP_USER, password=SFTP_PASS)
sftp = paramiko.SFTPClient.from_transport(transport)

## specifications
START_DATE = datetime.date(2025, 2, 14)
END_DATE   = datetime.date(2025, 6, 22)
TABLE = 'games'

## loops through each day to adds the games to the db
current_date = START_DATE
while current_date <= END_DATE:
    ## takes in the day after to get the data from the day before 
    next_day = current_date + datetime.timedelta(days=1)
    remote_dir = f"{REMOTE_BASE_DIR}/{next_day:%Y/%m/%d}/CSV"
    file_prefix = current_date.strftime("%Y%m%d")

    try:
        sftp.chdir(remote_dir)
        for f in sftp.listdir():
            if f.startswith(file_prefix) and f.endswith("-1.csv"):
                local_path = os.path.join(LOCAL_DOWNLOAD_DIR, f)
                sftp.get(f, local_path)

                ## loading it into postgreSQL
                df = pd.read_csv(local_path)
                conn = get_conn()
                cur = conn.cursor()

                col_defs = ", ".join([f'"{c}" TEXT' for c in df.columns])
                cur.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE} (id SERIAL PRIMARY KEY, {col_defs}); """)
                cur.execute(f"""SELECT column_name FROM information_schema.columns WHERE table_name='{TABLE}' """)
                existing_cols = {r[0] for r in cur.fetchall()}
                for c in df.columns:
                    if c not in existing_cols:
                        cur.execute(f'ALTER TABLE {TABLE} ADD COLUMN "{c}" TEXT;')
                cols = list(df.columns)
                values = [tuple(x) for x in df.to_numpy()]
                columns = ",".join([f'"{c}"' for c in cols])
                execute_values(cur, f"INSERT INTO {TABLE} ({columns}) VALUES %s", values)
                conn.commit()
                cur.close(); conn.close()

    except FileNotFoundError as fe:
        print(fe)
    except Exception as e:
        print(e)

    current_date += datetime.timedelta(days=1)

sftp.close()
transport.close()


