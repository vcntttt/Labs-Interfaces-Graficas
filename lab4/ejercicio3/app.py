from sqlite3 import connect
import matplotlib.pyplot as plt
import telepot
from env import TELEPOT_TOKEN, CHAT_ID
import matplotlib
matplotlib.use('Qt5Agg') # esto es linux momento
dbPathData = 'ejercicio2/contaminacion.db'

def getData():
    try:
        connection = connect(dbPathData)
        db = connection.cursor()
        db.execute("SELECT * FROM T_Conta where nodo = 'N2'")
        data = db.fetchall() # [[id, nodo, d01, d25, d10]]
        return data
    except Exception as e:
        print(e)
    finally:
        connection.close()


data = getData()
d01 = [row[2] for row in data]
d25 = [row[3] for row in data]
d10 = [row[4] for row in data]
x = range(len(data))

plt.figure(figsize=(14, 6))
plt.plot(x, d01, label='d01', color='red')
plt.plot(x, d25, label='d25', color='blue')
plt.plot(x, d10, label='d10', color='green')

plt.title("Contaminación en N2")
plt.xlabel("Indice de Muestra")
plt.ylabel("Contaminación")
plt.legend()
plt.grid()
plt.savefig('graph.png')
plt.show()
plt.close()


try:
    bot = telepot.Bot(TELEPOT_TOKEN)
    bot.sendPhoto(chat_id=CHAT_ID, photo=open('graph.png', 'rb'))
except Exception as e:
    print(e)