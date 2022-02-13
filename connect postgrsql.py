import psycopg2
import requests
from datetime import datetime

#enter ur server data
while True:
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="G7SoftEng",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="fmsdb")
        cursor = connection.cursor()

        now = datetime.now().time()

#request data from thingspeak
        msg=requests.get("https://api.thingspeak.com/channels/1615673/feeds.json?results=1")
        time= now
        distance= msg.json()['feeds'][-1]['field1']


#insert ur database data here
        postgres_insert_query = """ INSERT INTO dms_dms (time, distance) VALUES (%s,%s)"""
        record_to_insert = (time,distance)
        # executemany() to insert multiple rows
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into dms & arlam database")

        d2 = float(distance)
        if (d2 <= 10):
            postgres_insert_query = """ INSERT INTO dms_thingspeak (Time, Arlam) VALUES (%s,%s)"""
            arlam_to_insert = (time, 'on')
            cursor.execute(postgres_insert_query, arlam_to_insert)
            connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into dms", error)




    # closing database connection.
    if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")




    break