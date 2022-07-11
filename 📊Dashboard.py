from dataclasses import fields
from pickle import FALSE
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl as op
from datetime import date,datetime,time,timedelta

st.set_page_config(layout="wide", page_icon="📊", menu_items={
         'Get Help': 'https://github.com/MichaelJenningsAI/personalfinance',
         'Report a bug': "https://github.com/MichaelJenningsAI/personalfinance/issues",
         'About': "Made by Michael Jennings"
     }
 )
st.sidebar.title('Personal Budget Model')

@st.experimental_memo
def load_data(input):
    df = pd.read_excel (r'E:/Administration/Life.xlsx', sheet_name=input)
    return df

status = load_data("Status")
expenses = load_data("Expenses")
today=date.today()
todayformatted = datetime.today().strftime('%Y-%m-%d')

#####Sidebar Variables####
ftesalary=(st.sidebar.slider('Full Time Salary', min_value=0, max_value=500000, value=107110, step=100))
mortgagerate=(st.sidebar.slider('Mortgage Rate %', min_value=0.01, max_value=20.0, value=4.49, step=0.01))/100
proratahours=st.sidebar.slider('Pro-rata Hours', min_value=0, max_value=38, value=32)
fuelprice=st.sidebar.slider('Fuel Price', min_value=1.0, max_value=3.0, value=2.3, step=0.01)
#####End Sidebar Variables####


