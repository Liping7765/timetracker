import streamlit as st 
import time 
from database.database import Database
from datetime import datetime as dt

# GENERAL CONSTANTS
catagories = ["WORKOUT", "STUDY", "FAMALY TIME"]

def ending_progress(seconds):
        placeholder = st.empty()
        my_bar = placeholder.progress(0)

        for percent_complete in range(100):
            time.sleep(seconds / 100 * 1.0)
            my_bar.progress(percent_complete + 1)

        placeholder.empty()



def show_time(start_time, end_time):

    start = dt.fromtimestamp(int(start_time))
    end = dt.fromtimestamp(int(end_time))
    return str(end - start)

def metric():
    db = Database()
    rows = db.get_all()

    left_time= 80 * 60 * 60 
    prev_catup = 0
    total_catup = 0
    for row in rows:
        id, cat, start, end, _ = row
        prev_catup = total_catup
        total_catup += end - start if cat != "WORKOUT" else (end - start) * 2


    value, delta = str(show_time(total_catup, left_time)), str(int(total_catup - prev_catup)) + " secs"
    st.metric(label="Time to catch up...", value=value, delta=delta)





# side bar to starting and ending timer 
with st.sidebar:
    metric()
    st.selectbox("Choose your activity here...", options=catagories, key="catagory")
    st.button(" ________START__________", key="start")
    st.button("_________END___________", key = "end")
    


if st.session_state["start"]:

    if 'start_time' not in st.session_state:
        st.session_state["start_time"] = time.time()
    st.text('Starting the timer..')
    ending_progress(1.0)



if st.session_state["end"]:

    if 'end_time' not in st.session_state:
        st.session_state['end_time'] = time.time()
    st.text("Ending the timer...")
    

    end_time = (st.session_state["end_time"])
     
    start_time = (st.session_state['start_time'])
    cat = st.session_state['catagory']

    # a = st.text_input("category", value=cat, disabled=disabled) 
    # b = st.text_input("started at",value=start_time, disabled=disabled)
    # c = st.text_input("ended at",value=end_time, disabled=disabled)
    duration = dt.fromtimestamp(st.session_state["end_time"]) - dt.fromtimestamp(st.session_state['start_time'])

    st.text(f"""You did {cat} between {time.ctime(start_time)} and {time.ctime(end_time)}.
Duration of {duration} in seconds.""")
    
    
    db = Database()
    db.add_record(cat, start_time, end_time)
    del st.session_state['start_time']
    del st.session_state['end_time']

    time.sleep(5)
    st.experimental_rerun()

    


# db = Database()

# start = time.time()
# time.sleep(2)
# end = time.time()


# st.write(result2 - result1)

# import time




# st.balloons()

# db = Database()

# t = time.time()

# st.write(decimal.Decimal(t))


# rows = db.get_all()

# st.write(rows[-1][2])
# st.write(float(rows[-1][2]) - time.time())




# # input datetime

# time1 = datetime.fromtimestamp(time.time())

# time.sleep(2)
# time2 = datetime.fromtimestamp(time.time())

# print(time2 - time1)