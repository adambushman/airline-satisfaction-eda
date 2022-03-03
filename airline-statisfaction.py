import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

# Load the data (change to your personal directory)
os.chdir('C:/Users/Adam Bushman/Downloads')
aDataRaw = pd.read_csv('airlineSatisfaction.csv')

# Get a quick glimpse at the structure
print(aDataRaw.head())
print(aDataRaw.info())
print(aDataRaw.size)

# Explore extent of '0' satisfaction rating value
cats = ['Inflight wifi service','Departure/Arrival time convenient','Ease of Online booking','Gate location','Food and drink','Online boarding','Seat comfort','Inflight entertainment','On-board service','Leg room service','Baggage handling','Checkin service','Inflight service','Cleanliness']

zeroSum = pd.DataFrame(columns = ['categories', 'zerosPresent'])
zeroSum['categories'] = cats
zeroSum['zerosPresent'] = 0

for i in range(len(zeroSum)):
    cat = zeroSum['categories'].loc[i]
    zeroSum['zerosPresent'].loc[i] = len(aDataRaw[aDataRaw[cat] == 0])

print(zeroSum.head())

#################
# Data Cleaning #
#################

# Remove NA's (only present ~300 in "Arrival Delay in Minutes")
aDataNoNa = aDataRaw.dropna()

# Drop unnessary columns
aDataPostDrop = aDataNoNa.drop(columns = ['id', 'Departure/Arrival time convenient'])
aDataPostDrop.drop(aDataPostDrop.columns[0], axis = 1, inplace = True)


# Remove rows with 0 entry for satisfaction rating features
cats.remove('Departure/Arrival time convenient')

aDataZeros = aDataPostDrop
aDataZeros['Zeros Present'] = False

for ind, row in aDataZeros.iterrows():
    listTest = np.array(row[cats])
    y = np.where(listTest == 0)
    if y[0].size > 0:
        aDataZeros.loc[ind, 'Zeros Present'] = True

# We lose ~4700 rows by removing zeros from the satisfaction ratings
check = aDataZeros[aDataZeros['Zeros Present'] == True]
print('We lose', len(check), 'rows from our initial list of ', len(aDataPostDrop),', or appox', float(len(check)) / len(aDataPostDrop), 'percent')

aDataZeros = aDataZeros[aDataZeros['Zeros Present'] == False]
aDataZeros.drop(columns = ['Zeros Present'], inplace = True)


# Converting categorical columns to dummy variables
columnsStrip = ['Age', 'Flight Distance', 'Inflight wifi service', 'Ease of Online booking', 'Gate location', 'Food and drink', 'Online boarding', 'Seat comfort', 'Inflight entertainment', 'On-board service', 'Leg room service', 'Baggage handling', 'Checkin service', 'Inflight service', 'Cleanliness', 'Departure Delay in Minutes', 'Arrival Delay in Minutes']
aDataStripped = aDataZeros[columnsStrip]

aDataDummies = aDataZeros.loc[ : , aDataZeros.columns.isin(columnsStrip) == False]

dummies = []

# For loop to expand dummy columns
for col in aDataDummies.columns:
    df = pd.get_dummies(aDataDummies[col])
    dummies.append(df)

dummies.append(aDataStripped)
aDataWithDummies = pd.concat(dummies, axis = 1)

# Rename columns
renameDict = {'disloyal Customer': 'Disloyal Customer', 'Business': 'Business Class', 'Eco': 'Economy Class', 'Eco Plus': 'Economy Plus', 'neutral or dissatisfied': 'Not Satisfied', 'satisfied': 'Satisfied'}
aDataWithDummies.rename(columns=renameDict, inplace = True)
aDataZeros.rename(columns=renameDict, inplace = True)

######################
# Final Cleaned Data #
######################
aDataClean = aDataZeros #Without dummies
aDataCleanD = aDataWithDummies #With dummies

######################
# Data Visualization #
######################

#Boxplot by age and ease of booking online
sb.set_theme(style="whitegrid")
sb.set(style='ticks')
ax = sb.boxplot(x='Ease of Online booking', y='Age', data=aDataClean)
plt.show()

#Boxplot by customer type and for 2,000+ mile long flights
dataFiltered = aDataClean[aDataClean['Flight Distance'] >= 2000]
ax = sb.boxplot(x='satisfaction', y='Flight Distance', data=dataFiltered)
plt.show()


# ax = sb.histplot(data = aDataClean, x = 'Departure Delay in Minutes', bins = 10)
#plt.show()


######################
# Summary Statistics #
######################

#Delays (+30 mins)
dataFiltered = aDataClean[(aDataClean['Departure Delay in Minutes']) >= 30 | (aDataClean['Arrival Delay in Minutes'] >= 30)]

#By customer type
pd.crosstab(dataFiltered['Customer Type'], dataFiltered['satisfaction'])
   # Fisher's test reports p-value < 0.00001

#By travel type
pd.crosstab(dataFiltered['Type of Travel'], dataFiltered['satisfaction'])
   # Fisher's test reports p-value < 0.00001

#Long Flights (+2000 miles)
dataFiltered = aDataClean[(aDataClean['Flight Distance']) >= 2000]

#By seat class
pd.crosstab(dataFiltered['Class'], dataFiltered['satisfaction'])
   # Chi-squared test estimates p-value < 0.00001

#Random summary statistics
print('Median Departure Delay:', aDataClean['Departure Delay in Minutes'].median())
print('Departure Delay StDev:', np.std(aDataClean['Departure Delay in Minutes']))

print('Median Arrival Delay:', aDataClean['Arrival Delay in Minutes'].median())
print('Arrival Delay StDev:', np.std(aDataClean['Arrival Delay in Minutes']))

dataSub40 = aDataClean[aDataClean['Age'] < 40]
dataPlus40 = aDataClean[aDataClean['Age'] >= 40]
print('Average Satisfaction with Online Booking (age < 40):', dataSub40['Ease of Online booking'].mean())
print('Satisfaction with Online Booking StDev (age < 40):', np.std(dataSub40['Ease of Online booking']))

print('Average Satisfaction with Online Booking (age >= 40):', dataPlus40['Ease of Online booking'].mean())
print('Satisfaction with Online Booking StDev (age >= 40):', np.std(dataPlus40['Ease of Online booking']))