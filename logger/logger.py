import pandas as pd
from datetime import datetime
import os

class Logger:

    def __init__(self, logpath):
        
        if not os.path.exists(logpath):
            os.makedirs(logpath)

        self.LOGFILE = logpath + "event_log.csv"

    def createDataBase(self):
        
        if os.path.exists(self.LOGFILE):
            return
        
        data = {"Name": [],
                "Tool": [],
                "Pickup Timestamp": [],
                "Return Timestamp": []}
        
        df = pd.DataFrame(data)

        df.to_csv(self.LOGFILE, index=False)

    def insert_tools(self):

        load = pd.read_csv(self.LOGFILE)

        if any(load["Tool"].str.contains("Hammer")) or any(load["Tool"].str.contains("Scissor")):
            return

        scissor = {"Name": ["Inital_insert"],
            "Tool": ["Scissor"],
            "Pickup Timestamp": [datetime.now()],
            "Return Timestamp": [datetime.now()]}
        
        hammer = {"Name": ["Inital_insert"],
            "Tool": ["Hammer"],
            "Pickup Timestamp": [datetime.now()],
            "Return Timestamp": [datetime.now()]}
        
        df1 = pd.DataFrame(hammer)
        df2 = pd.DataFrame(scissor)

        frames = [load, df1, df2]
        loaded_df = pd.concat(frames)
        loaded_df.to_csv(self.LOGFILE, index=False)

    def log_empty(self):
        return pd.read_csv(self.LOGFILE).empty

    def updateOnPicking(self, name, tool):
        data = {"Name": [name],
                "Tool": [tool],
                "Pickup Timestamp": [datetime.now()],
                "Return Timestamp": [-1]}
        
        df = pd.DataFrame(data)
        load = pd.read_csv(self.LOGFILE)

        frames = [load, df]
        loaded_df = pd.concat(frames)

        loaded_df.to_csv(self.LOGFILE, index=False)


    def updateOnReturning(self, name, tool):
        
        load = pd.read_csv(self.LOGFILE)
        mask = (load["Name"] == name) & (load["Tool"] == tool)
        load.loc[mask, "Return Timestamp"] = datetime.now()

        load = pd.DataFrame(load)
        load.to_csv(self.LOGFILE, index=False)

    def checkAvailability(self):
        
        load = pd.read_csv(self.LOGFILE)

        available_rows = load[load["Return Timestamp"] == "-1"]

        tool_availability = {tool: False for tool in available_rows["Tool"].unique()}

        for tool, last_row in load.groupby("Tool").last().iterrows():
            if tool not in tool_availability:
                tool_availability[tool] = True
        
        return tool_availability

    def register(self, name):
        data = {"Name": [name],
                "Tool": ["register"],
                "Pickup Timestamp": [datetime.now()],
                "Return Timestamp": [None]}
        df = pd.DataFrame(data)
        load = pd.read_csv(self.LOGFILE)

        frames = [load, df]
        loaded_df = pd.concat(frames)
        loaded_df.to_csv(self.LOGFILE, index=False)

    def find_users(self):
        load = pd.read_csv(self.LOGFILE)
        register_rows = load[load["Tool"] == "register"]
        users = register_rows["Name"].unique()
        users.tolist()
        return users

    def getBackground(self, name):

        load = pd.read_csv(self.LOGFILE)

        return load[load["Name"] == name]
    
    def get_n_latest_records(self, n):
        load = pd.read_csv(self.LOGFILE)
        if n > len(load):
            print("Input longer than dataframe")
            return pd.DataFrame()
        latest_entries = load.tail(n)
        return latest_entries

def main(LOGFILE):
    LOGFILE = logpath + "event_log.csv"
    try:
        load = pd.read_csv(LOGFILE)
    except FileNotFoundError:
        print(f"No logfile excist")
        return None
    logger = Logger(logpath)
    query = "Enter a name to recieve all logged data to that user or a number to get the n latest records: "
    user_input = input(query)
    while True:
        try:
            user_input = int(user_input)
            log = logger.get_n_latest_records(user_input)
            if not log.empty:
                print(log)
                break
        except ValueError:
            if user_input in load["Name"].values:
                log = logger.getBackground(user_input)
                print(log)
                break
            else:
                print("User not in log")
        
        user_input = input(query)

if __name__ == "__main__":
    logpath = "logs/"
    main(logpath)
