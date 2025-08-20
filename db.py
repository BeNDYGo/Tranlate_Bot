import sqlite3

DB_NAME = 'db.db'

db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

def init():
    cursor.execute("CREATE TABLE IF NOT EXISTS UsersData (username TEXT, data TEXT)")
    db.commit()

def add_word(username, inputUser):
    cursor.execute("INSERT INTO UsersData (username, data) VALUES (?, ?)", (username, inputUser))
    db.commit()

def get_words(username):
    cursor.execute("SELECT data FROM UsersData WHERE username = ?", (username,))
    return cursor.fetchall()

def del_word(username, inputUser):
    cursor.execute("DELETE FROM UsersData WHERE username = ? AND data = ?", (username, inputUser))
    db.commit()

def all():
    cursor.execute("SELECT * FROM UsersData")
    return cursor.fetchall()

data = ['enough - достаточно',
'relationship - отношения',
'friendship - дружба',
'should - должен',
'rug - ковёр',
'awesome - устрашающий',
'authentic - стентичный/подлинный',
'the same - такой же',
'ever - всегда',
'besides - кроме',
'leading - ведущий',
'numb - онемевший',
'spirit - дух',
'until - до',
'lead - вести',
'clean - чистый',
'insult - оскорблять',
'unbearable - невыносимо',
'around - вокруг',
'soul - душа',
'sober - трезвый',
'violent - жестокий',
'through - через',
'pretty - симпатичный',
'weak - слабый',
'wild - дикий',
'waves - волны',
'madly - безумно',
'hopelessly - безнадежно',
'twist - крутить',
'leading - ведущий',
'burns - ожоги',
'fear - страх',
'throw - бросать',
'dumpster - мусорный контейнер',
'interact - взаимодействовать',
'witch - ведьма',
'even - даже',
'means - означать',
'same - такой же',
'letting - сдача в аренду',
'delusions - заблуждение',
'consume - потреблять',
'loyalty - верность',
'fit - подходить',
'avoid - избегать',
'god/goddes - бог/богиня',
'prisoner - заключенный',
'own - собственный',
'void - пустота',
'capture - захватывать/снимать',
'determine - определять',
'faith - вера']

if __name__ == "__main__":
    for i in all():
        print(i)
        #add_word('BeNDYGo0', i)
    db.commit()
    db.close()
