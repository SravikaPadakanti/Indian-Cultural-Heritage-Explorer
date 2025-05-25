import streamlit as st

# Display Snowflake credentials from secrets.toml
st.write("Snowflake User:", st.secrets["snowflake"]["user"])
st.write("Snowflake Account:", st.secrets["snowflake"]["account"])
st.write("Snowflake Warehouse:", st.secrets["snowflake"]["warehouse"])
st.write("Snowflake Database:", st.secrets["snowflake"]["database"])
st.write("Snowflake Schema:", st.secrets["snowflake"]["schema"])