# -*- encoding: utf-8 -*-

import sqlite3
import numpy as np

def getids(qry):
    lst = []
    for idt in qry:
         lst.append(str(idt[0]))
    lst = np.array(lst)
    # print lst
    # print lst[0]
    np.savetxt('id_tweets.gz', lst, delimiter=" ", fmt="%s")   
    # f = open('./id_tweets.txt', 'w')
    # f.write(str(lst))
    # f.close()
    print len(lst)

con = sqlite3.connect("data.db")
con.isolation_level = None
cur = con.cursor()

sql = "select id_tweet from IMAGENS where servico = 'twitpic' and tipo = 'tweet';"

print sql

if sqlite3.complete_statement(buffer):
        try:
            # buffer = buffer.strip()
            cur.execute(slq)

            if sql.lstrip().upper().startswith("SELECT"):
                # print cur.fetchall()
                qry = cur.fetchall()
                # print qry
                getids(qry)
        except sqlite3.Error as e:
            print "An error occurred:", e.args[0]


# buffer = ""

# print "Enter your SQL commands to execute in sqlite3."
# print "Enter a blank line to exit."

# while True:
#     line = raw_input()
#     if line == "":
#         break
#     buffer += line
#     if sqlite3.complete_statement(buffer):
#         try:
#             buffer = buffer.strip()
#             cur.execute(buffer)

#             if buffer.lstrip().upper().startswith("SELECT"):
#                 # print cur.fetchall()
#                 qry = cur.fetchall()
#                 # print qry
#                 getids(qry)
#         except sqlite3.Error as e:
#             print "An error occurred:", e.args[0]
#         buffer = ""

con.close()




