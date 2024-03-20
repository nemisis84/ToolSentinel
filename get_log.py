import pandas as pd
from logger.logger import Logger

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