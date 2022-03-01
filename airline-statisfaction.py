import os
import pandas as pd

os.chdir('C:/Users/Adam Bushman/Downloads')

aDataRaw = pd.read_csv('airlineSatisfaction.csv')

print(aDataRaw.info())


# Stuff to get the zeros for each category column

cats = ['Inflight wifi service','Departure/Arrival time convenient','Ease of Online booking','Gate location','Food and drink','Online boarding','Seat comfort','Inflight entertainment','On-board service','Leg room service','Baggage handling','Checkin service','Inflight service','Cleanliness']

zeroSum = pd.DataFrame(columns = ['categories', 'zerosPresent'])

zeroSum['categories'] = cats
zeroSum['zerosPresent'] = 0

for i in range(len(zeroSum)):
    cat = zeroSum['categories'].loc[i]
    zeroSum['zerosPresent'].loc[i] = len(aDataRaw[aDataRaw[cat] == 0])

aDataDropped = aDataRaw.dropna()