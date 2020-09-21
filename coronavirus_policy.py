import streamlit as st
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint
import requests

st.write('# Coronavirus TTX POLICY')
st.subheader('Data Collection to prompt policy idea:')
st.write('Input a country below, and it will scrape the total cases/deaths per ' +
         'day from https://covid.ourworldindata.org/data/owid-covid-data.json')


r = requests.get("https://covid.ourworldindata.org/data/owid-covid-data.json")
stats = r.json()

country = st.text_input('Input Country (3 letter abbreviation):', 'USA')

newCaseList = []
totalCaseList = []
newDeathList = []
totalDeathList = []

try:
    for i in range(len(stats[country]["data"])):
        newCaseList.append(stats[country]["data"][i]["new_cases"])
        totalCaseList.append(stats[country]["data"][i]["total_cases"])
        newDeathList.append(stats[country]["data"][i]["new_deaths"])
        totalDeathList.append(stats[country]["data"][i]["total_deaths"])
    newCaseArr = np.array(newCaseList)
    totalCaseArr = np.array(totalCaseList)
    newDeathArr = np.array(newDeathList)
    totalDeathArr = np.array(totalDeathList)
    fig, ax = plt.subplots(4, 1, figsize = (15,15))
    fig.tight_layout(pad = 5.0)

    ax[0].plot(newCaseArr)
    ax[0].set_title("new case in " + country + " per day")
    ax[0].set_xlabel("days after " + stats[country]["data"][0]['date'])
    ax[0].set_ylabel("total number of cases cumulative")

    
    ax[1].plot(totalCaseArr)
    ax[1].set_title("total number of cases in " + country + " added per day")
    ax[1].set_xlabel("days after " + stats[country]["data"][0]['date'])
    ax[1].set_ylabel("total number of cases cumulative")

    ax[2].plot(newDeathArr)
    ax[2].set_title("new deaths in " + country + " per day")
    ax[2].set_xlabel("days after " + stats[country]["data"][0]['date'])
    ax[2].set_ylabel("total number of cases cumulative")

    ax[3].plot(totalDeathArr)
    ax[3].set_title("total number of deaths in " + country + " added per day")
    ax[3].set_xlabel("days after " + stats[country]["data"][0]['date'])
    ax[3].set_ylabel("total number of deaths cumulative")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
except:
    st.write("Invalid Country or attribute <total_cases> invalid for specific country :(")
    st.write("Try a different one!!!")


st.subheader('Coronavirus has affected multiple states in the US:')
st.write("Input a state, and if it's valid, it should show red dots where coronavirus cases are occuring")




state = st.text_input('Input State:', 'Georgia')
with open("COVID-19_Cases_US.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    latList = []
    lonList = []
    stateList = []
    for row in csv_reader:
        if row[3] == state:
            try:
                float(row[6])
                float(row[7])
                stateList.append(row[3])
                latList.append(float(row[6]))
                lonList.append(float(row[7]))
            except:
                continue

stats3 = pd.DataFrame({
    'province' : stateList,
    'lat' : latList,
    'lon' : lonList
})

midpoint = (np.average(stats3['lat']), np.average(stats3['lon']))
st.deck_gl_chart(
            viewport={
                'latitude': midpoint[0],
                'longitude':  midpoint[1],
                'zoom': 4
            },
            layers=[{
                'type': 'ScatterplotLayer',
                'data': stats3,
                'radiusScale': 3,
   'radiusMinPixels': 5,
                'getFillColor': [248, 24, 148],
            }]
        )









st.subheader('Policy: Pre-install Novid type App in a new iPhone/Mobile Update')
st.write('''For each of the country's graphs, clearly the total number of cases is rising at an exponential rate.
It's not easy for everyone to always follow the rules nor mind their surroundings. I think
it would be best if we could have a Novid app that is preinstalled in a new update, such that many
users have access to it. This way, we can ensure everyone is 6 feet apart.''')

st.subheader("Group Roles:")
st.write(''' Group 2: Could develop a new Novid type app that interfaces well with iPhone and follows
Apple's new privacy policies.''')
st.write('''Group 3: Points system for social distancing, every day you log in, leaderboard with points get
special prize, etc''')
st.write('''Group 4: For the people consenting for data usage on their iPhones, we can do some sort of data
clustering (Kmeans, etc) and see how app is actually performing''')
