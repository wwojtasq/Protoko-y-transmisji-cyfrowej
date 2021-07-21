import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import numpy
import sqlite3 as sl
from datetime import datetime

#subscriber


con = sl.connect('my-test.db') 
with con:
    con.execute("""
        CREATE TABLE POMIARY (  
            stempel_czasu DATETIME,
            id_urzadzenia INT,
            id_kanału INT,
            pomiar FLOAT
        );
    """)

sql = 'INSERT INTO POMIARY (stempel_czasu, id_urzadzenia, id_kanału, pomiar) values(?, ?, ?, ?)' 




l_danych = 20 #liczba przechowywanych wartości danego typu(tematu)

w_czasu = [None] * l_danych # wektor czasu
for i in range(len(w_czasu)):
    w_czasu[i] = i

    
W1 = [None] * l_danych # dane publishera 1
for i in range(len(W1)):
    W1[i] = 0



def on_connect(client, userdata, flags, rc):
    print("connected with result code"+str(rc))
    client.subscribe("topic/test/1")


def on_message(client, userdata, msg):
    #if msg.payload.decode() == "Hello World!"
    #print("Yes!")
    #client.disconnect()
    print(msg.payload.decode())
    #print(msg.payload)
    
    paczka = msg.payload.decode().split("/")
    dane = [paczka[0], paczka[1], paczka[2], paczka[3]]
    
    tmp = dane[0]
    tmp2 = datetime.strptime(tmp, '%Y-%m-%d %H:%M:%S.%f')
    dane[0] = tmp2
    #print(type(dane[0]))
    
    with con:
        con.execute(sql, dane)

    for j in range(len(W1)-1, 0, -1):# dodaje nową wartość i usuwa najstarszą
        W1[j] = W1[j-1]
    W1[0] = float(paczka[3]) #wartość pomiaru
    plt.plot(w_czasu, W1)
    plt.show()
    #print(W1);


client = mqtt.Client()
client.connect("127.0.0.1",1883,60)

client.on_connect = on_connect
client.on_message =on_message


client.loop_forever()