with st.expander("University Related", expanded=False):
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Return trip to Uni (KM)</p></b>', unsafe_allow_html=True)
       with col2:
              unidistance = st.number_input('Value', min_value=0, max_value=200, value=59, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Uni Trips per week</p></b>', unsafe_allow_html=True)
       with col2:
              unifreq = st.number_input("Value", min_value=0, max_value=7, value=2, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Uni Fees</p></b>', unsafe_allow_html=True)
       with col2:
              unifees = st.number_input("Value", min_value=0.0, max_value=5000.0, value=1720.14, step=0.01)*2
       with col3:
              unifeesfreq = st.selectbox('Uni Fees Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=4)
       with col4:
              unifeesdate = st.date_input("Uni Fees Last Date", datetime(2022, 3, 10))
       ###########End Field###############



with st.expander("Car Related", expanded=False):
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Car Value</p></b>', unsafe_allow_html=True)
       with col2:
              carvalue = st.number_input('Value', min_value=0, max_value=100000, value=65400, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Odometer</p></b>', unsafe_allow_html=True)
       with col2:
              odometer = st.number_input("Value", min_value=0, max_value=250000, value=22500, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Registration</p></b>', unsafe_allow_html=True)
       with col2:
              rego = st.number_input("Value", min_value=0, max_value=1000, value=837, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Fuel Usage Rate</p></b>', unsafe_allow_html=True)
       with col2:
              fuelusage = st.number_input("Value", min_value=0.0, max_value=25.0, value=10.2, step=.01)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Tyre Cost (Full Set)</p></b>', unsafe_allow_html=True)
       with col2:
              tyrecost = st.number_input("Value", min_value=0, max_value=2000, value=1800, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Tyre Replacement KMs</p></b>', unsafe_allow_html=True)
       with col2:
              tyrefreq = st.number_input("Value", min_value=0, max_value=30000, value=30000, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Car Insurance</p></b>', unsafe_allow_html=True)
       with col2:
              insurancecar = st.number_input("Value", min_value=0.0, max_value=1000.0, value=137.76, step=0.01)*12
       with col3:
              insurancecarfreq = st.selectbox('Car Insurance Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=2)
       with col4:
              insurancecardate = st.date_input("Car Insurance Last Date", datetime(2022, 6, 24))
       #?##########End Field###############


with st.expander("Investment Home Related", expanded=False):
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Advertising Costs</p></b>', unsafe_allow_html=True)
       with col2:
              advertising = st.number_input("Value", min_value=0, max_value=300, value=220, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Capital Works</p></b>', unsafe_allow_html=True)
       with col2:
              capitalworks = st.number_input("Value", min_value=0, max_value=10000, value=9420, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Capital Allowances</p></b>', unsafe_allow_html=True)
       with col2:
              capitalallowances = st.number_input("Value", min_value=0, max_value=10000, value=1631, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Rental Income</p></b>', unsafe_allow_html=True)
       with col2:
              rentalincome = st.number_input('Value', min_value=0, max_value=1000, value=625, step=25)*52
       with col3:
              rentalincomefreq = st.selectbox('Rental Income Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=0)
       with col4:
              rentalincomedate = st.date_input("Rental Income Date", datetime(2022, 6, 30))
       ###########End Field###############
       ###########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Building Insurance</p></b>', unsafe_allow_html=True)
       with col2:
              insurancebuilding = st.number_input("Value", min_value=0.0, max_value=200.0, value=128.6, step=0.01)*12
       with col3:
              insurancebuildingfreq = st.selectbox('Building Insurance Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=2)
       with col4:
              insurancebuildingdate = st.date_input("Building Insurance Last Date", datetime(2022, 6, 23))
       #?##########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Zuccoli Rates</p></b>', unsafe_allow_html=True)
       with col2:
              rateszucc = st.number_input("Value", min_value=0.0, max_value=500.0, value=434.0, step=0.01)*4
       with col3:
              rateszuccfreq = st.selectbox('Zuccoli Rates Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=3)
       with col4:
              rateszuccdate = st.date_input("Zuccoli Rates Date", datetime(2022, 3, 30))
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Zuccoli Water</p></b>', unsafe_allow_html=True)
       with col2:
              waterzucc = st.number_input("Value", min_value=0.0, max_value=500.0, value=386.75, step=0.01)*4
       with col3:
              waterzuccfreq = st.selectbox('Zuccoli Water Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=3)
       with col4:
              waterzuccdate = st.date_input("Zuccoli Water Date", datetime(2022, 6, 17))
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Landlord Insurance</p></b>', unsafe_allow_html=True)
       with col2:
              insurancelandlord = st.number_input("Value", min_value=0.0, max_value=300.0, value=232.84, step=0.01)
       with col3:
              insurancelandlordfreq = st.selectbox('Landlord Insurance Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=5)
       with col4:
              insurancelandlorddate = st.date_input("Landlord Insurance Last Date", datetime(2021, 9, 4))
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Maintenance</p></b>', unsafe_allow_html=True)
       with col2:
              maintenance = st.number_input("Value", min_value=0.0, max_value=1000.0, value=615.0, step=0.01)
       with col3:
              maintenancefreq = st.selectbox('Maintenance Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=5)
       with col4:
              maintenancedate = st.date_input("Maintenance Last Date", datetime(2022, 7, 1))
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Rental Admin</p></b>', unsafe_allow_html=True)
       with col2:
              rentaladmin = st.number_input("Value", min_value=0.0, max_value=50.0, value=15.0, step=0.01)*1.1
       with col3:
              rentaladminfreq = st.selectbox('Rental Admin Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=5)
       with col4:
              rentaladmindate = st.date_input("Rental Admin Last Date", datetime(2022, 6, 30))
       ###########End Field###############


with st.expander("Bills", expanded=False):
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Rent</p></b>', unsafe_allow_html=True)
       with col2:
              rent = st.number_input('Value', min_value=0, max_value=1000, value=200, step=25)*52
       with col3:
              rentfreq = st.selectbox('Rent Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=0)
       with col4:
              rentdate = st.date_input("Rent Date", datetime(2022, 7, 11))
       ###########End Field###############
       ###########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Contents Insurance</p></b>', unsafe_allow_html=True)
       with col2:
              insurancecontents = st.number_input("Value", min_value=0.0, max_value=100.0, value=42.74, step=0.01)*12
       with col3:
              insurancecontentsfreq = st.selectbox('Contents Insurance Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=2)
       with col4:
              insurancecontentsdate = st.date_input("Contents Insurance Last Date", datetime(2022, 6, 23))
       #?##########End Field###############
       ###########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Health Insurance</p></b>', unsafe_allow_html=True)
       with col2:
              insuracehealth = st.number_input("Value", min_value=0.0, max_value=300.0, value=137.46, step=0.01)*12
       with col3:
              insuracehealthfreq = st.selectbox('Health Insurance Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=2)
       with col4:
              insuracehealthdate = st.date_input("Health Insurance Last Date", datetime(2022, 6, 28))
       #?##########End Field###############
       ###########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Telstra</p></b>', unsafe_allow_html=True)
       with col2:
              telstra = st.number_input("Value", min_value=0.0, max_value=300.0, value=166.0, step=0.01)*12
       with col3:
              telstrafreq = st.selectbox('Telstra Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=2)
       with col4:
              telstradate = st.date_input("Telstra Last Date", datetime(2022, 6, 22))
       ###########End Field###############
       ###########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Hair Cuts</p></b>', unsafe_allow_html=True)
       with col2:
              haircuts = st.number_input("Value", min_value=0.0, max_value=50.0, value=32.0, step=0.01)*52/6
       with col3:
              haircutsfreq = st.selectbox('Hair Cut  Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=2)
       with col4:
              haircutsdate = st.date_input("Hair Cut Last Date", datetime(2022, 5, 27))
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Power</p></b>', unsafe_allow_html=True)
       with col2:
              power = st.number_input("Value", min_value=0.0, max_value=1000.0, value=400.0, step=0.01)*4
       with col3:
              powerfreq = st.selectbox('Power Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=3)
       with col4:
              powerdate = st.date_input("Power Date", datetime(2022, 6, 1))
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Rates Wangi</p></b>', unsafe_allow_html=True)
       with col2:
              rateswang = st.number_input("Value", min_value=0.0, max_value=500.0, value=203.0, step=0.01)*4
       with col3:
              rateswangfreq = st.selectbox('Rates Wangi Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=3)
       with col4:
              rateswangdate = st.date_input("Rates Wangi Date", datetime(2022, 5, 31))
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Water Wangi</p></b>', unsafe_allow_html=True)
       with col2:
              waterwang = st.number_input("Value", min_value=0.0, max_value=500.0, value=200.0, step=0.01)*4
       with col3:
              waterwangfreq = st.selectbox('Water Wangi Frequency',('Weekly', 'Fortnightly', 'Monthly', 'Quarterly', 'Biannually', 'Annually'), index=3)
       with col4:
              waterwangdate = st.date_input("Water Wangi Date", datetime(2022, 6, 1))
       ###########End Field###############

with st.expander("Assets", expanded=False):
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">House Value</p></b>', unsafe_allow_html=True)
       with col2:
              housevalue = st.number_input("Value", min_value=0, max_value=1000000, value=600000, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Furniture Value</p></b>', unsafe_allow_html=True)
       with col2:
              furniture = st.number_input("Value", min_value=0, max_value=100000, value=70000, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Super</p></b>', unsafe_allow_html=True)
       with col2:
              super = st.number_input("Value:", min_value=0, max_value=1000000, value=210862, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############


with st.expander("Business Deductions", expanded=False):
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Extra Deductions</p></b>', unsafe_allow_html=True)
       with col2:
              extradeduction = st.number_input('Value', min_value=0, max_value=10000, value=1000, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">WFH Days</p></b>', unsafe_allow_html=True)
       with col2:
              wfhdays = st.number_input('Value', min_value=0, max_value=365, value=199, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
       #?##########Field###############
       col1, col2, col3, col4 = st.columns(4)
       with col1:
              st.text("")
              st.markdown('<b><p style="color:Black;font-size:20px;text-align:Right;">Telstra Business %</p></b>', unsafe_allow_html=True)
       with col2:
              businessinternetpercent = st.number_input('Value', min_value=0, max_value=100, value=50, step=1)
       with col3:
              st.text("")
       with col4:
              st.text("")
       ###########End Field###############
      


#Entered Variables
businesscarcap = 60733 # the 2022 cap for car owned for business
ftehours=38
gym = 0
carloanrate=0.0679
#Caluculations
carloanmin = ((60265.26*(carloanrate/12)*((1+(carloanrate/12))**(12*7)))/((1+(carloanrate/12))**(12*7)-1))*12
mortgagemin = ((460346.22*(mortgagerate/12)*((1+(mortgagerate/12))**(12*27.5)))/((1+(mortgagerate/12))**(12*27.5)-1))*12
prorata=proratahours/ftehours
businessinternet = businessinternetpercent/100 * telstra

status = status[['Date', 'Account 1', 'Account 2',
       'Account 3', 'Account 4', 'Crypto', 'Shares Account', 'Shares',
       'Car Loan', 'Home Loan']]
status = status[status['Date'] < todayformatted]
status = status[status['Date'] > '2020-09-22']
status = status.reset_index(drop=True)

status['Equity'] = status['Account 1'] + status['Account 2'] + status['Account 3'] + status['Account 4'] + status['Crypto'] + status['Shares Account'] + status['Shares']
status['Debt'] = status['Car Loan'] + status['Home Loan']
status['Net Worth'] = status['Equity'] - status['Debt'] + housevalue + carvalue + furniture + super

networthrate = (status['Net Worth'][int(len(status.index)-1)] - status['Net Worth'][0])/len(status.index)

cash = status['Account 1'][int(len(status.index)-1)] + status['Account 2'][int(len(status.index)-1)] + status['Account 3'][int(len(status.index)-1)] + status['Shares Account'][int(len(status.index)-1)]
crypto = status['Crypto'][int(len(status.index)-1)]
shares = status['Shares'][int(len(status.index)-1)]
assetvalue = housevalue+carvalue+furniture+super+cash+crypto+shares

#Current Debts
mortgagecurrent = status['Home Loan'][int(len(status.index)-1)]
carloancurrent = status['Car Loan'][int(len(status.index)-1)]
debtvalue = mortgagecurrent+carloancurrent

#Current Networth
networth=assetvalue-debtvalue

carpurchase = date(2020,9,30)
cartimeowned = (today-carpurchase).days/365
kmperyr = (odometer-335)/cartimeowned
fuelperyr = kmperyr/100*fuelusage # fuel used each year
fuelcostpa = fuelperyr*fuelprice # cost of fuel each year
carservmean = pd.DataFrame(data={336,552,457,776,378,714,885}).mean()
carservpa = carservmean*(kmperyr/10000) # $ of servicing per year
tyrepa = tyrecost*(kmperyr/30000)
carpa = fuelcostpa+carservpa+tyrepa+insurancecar+rego
carthousandkm = carpa/kmperyr*1000
unikms = unidistance * unifreq * 26 # 26 weeks in 2 semesters
unicarperc = unikms/kmperyr # percentage use of car for uni
unicarrc = unicarperc * carpa # car running cost for uni
cardep = (businesscarcap*.75**(int(round(cartimeowned))-1))-(businesscarcap*.75**int(round(cartimeowned))) # car depreciation this fy
unicardep = cardep*unicarperc # car depreciation for uni
unicarcost = unicarrc+unicardep

#Incomes
pretaxsalary = ftesalary*prorata
bonus = 0.07*pretaxsalary*prorata
pension = 26*6.4
totalincome = pretaxsalary+pension+bonus+rentalincome

if int((pretaxsalary+bonus)) > 180000:      
       taxpaid = (int((pretaxsalary+bonus))-180000)*0.45+51667
if int((pretaxsalary+bonus)) <= 180000:
       taxpaid = (int((pretaxsalary+bonus))-120000)*0.37+29467
if int((pretaxsalary+bonus)) <= 120000:
       taxpaid = (int((pretaxsalary+bonus))-45000)*0.325+5092
if int((pretaxsalary+bonus)) <= 45000:
       taxpaid = (int((pretaxsalary+bonus))-18200)*0.19
if int((pretaxsalary+bonus)) <= 18200:
       taxpaid = 0

aftertaxincome = pretaxsalary+bonus+pension-taxpaid
superpa=(pretaxsalary+bonus)*.105
#Expenses

rentalmanagement = (rentalincome*0.09)*1.1
rentalannual = rentalincome*1.1/52

expenses = expenses[['Date', 'Invest Prop.', 'Shopping', 'Home', 'Groceries',
       'Transport', 'Utilities', 'Health', 'Eating Out', 'Entertainment',
       'Cash', 'Travel', 'Education', 'Fees & Interest']]       
expenses=expenses[14:]
expenses = expenses.reset_index(drop=True)

lifeexpenses = expenses[len(expenses.index)-12:len(expenses.index)-1]
lifeexpenses = lifeexpenses[['Groceries','Eating Out','Entertainment','Cash','Fees & Interest']]
lifeexpenses = lifeexpenses.mean().sum()*12

#Tax stuff
wfhfixedrate = wfhdays/5*38*0.52
wfhcost = businessinternet+wfhfixedrate

#Tax Calculations
mortgageinterest = mortgagecurrent*mortgagerate
totaldeductions = rateszucc+waterzucc+rentalmanagement+rentalannual+rentaladmin+advertising+maintenance+mortgageinterest+insurancebuilding+insurancelandlord+capitalworks+capitalallowances+wfhcost+extradeduction+unicarcost+unifees
taxableincome = totalincome - totaldeductions

if int(taxableincome) > 180000:      
       taxowed = (taxableincome-180000)*0.45+51667
if int(taxableincome) <= 180000:
       taxowed = (taxableincome-120000)*0.37+29467
if int(taxableincome) <= 120000:
       taxowed = (taxableincome-45000)*0.325+5092
if int(taxableincome) <= 45000:
       taxowed = (taxableincome-18200)*0.19
if int(taxableincome) <= 18200:
       taxowed = 0
if int(taxableincome) <= 0:
       taxableincome=0

taxreturn = taxpaid - taxowed
rentalinpocket = rentalincome-rentalmanagement-rentalannual-rentaladmin-advertising-maintenance
inpocketincome = aftertaxincome+rentalinpocket+taxreturn
lifeexpenses = mortgagemin+carloanmin+insurancebuilding+insurancecontents+insurancelandlord+insuracehealth+rateszucc+waterzucc+rent+telstra+power+gym+haircuts+rateswang+waterwang+unifees+lifeexpenses+carpa
savingpotential=inpocketincome-lifeexpenses

#All fields Chart
data = {'Fields':['Total Income','Taxable Income','Tax Return','Inpocket Income','Super','Expenses','Total Deductions','Tax Owed','Tax Paid','Saving Potential',]
       ,'Values':[int(totalincome),int(taxableincome),int(taxreturn),int(inpocketincome),int(superpa),int(lifeexpenses),int(totaldeductions),int(taxowed),int(taxpaid),int(savingpotential)]
       ,'Category':['Income','Income','Income','Income','Income','Expense','Expense','Expense','Expense','Estimation']}
input = pd.DataFrame(data)
fig = px.bar(input, x='Fields', y='Values', color='Category')
#fig.update_layout(yaxis_range=[0,150000])
st.plotly_chart(fig, use_container_width=True)

#Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Savings", '$' + str(int(savingpotential)), str(int(int(savingpotential)/int(totalincome)*100)) + '%')
col2.metric("Expenses", '$' + str(int(lifeexpenses)), str(int(int(lifeexpenses)/int(totalincome)*100)) + '%', delta_color="inverse")
col3.metric("Tax", '$' + str(int(taxowed)), str(int(int(taxowed)/int(totalincome)*100)) + '%', delta_color="inverse")

col1, col2 = st.columns(2)
with col1:
       #Pie Chart
       data = {'Fields':['Expenses','Saving Potential','Tax Owed']
              ,'Values':[int(lifeexpenses),int(savingpotential),int(taxowed)]}
       input = pd.DataFrame(data)
       fig = px.pie(input, values='Values', names='Fields')
       st.plotly_chart(fig, use_container_width=True)
       
with col2:
       #Stacked Chart
       x = ['Value']
       fig = go.Figure(data=[go.Bar(name='Income',x = x, y = [int(inpocketincome)]),go.Bar(name = 'Super',x = x,y = [int(superpa)]),go.Bar(name = 'Tax',x = x,y = [int(taxowed)])])
       fig.update_layout(barmode='stack')
       #fig.update_layout(yaxis_range=[0,200000])
       st.plotly_chart(fig, use_container_width=True)