import pathlib

import sqlite3

#A toy sql driver with python
class SQLiteDatabase:
    # Called when the object is initialized
    def __init__(self, db_file, schema_dir='schemas/'):
        #connect to sqlite automatically
        self.con = sqlite3.connect(db_file)
        
        # Create our tables
        schemas_path = pathlib.Path(schema_dir)
        for schema_file in schemas_path.glob('*.sql'):
            with open(schema_file, 'r') as f:
                schema_query = f.read()

                #cursor is opening sqlite
                cur = self.con.cursor()
                #execute means hitting enter 
                cur.execute(schema_query)

    # Called when the object is deleted
    def __del__(self):
        self.con.close()

    # INSERT INTO movies (name, rating, genre) VALUES ('Titanic', 9, 'Romance')
    def insert(self, table, data):
        cur = self.con.cursor()

        keys = data.keys()
        #the command in sql is in a tuple format
        values = tuple(data.values())
        columns = ', '.join(keys)
        placeholders = ', '.join(['?'] * len(keys))

        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        #the values are for the placeholders
        cur.execute(query, values)

        #when you insert/delete you have to commit your change to save them to the db
        self.con.commit()

    # DELETE FROM movies WHERE movieId = '6
    def delete(self, table, where_clause):
        cur = self.con.cursor()

        query = f'DELETE FROM {table} WHERE {where_clause}'
        cur.execute(query)

        self.con.commit()

    # SELECT * FROM directors
    def select(self, table, where_clause='1=1'):
        cur = self.con.cursor()

        query = f'SELECT * FROM {table} WHERE {where_clause}'
        cur.execute(query)

        #fetchall() gets the result of the query
        return cur.fetchall()
    
    #UPDATE movies SET name='Titanic', genre='Romance' where movieId=2;
    def update(self, table, update_data, where_clause):
        cur = self.con.cursor()

        keys = update_data.keys()
        placeholders = ', '.join(f'{column} = ?' for column in keys)
        values = tuple(update_data.values()) 
        query = f'UPDATE {table} SET {placeholders} WHERE {where_clause}'
        cur.execute(query, values)

        self.con.commit()

db = SQLiteDatabase('movies.db')

data = {
    'name': 'Christopher',
    'familyName': 'Nolan'
}

#db.insert('director', data)

#db.delete('movies', 'movieId = 5')

#print(db.select('director', 'directorId = 2'))

update_data = {
    'name': 'Kung fu Panda 2',
    'rating': 7.8
}

db.update('movies', update_data, 'movieId=3')
