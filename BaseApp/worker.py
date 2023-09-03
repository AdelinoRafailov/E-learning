import threading
import pywhatkit
import logging
import csv
import socket
from datetime import datetime
import time
import os
import sys
import sqlite3

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
res = cur.execute("SELECT id,phone_number,content FROM neo4J_messagequeue").fetchall()

# for i in res:
#     print(i[0],i[1],i[2])

sql = '''UPDATE neo4J_messagequeue SET status = ? WHERE id = ?'''
for i in res:
    try:
        now = datetime.now()
        pywhatkit.sendwhatmsg("+" + str(i[1]), i[2],
                              now.hour, int(now.minute) + 1,  15, True, 2)
        cur.execute(sql, ("Done",i[0],))
    except Exception as e:
        cur.execute(sql, ("fail " + str(e),i[0],))
        pass

    con.commit()
        # messageQueue.objects.filter(id=id).update(status="Failed " + str(e))

 