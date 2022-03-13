import sqlite3
import numpy as np

con = sqlite3.connect("testset.sqlite")
con.create_function("log2", 1, np.log2)

f = open('query.sql')
query = f.read()

cur = con.cursor()
cur.execute(query)
print(cur.fetchall()[:10])