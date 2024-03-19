import pandas as pd
from datetime import datetime

LOGFILE = "event_log.csv"

def createDataBase():

    data = {"Name": [],
            "Tool": [],
            "Pickup Timestamp": [],
            "Return Timestamp": []}
    
    df = pd.DataFrame(data)

    df.to_csv(LOGFILE, index=False)


def updateOnPicking(name, tool):
    data = {"Name": [name],
            "Tool": [tool],
            "Pickup Timestamp": [datetime.now()],
            "Return Timestamp": [-1]}
    
    df = pd.DataFrame(data)
    load = pd.read_csv(LOGFILE)

    frames = [load, df]
    loaded_df = pd.concat(frames)

    loaded_df.to_csv(LOGFILE, index=False)


def updateOnReturning(name, tool):
    
    load = pd.read_csv(LOGFILE)

    counter = 0
    for el in load["Tool"]:

        dic = load.to_dict()
        

        if dic["Name"][counter] == name and int(dic["Return Timestamp"][counter]) == -1 and dic["Tool"][counter] == tool:
            
            dic["Return Timestamp"][counter] = datetime.now()
            break

        counter += 1

    df = pd.DataFrame(dic)
    df.to_csv(LOGFILE, index=False)


def getBackground(name):

    load = pd.read_csv(LOGFILE)
    dic = load.to_dict()

    retList = []
    counter = 0
    for element in load["Name"]:
    
        if element == name:
            retList.append([dic["Tool"][counter], dic["Pickup Timestamp"][counter], dic["Return Timestamp"][counter]])
        counter += 1

    return retList
