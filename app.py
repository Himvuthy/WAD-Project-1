import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="EduRisk Analytics - Lab 05",
    page_icon="🎓",
    layout="wide"
)

# NOTE: Custom CSS — change font to Inter and add rounded corners
# to all interactive elements (buttons, inputs, selects, dataframes, etc.)
st.markdown("""
<style>
/* NOTE: Import Inter font from Google Fonts for a modern clean look */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* NOTE: Apply Inter font globally to all Streamlit elements */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* NOTE: Round the corners on dataframe containers */
div[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

/* NOTE: Round the corners on select-box dropdowns */
div[data-testid="stSelectbox"] > div > div {
    border-radius: 12px !important;
}

/* NOTE: Round the corners on text inputs */
div[data-testid="stTextInput"] input {
    border-radius: 12px !important;
}

/* NOTE: Round the corners on number inputs */
div[data-testid="stNumberInput"] input {
    border-radius: 12px !important;
}

/* NOTE: Round the corners on alert boxes (success, info, warning, error) */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* NOTE: Round the corners on form containers */
div[data-testid="stForm"] {
    border-radius: 16px !important;
}

/* NOTE: Round the corners on bordered containers (like the filter card) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px !important;
}

/* NOTE: Round the corners on chart containers */
div[data-testid="stVegaLiteChart"] {
    border-radius: 16px;
    overflow: hidden;
}

/* NOTE: Change the global accent/primary colour from orange to light purple */
:root {
    --primary-color: #a855f7 !important;
}

/* NOTE: Override Streamlit's default widget accent to light purple */
/* This affects sliders, checkboxes, radio fills, and focused inputs */
.stSlider [data-testid="stThumbValue"],
.stCheckbox input:checked ~ span,
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #a855f7 !important;
}

/* NOTE: Metric cards — add a visible rounded box that adapts to dark/light mode */
div[data-testid="stMetric"] {
    background-color: rgba(128, 128, 128, 0.05);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 16px;
    padding: 20px 16px;
}

/* NOTE: Make ALL buttons look like the 3rd reference image (solid indigo/purple, white text) */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    border-radius: 12px !important;
    background-color: #6366f1 !important; /* Indigo/purple matching the 3rd image */
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    font-weight: 600 !important;
    padding: 6px 24px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

/* NOTE: Ensure text inside buttons stays white regardless of theme */
.stButton > button *,
.stDownloadButton > button *,
.stFormSubmitButton > button * {
    color: #ffffff !important;
}

/* NOTE: Hover effect for all buttons */
.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #4f46e5 !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
}

/* NOTE: Style native sidebar navigation links */
a[data-testid="stSidebarNavLink"] {
    padding: 8px 12px !important;
    border-radius: 12px !important;
    margin: 1px 0 !important;
    border: 2px solid transparent !important;
    transition: all 0.15s ease !important;
}

a[data-testid="stSidebarNavLink"] span {
    font-weight: 600 !important;
}

a[data-testid="stSidebarNavLink"]:hover {
    background-color: rgba(168, 85, 247, 0.08) !important;
}

a[data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: rgba(168, 85, 247, 0.12) !important;
    border: 2px solid #a855f7 !important;
}

a[data-testid="stSidebarNavLink"][aria-current="page"] span {
    color: #a855f7 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

def load_student_data():
    csv_path = Path(__file__).resolve().with_name("students.csv")
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()


student_df = load_student_data()

def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)

if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []

def highlight_risk(value):
    if value == "High Risk":
        return "color: #ff4b4b; font-weight: bold"
    if value == "Medium Risk":
        return "color: #faca2b; font-weight: bold"
    if value == "Low Risk":
        return "color: #09ab3b; font-weight: bold"
    return ""


def page_home():
    st.title("🎓 EduRisk Analytics")
    st.subheader("Interactive Dashboard with Visualization and Filters")
    st.write("Welcome to Lab 05.")
    st.write(
        "In this lab, the app improves the Dashboard page using "
        "grouped summaries, interactive filters, Streamlit charts, and Plotly charts."
    )
    st.success("Lab 05 app is running successfully!")

def page_dashboard():
    st.title("Interactive Student Performance Dashboard")
    st.write(
        "Use filters to explore student performance by course, risk level, score, "
        "and attendance. The dashboard updates based on your selections."
    )

    with st.container(border=True):
        st.subheader("Dashboard Filters")
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

        with filter_col1:
            selected_course = st.selectbox(
                "Filter by Course",
                ["All"] + sorted(student_df["Course"].dropna().unique().tolist())
            )

        with filter_col2:
            selected_risk = st.selectbox(
                "Filter by Risk Level",
                ["All", "Low Risk", "Medium Risk", "High Risk"]
            )

        with filter_col3:
            min_score = st.slider("Min Score", 0, 100, 0)

        with filter_col4:
            min_attendance = st.slider("Minimum Attendance", 0, 100, 0)

    filtered_df = student_df.copy()
    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]
    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]
    filtered_df = filtered_df[
        (filtered_df["Score"] >= min_score)
        & (filtered_df["Attendance"] >= min_attendance)
    ]

    if filtered_df.empty:
        st.warning("No students match the selected filters. Please adjust the filters.")

    total_students = len(filtered_df)
    average_score = filtered_df["Score"].mean() if total_students else 0
    average_attendance = filtered_df["Attendance"].mean() if total_students else 0
    high_risk_students = int((filtered_df["Risk Level"] == "High Risk").sum())

    st.subheader("Filtered Dashboard Metrics")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("Students", total_students)
    with metric_col2:
        st.metric("Average Score", round(average_score, 2))
    with metric_col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")
    with metric_col4:
        st.metric("High Risk", high_risk_students)

    st.subheader("Course Summary")

    if total_students > 0:
        course_summary = filtered_df.groupby("Course").agg(
            Students=("Student Name", "count"),
            Average_Score=("Score", "mean"),
            Average_Attendance=("Attendance", "mean"),
            Average_Study_Hours=("Study Hours", "mean")
        ).reset_index()

        st.dataframe(course_summary.round(2), width="stretch", hide_index=True)
    else:
        st.info("No course summary available for the selected filters.")

    st.subheader("Risk Level Summary")

    if total_students > 0:
        risk_summary = filtered_df["Risk Level"].value_counts().reset_index()
        risk_summary.columns = ["Risk Level", "Students"]

        st.dataframe(risk_summary, width="stretch", hide_index=True)
    else:
        st.info("No risk summary available for the selected filters.")

    st.subheader("Streamlit Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Scores")

        if total_students > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.info("No score chart available.")

    with chart_col2:
        st.write("Students by Course")

        if total_students > 0:
            course_count = filtered_df["Course"].value_counts()
            st.bar_chart(course_count)
        else:
            st.info("No course count chart available.")

    st.subheader("Interactive Plotly Charts")

    plotly_col1, plotly_col2 = st.columns(2)

    with plotly_col1:
        st.write("Risk Level Distribution")

        if total_students > 0:
            risk_summary_chart = filtered_df["Risk Level"].value_counts().reset_index()
            risk_summary_chart.columns = ["Risk Level", "Students"]

            fig_risk = px.bar(
                risk_summary_chart,
                x="Risk Level",
                y="Students",
                color="Risk Level",
                title="Risk Level Distribution",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_risk, width="stretch")
        else:
            st.info("No risk distribution chart available.")

    with plotly_col2:
        st.write("Student Scores by Risk Level")

        if total_students > 0:
            fig_score = px.bar(
                filtered_df,
                x="Student Name",
                y="Score",
                color="Risk Level",
                title="Student Scores by Risk Level",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_score, width="stretch")
        else:
            st.info("No score chart available.")

    st.subheader("Filtered Student Records")
    show_data = st.checkbox("Show Filtered Dataset", True)
    if show_data:
        if total_students:
            st.dataframe(
                filtered_df.style.map(highlight_risk, subset=["Risk Level"]),
                width="stretch"
            )
            st.download_button(
                label="Download Filtered Data",
                data=filtered_df.to_csv(index=False),
                file_name="filtered_student_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No student records to display.")
    else:
        st.info("Filtered dataset is hidden.")

    st.warning(
        "Ethics Reminder: Visualizations should support students and guide "
        "academic support decisions, not label or punish students."
    )


def page_student_data():
    st.title("Student Data")
    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )
    st.subheader("Data Inspection")
    st.write("Rows and Columns:", student_df.shape)
    st.write("Column Names:")
    st.write(student_df.columns.tolist())
    total_students = len(student_df)
    average_score = student_df["Score"].mean() if total_students else 0
    average_attendance = student_df["Attendance"].mean() if total_students else 0
    high_risk_students = int((student_df["Risk Level"] == "High Risk").sum())

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("Total Students", total_students)
    with metric_col2:
        st.metric("Average Score", round(average_score, 2))
    with metric_col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")
    with metric_col4:
        st.metric("High Risk Students", high_risk_students)

    st.write("First 5 Rows:")
    st.dataframe(
        student_df.head().style.map(highlight_risk, subset=["Risk Level"]),
        width="stretch"
    )
    st.subheader("Full Student Dataset")
    st.dataframe(
        student_df.style.map(highlight_risk, subset=["Risk Level"]),
        width="stretch"
    )

def page_risk_checker():
    st.title("Single Student Risk Checker")
    st.write(
        "Enter student information to check risk level. "
        "The result is based on score and attendance."
    )
    st.info(
        "This tool is for academic support. Risk results should help students, "
        "not label or punish them."
    )
    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    if submitted:
        if input_name.strip() == "":
            st.warning("Please enter the student name.")
        else:
            risk_result = get_risk_level(input_score, input_attendance)
            result = {
                "Student Name": input_name.strip(),
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": risk_result
            }
            st.session_state["risk_history"].append(result)

            if risk_result == "Low Risk":
                st.success("Risk Level: Low Risk")
                st.write("Student appears on track.")
            elif risk_result == "Medium Risk":
                st.warning("Risk Level: Medium Risk")
                st.write("Monitor progress and provide guidance.")
            else:
                st.error("Risk Level: High Risk")
                st.write("Student may need additional support.")

            st.write("Student Name:", result["Student Name"])
            st.write("Score:", input_score)
            st.write("Attendance:", input_attendance)

    st.subheader("Recent Risk Checks")
    if st.session_state["risk_history"]:
        # Process clearing before rendering the table so it disappears immediately.
        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.success("Risk check history cleared.")

    if st.session_state["risk_history"]:
        history_df = pd.DataFrame(st.session_state["risk_history"])
        st.dataframe(
            history_df.style.map(highlight_risk, subset=["Risk Level"]),
            width="stretch"
        )
    else:
        st.info("No risk checks yet.")

    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )

def page_about():
    st.title("About")
    st.write("This app is part of Lab 05.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Visualization and Interactivity")
    st.info(
        "This version improves the Dashboard page using grouped summaries, "
        "interactive filters, Streamlit charts, and Plotly charts."
    )
    st.warning(
        "Ethics Reminder: Student performance visualizations should be used "
        "responsibly to support learning and student success."
    )


pg = st.navigation({
    "MAIN MENU": [
        st.Page(page_dashboard, title="Dashboard", icon=":material/tune:"),
        st.Page(page_student_data, title="Student Data", icon=":material/person:"),
        st.Page(page_risk_checker, title="Risk Checker", icon=":material/warning:"),
        st.Page(page_about, title="About", icon=":material/info:"),
        st.Page(page_home, title="Home", icon=":material/home:")
    ]
})
pg.run()
