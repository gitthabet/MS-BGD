import sys, csv
import sqlite3 as lite

con = lite.connect('beyonce_vs_rihanna.db')
with con:
  cur = con.cursor()
  # Saving detailled data
  cur.execute('''SELECT b.Curr_date,b.Total_likes, b.Total_dislikes, b.Total_views,r.Total_likes, r.Total_dislikes, r.Total_views  FROM Beyonce_stats  b, Rihanna_stats r WHERE b.Curr_date = r.Curr_date LIMIT 100''')

  rows = cur.fetchall()

  f = open('data.tsv', 'wt')
  try:
      writer = csv.writer(f)
      writer.writerow( ('date', 'b.likes', 'b.dislikes','b.views','r.likes', 'r.dislikes','r.views' ) )
      for row in rows:
          writer.writerow( (row[0], row[1], row[2], row[3], row[4],row[5],row[6]) )
  finally:
      f.close()
