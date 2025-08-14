import streamlit as st
import datetime
import pandas as pd

st.title("📚 Personalized Study Planner")

# Store data in session
if "subjects" not in st.session_state:
    st.session_state.subjects = []

# Step 1: Number of subjects
num_subjects = st.number_input("Enter number of subjects:", min_value=1, step=1)

# Step 2: Collect subject names and dates
for i in range(num_subjects):
    if len(st.session_state.subjects) <= i:
        st.session_state.subjects.append({"name": "", "date": None})

    sub_name = st.text_input(f"Enter name of subject {i+1}", value=st.session_state.subjects[i]["name"], key=f"name_{i}")
    exam_date = st.date_input(
        f"Enter exam date for {sub_name or 'Subject ' + str(i+1)}",
        value=st.session_state.subjects[i]["date"] or datetime.date.today(),
        key=f"date_{i}"
    )

    st.session_state.subjects[i]["name"] = sub_name
    st.session_state.subjects[i]["date"] = exam_date

# Step 3: Generate timetable
if st.button("Generate Study Plan"):
    today = datetime.date.today()
    plan = []

    # Create a list of days for each subject until exam
    for sub in sorted(st.session_state.subjects, key=lambda x: x["date"]):
        days_left = (sub["date"] - today).days
        for d in range(days_left):
            date = today + datetime.timedelta(days=d)
            plan.append({"Date": date.strftime("%Y-%m-%d"), "Subject": sub["name"]})

    # Distribute subjects evenly
    df = pd.DataFrame(plan)
    st.subheader("📅 Your Day-by-Day Study Plan")
    st.dataframe(df)


