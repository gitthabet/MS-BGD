import sqlite3 as lite
import sys

con = lite.connect('beyonce_vs_rihanna.db')

with con:

  cur = con.cursor()
  cur.execute("CREATE TABLE Beyonce_details(Curr_date TEXT, Title TEXT, Views INT, Likes INT, Dislikes INT)")
  cur.execute("CREATE TABLE Rihanna_details(Curr_date TEXT, Title TEXT, Views INT, Likes INT, Dislikes INT)")
  cur.execute("CREATE TABLE Beyonce_stats(Curr_date TEXT, Total_likes INT, Total_dislikes INT, Total_views INT)")
  cur.execute("CREATE TABLE Rihanna_stats(Curr_date TEXT, Total_likes INT, Total_dislikes INT, Total_views INT)")
