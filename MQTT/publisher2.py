import paho.mqtt.client as mqtt
import time
import numpy
from datetime import datetime

id_pu = 1
id_publishera = str(id_pu)

id_k = 1
id_kanału = str(id_k)

temat = 1 # nazwa katalogu z danymi


od = 200 # wartość minimalna
do = 1000 # wartość maksymalna


def generator_danych(temat, od, do):

    g1 = do - ((do - od)/2) # środek rozkładu normalnego
    g2 = (do - od)/2 # odchylenie standardowe
    g3 = 1 # liczba generowanych próbek
    
    probka = numpy.random.normal(g1, g2, g3)
    
    while((probka > do) or (probka < od)): # odrzuca wartości z poza przedziału
        probka = numpy.random.normal(g1, g2, g3)
        
    return probka
     

client=mqtt.Client()
client.connect("127.0.0.1",1883,60)

for i in range(20):
    W = float(generator_danych(temat, od, do))
    W_in_String=str(W)
    
    teraz = datetime.now()
    stempel_czasu = datetime.timestamp(teraz)
    czas = datetime.fromtimestamp(stempel_czasu)
    czas_in_string = str(czas)
    
    wiadomosc = czas_in_string + "/" + id_publishera + "/" + id_kanału + "/" + W_in_String
    
    
    client.publish("topic/test/"+str(temat),wiadomosc)
    print(W)
    time.sleep(1)

client.disconnect()
