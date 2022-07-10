import streamlit as st
import pandas as pd
from pytz import country_names
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder


@st.experimental_memo
def load_data():
    df = pd.read_excel (r'E:/Administration/Life.xlsx', sheet_name='Status')
    return df


@st.experimental_memo
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


def execute_query(conn, df_sel_row, table_name):
    if not df_sel_row.empty:
        conn.cursor().execute(
            "CREATE OR REPLACE TABLE "
            f"{table_name}(COUNTRY string, CAPITAL string, TYPE string)"
        )
        write_pandas(
            conn=conn,
            df=df_sel_row,
            table_name=table_name,
            database="STREAMLIT_DB",
            schema="PUBLIC",
            quote_identifiers=False,
        )

# The code below is for the title and logo.
st.set_page_config(page_title="Dataframe with editable cells", page_icon="💾", layout="wide")
st.image(
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/floppy-disk_1f4be.png",
    width=100,
)
df = load_data()
st.title("Dataframe with editable cells")
st.subheader("① Edit and select cells")
st.info("💡 Hold the `Shift` (⇧) key to select multiple rows at once.")
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=True, groupable=True)
gd.configure_selection(selection_mode="multiple", use_checkbox=True)
gridoptions = gd.build()
grid_table = AgGrid(
    df,
    gridOptions=gridoptions,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    theme="material",
)
sel_row = grid_table["selected_rows"]



st.subheader(" ② Check your selection")

df_sel_row = pd.DataFrame(sel_row)
csv = convert_df(df_sel_row)
if not df_sel_row.empty:
    st.write(df_sel_row)
st.download_button(
    label="Download to CSV",
    data=csv,
    file_name="results.csv",
    mime="text/csv",
)
