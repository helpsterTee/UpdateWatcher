import sqlite3 as sql

class Database:
    conn = False

    def initDB(self):
        global conn
        conn = sql.connect("./db.sqlite")

        # init db, if not exists
        conn.execute('''CREATE TABLE IF NOT EXISTS to_watch
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            content TEXT NOT NULL,
            last_scraped DATE NOT NULL
            );
            ''')

    def closeDB(self):
        conn.close()

    def insertEntry(self, mode, name, url, content):
        global conn
        if conn == False:
            self.initDB()

        cur = conn.cursor()

        if mode == "insert":
            sql = ''' INSERT INTO to_watch
                    (name, url, content, last_scraped)
                    VALUES (?,?,?,date("now"));'''
            cur.execute(sql, (name, url, content))
        elif mode == "update":
            sql = ''' UPDATE to_watch SET
                    name = ?,
                    url = ?,
                    content = ?,
                    last_scraped = date("now")
                    WHERE name = ? AND url = ?;'''
            cur.execute(sql, (name, url, content, name, url))
        conn.commit()
        return cur.lastrowid

    def getEntryContent(self, name, url):
        global conn
        if conn == False:
            self.initDB()

        sql = ''' SELECT content FROM to_watch WHERE name = ? AND url = ?;'''

        cur = conn.cursor()
        cur.execute(sql, (name, url))
        rows = cur.fetchall()

        if len(rows) > 0:
            return rows[0][0]
        else:
            return False
