import sqlite3
import emoji

class EmojiDatabase:
    tableName = "emojireactions"
    dbName = "emojis.db"
    db = sqlite3.connect(dbName)
    cursor = db.cursor()

    defaultPairs = {
        "vore":  "👀",
        "foot": "🦶",
        "feet": "👣",
        "paw": "🐾",
        "bear": "🐻",
        "monkey": "🐵"
    }

    def __init__(self):
        tableCheck = self.cursor.execute("SELECT name FROM sqlite_master WHERE name='" + self.tableName + "'")
        if (tableCheck.fetchone() is None):
            self.cursor.execute("CREATE TABLE " + self.tableName + "(word,emoji)")
            print("Table created.")
        else:
            print("Table already exists.")

        for word in self.defaultPairs.keys():
            self.addPairToDB(word, self.defaultPairs[word])

        self.getListOfTriggerWords()

    def addPairToDB(self, key, value):

        if (key == None or value == None):
            print("User submitted empty values")
            return 0

        if (key in self.getListOfTriggerWords()):
            print(key + " already in database.")
            return 0
        
        if (not emoji.is_emoji(value)):
            print("User submitted non-emoji value.")
            return 0

        query = f"INSERT INTO {self.tableName} VALUES('{key}', '{value}')"
        self.cursor.execute(query)
        self.db.commit()
        return 1

    def getEmojiFromDB(self, word):
        query = f"SELECT emoji FROM {self.tableName} WHERE word IS '{word}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result
    
    def getListOfTriggerWords(self):
        query = f"SELECT word FROM {self.tableName}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        wordlist = [row[0] for row in result]
        return wordlist