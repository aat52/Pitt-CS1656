import sqlite3 as lite
import csv
import re
import pandas as pd
import argparse
import collections
import json
import glob
import math
import os
import requests
import string
import sqlite3
import sys
import time
import xml


class Movie_db(object):
    def __init__(self, db_name):
        #db_name: "cs1656-public.db"
        self.con = lite.connect(db_name)
        self.cur = self.con.cursor()

    #q0 is an example
    def q0(self):
        query = '''SELECT COUNT(*) FROM Actors'''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q1(self):
        query = '''
            SELECT fname, lname
        	FROM Actors, Cast c1, Cast c2, Movies m1, Movies m2
        	WHERE Actors.aid = c1.aid
        	AND c1.mid = m1.mid
            AND c2.mid = m2.mid
        	AND Actors.aid = c2.aid
            AND (m1.year <= 1990 AND m1.year >= 1980)
        	AND m2.year >= 2000
        	ORDER BY fname ASC, lname ASC
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q2(self):
        query = '''
            SELECT title, year
            FROM Movies
            WHERE rank > (SELECT rank
                FROM Movies
                WHERE title = "Rogue One: A Star Wars Story")
            AND year = (SELECT year
                FROM Movies
                WHERE title = "Rogue One: A Star Wars Story")
            ORDER BY title ASC
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q3(self):
        query = '''
            DROP VIEW IF EXISTS movie_count
        '''
        self.cur.execute(query)

        query = '''
            create view movie_count as
        		SELECT fname, lname, title
        		FROM Actors
                NATURAL JOIN Cast
                NATURAL JOIN Movies
                WHERE title LIKE '%Star Wars%'
        '''
        self.cur.execute(query)

        query = '''
            SELECT fname, lname, COUNT(DISTINCT title) AS count
            FROM movie_count
            GROUP BY fname, lname
            ORDER By count DESC, lname, fname
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q4(self):
        query = '''
            DROP VIEW IF EXISTS pre1980
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW pre1980 AS
                SELECT c.aid
                FROM Movies as m, Cast as c, Actors as a
                WHERE m.mid IN (SELECT mid
                    FROM Movies as m
                    WHERE m.year < 1980)
                AND m.mid = c.mid AND c.aid = a.aid
        '''
        self.cur.execute(query)

        query = '''
            DROP VIEW IF EXISTS post1980
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW post1980 AS
                SELECT c.aid
                FROM Movies as m, Cast as c, Actors as a
                WHERE m.mid IN (SELECT mid
                    FROM Movies as m
                    WHERE m.year >= 1980)
                AND m.mid = c.mid AND c.aid = a.aid
        '''
        self.cur.execute(query)

        query = '''
            SELECT DISTINCT a.fname, a.lname
            FROM pre1980, Actors as a
            WHERE pre1980.aid NOT IN post1980 AND a.aid = pre1980.aid
            ORDER BY a.lname, a.fname
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q5(self):
        query = '''
            SELECT d.fname, d.lname, COUNT(*) AS count
        	FROM Directors as d
        	NATURAL JOIN Movie_Director
        	GROUP BY d.fname, d.lname
        	ORDER BY count DESC, d.lname ASC, d.fname ASC
        	LIMIT 10
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q6(self):

        query = '''
            DROP VIEW IF EXISTS c2count
        '''
        self.cur.execute(query)

        query = '''
        CREATE VIEW c2count AS
            SELECT COUNT(c2.aid) AS num_cast2
                  FROM Movies AS m2
                  NATURAL JOIN Cast AS c2
                  GROUP BY m2.mid
                  ORDER BY num_cast2 DESC
                  LIMIT 10
        '''
        self.cur.execute(query)

        query = '''
            SELECT m.title, COUNT(c.aid) AS num_cast
        	FROM Movies AS m
        	NATURAL JOIN Cast AS c
        	GROUP BY m.mid
        	HAVING num_cast >= (SELECT MIN(num_cast2)
        	   FROM c2count)
        	ORDER BY num_cast DESC
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q7(self):
        query = '''
            DROP VIEW IF EXISTS movie_men
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW movie_men AS
                SELECT c1.mid, COUNT(a1.gender) as men
                FROM Cast AS c1
                NATURAL JOIN Actors as a1
                WHERE a1.gender = 'Male'
                GROUP BY c1.mid
        '''
        self.cur.execute(query)

        query = '''
            DROP VIEW IF EXISTS movie_female
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW movie_female AS
                SELECT c.mid, COUNT(a.gender) as female
                FROM Cast AS c
                NATURAL JOIN Actors as a
                WHERE a.gender = 'Female'
                GROUP BY c.mid
        '''
        self.cur.execute(query)

        query = '''
            SELECT Movies.title as movie_title, fem.female AS women_count, males.men as men_count
            FROM Movies
            NATURAL JOIN movie_female as fem
            NATURAL JOIN movie_men as males
            WHERE women_count > men_count
            ORDER BY movie_title
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q8(self):
        query = '''
            SELECT a.fname, a.lname, count(DISTINCT d.did) AS director
            FROM Actors AS a, Directors AS d
            NATURAL JOIN Cast as c
            NATURAL JOIN Movie_Director AS md
            WHERE c.mid = md.mid AND md.did = d.did
            AND a.fname !=d.fname AND a.lname !=d.lname
            GROUP BY a.fname, a.lname
            HAVING director >= 7
            ORDER BY director DESC

        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q9(self):
        query = '''
            DROP VIEW IF EXISTS ActCast
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW ActCast AS
                SELECT *
                FROM Actors a
                NATURAL JOIN Cast c
        '''
        self.cur.execute(query)

        query = '''
            DROP VIEW IF EXISTS debut_count
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW debut_count AS
                SELECT MIN(year) AS debutYear, m.mid, aid, fname, lname
                FROM ActCast
                    NATURAL JOIN Movies m
                    GROUP BY aid
        '''
        self.cur.execute(query)

        query = '''
            SELECT fname, lname, COUNT(*)
            FROM ActCast
            NATURAL JOIN Movies m
            WHERE m.year = (SELECT debutYear
                FROM debut_count m
                WHERE m.aid = ActCast.aid)
            AND fname LIKE 'D%'
            GROUP BY fname, lname
            ORDER BY count(*) DESC
        '''
        self.cur.execute(query)

        all_rows = self.cur.fetchall()
        return all_rows

    def q10(self):
        query = '''
            SELECT a.lname, m.title
        	FROM Actors AS a
        	NATURAL JOIN Cast AS c
        	NATURAL JOIN Movies AS m
        	NATURAL JOIN Movie_Director AS md
        	INNER JOIN Directors AS d ON d.did = md.did
        	WHERE a.lname = d.lname
        	ORDER BY a.lname, m.title
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q11(self):
        query = '''
            DROP VIEW IF EXISTS Bacon0
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW Bacon0 AS
                SELECT c.mid AS cast
                FROM Cast AS c
                WHERE c.aid = (SELECT a.aid
                    FROM Actors AS a
                    WHERE a.fname = 'Kevin' AND a.lname = 'Bacon')
        '''
        self.cur.execute(query)

        query = '''
            DROP VIEW IF EXISTS Bacon1
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW Bacon1 AS
                SELECT a.aid
                FROM Bacon0, Movies AS m, Actors AS a, Cast AS c
                WHERE a.aid = c.aid AND c.mid = m.mid AND m.mid = bacon0.cast AND NOT (a.fname = 'Kevin' AND a.lname = 'Bacon')
                GROUP BY a.aid
        '''
        self.cur.execute(query)

        query = '''
            DROP VIEW IF EXISTS Bacon2
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW Bacon2 AS
                SELECT DISTINCT m.mid
                FROM Bacon1, Cast AS c, Movies AS m
                WHERE Bacon1.aid = c.aid AND c.mid = m.mid
        '''
        self.cur.execute(query)

        query = '''
            DROP VIEW IF EXISTS Bacon3
        '''
        self.cur.execute(query)

        query = '''
            CREATE VIEW Bacon3 AS
                SELECT DISTINCT a.aid AS Actor
                FROM Bacon2, Cast AS c, Movies AS m, Actors AS a
                WHERE c.mid = m.mid AND a.aid = c.aid AND m.mid = Bacon2.mid AND a.aid NOT IN Bacon1
                AND NOT (a.fname = 'Kevin' AND a.lname = 'Bacon')
        '''
        self.cur.execute(query)

        query = '''
            SELECT a.fname, a.lname
            FROM Bacon3, Actors AS a
            WHERE a.aid = Bacon3.Actor
            ORDER BY a.lname, a.fname
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q12(self):
        query = '''
            SELECT a.fname, a.lname, COUNT(m.mid), AVG(m.rank) AS popularity
        	FROM Actors AS a
        	NATURAL JOIN Cast AS c
        	NATURAL JOIN Movies AS m
        	GROUP BY a.aid
        	ORDER BY popularity DESC
        	LIMIT 20
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

if __name__ == "__main__":
    task = Movie_db("cs1656-public.db")
    rows = task.q0()
    print(rows)
    print()
    rows = task.q1()
    print(rows)
    print()
    rows = task.q2()
    print(rows)
    print()
    rows = task.q3()
    print(rows)
    print()
    rows = task.q4()
    print(rows)
    print()
    rows = task.q5()
    print(rows)
    print()
    rows = task.q6()
    print(rows)
    print()
    rows = task.q7()
    print(rows)
    print()
    rows = task.q8()
    print(rows)
    print()
    rows = task.q9()
    print(rows)
    print()
    rows = task.q10()
    print(rows)
    print()
    rows = task.q11()
    print(rows)
    print()
    rows = task.q12()
    print(rows)
    print()
