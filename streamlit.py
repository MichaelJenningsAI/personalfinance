# %%
from pickle import FALSE
import streamlit as st
import plotly.express as px
import seaborn as sns
import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl as op
from datetime import date,datetime,time,timedelta

st.sidebar.title('Personal Budget Model')



status = pd.read_excel (r'E:/Administration/Life.xlsx', sheet_name='Status')
expenses = pd.read_excel (r'E:/Administration/Life.xlsx', sheet_name='Expenses')
today=date.today()
todayformatted = datetime.today().strftime('%Y-%m-%d')


#Adjustable Variables
mortgagerate=(st.sidebar.slider('Mortgage Rate %', min_value=0.01, max_value=15.0, value=4.49, step=0.01))/100
proratahours=st.sidebar.slider('Pro-rata Hours', min_value=0, max_value=38, value=32)
fuelprice=st.sidebar.slider('Fuel Price', min_value=1.0, max_value=3.0, value=2.3)


#Entered Variables
housevalue = 600000
carvalue = 65400
furniture = 70000
super = 210862.21
odometer = 22500



insurancecar = 12*137.76
rego = 837.09
unifreq = 2 # how many times a week i go to uni
rentalincome = 52*625

carloanmin = 12 * 903.39
insurancebuilding = 12*128.6
insurancecontents = 12*42.74
insurancelandlord = 232.84
insuracehealth = 12*137.46
rateszucc = 4*434
waterzucc = 1547
rent = 52*200
telstra = 12*166
power = 4*400
gym = 0
unifees =  1720.14 
maintenance = 615
wfhdays = 199
extradeduction=1000

#Fixed Values
fuelusage=10.2
tyrecost = 1800     # $for all 4 replaced
carloanrate=0.0679
ftehours=38
tyrefreq = 30000    # in Kms
businesscarcap = 60733 # the 2022 cap for car owned for business
unidistance = 58.8 # distance to uni
haircuts = 52/6*32
rateswang = 4*203
waterwang = 4*200
rentaladmin = 12*15*1.1
advertising = 220
capitalworks = 9420
capitalallowances = 1631

#Caluculations
mortgagemin = ((460346.22*(mortgagerate/12)*((1+(mortgagerate/12))**(12*27.5)))/((1+(mortgagerate/12))**(12*27.5)-1))*12
prorata=proratahours/ftehours

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
pretaxsalary = 107110.5*prorata
bonus = 0.07*pretaxsalary*prorata
salary = pretaxsalary-(((pretaxsalary)-45000)*0.325+5092)
pension = 26*6.4
aftertaxincome = salary+pension+salary*0.07

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
businessinternet = 0.5 * telstra
wfhfixedrate = 0.52 * wfhdays
wfhcost = businessinternet+wfhfixedrate

#Tax Calculations
mortgageinterest = mortgagecurrent*mortgagerate
totaldeductions = rateszucc+waterzucc+rentalmanagement+rentalannual+rentaladmin+advertising+maintenance+mortgageinterest+insurancebuilding+insurancelandlord+capitalworks+capitalallowances+wfhcost+extradeduction+unicarcost+unifees
totalincome = pretaxsalary+pension+bonus+rentalincome
taxableincome = totalincome - totaldeductions
taxowed = (taxableincome-45000)*0.325+5092
taxpaid = ((pretaxsalary+bonus)-45000)*0.325+5092
taxreturn = taxpaid - taxowed
rentalinpocket = rentalincome-rentalmanagement-rentalannual-rentaladmin-advertising-maintenance
inpocketincome = aftertaxincome+rentalinpocket+taxreturn
lifeexpenses = mortgagemin+carloanmin+insurancebuilding+insurancecontents+insurancelandlord+insuracehealth+rateszucc+waterzucc+rent+telstra+power+gym+haircuts+rateswang+waterwang+unifees+lifeexpenses+carpa
savingpotential=inpocketincome-lifeexpenses


data = {'Fields':['Total Income','Taxable Income','Tax Return','Inpocket Income','Life Expenses','Total Deductions','Tax Owed','Tax Paid','Saving Potential',]
       ,'Values':[int(totalincome),int(taxableincome),int(taxreturn),int(inpocketincome),int(lifeexpenses),int(totaldeductions),int(taxowed),int(taxpaid),int(savingpotential)]
       ,'Colours':['Income','Income','Income','Income','Expense','Expense','Expense','Expense','Output']}

input = pd.DataFrame(data)
fig = px.bar(input, x='Fields', y='Values', color='Colours')
fig.update_layout(yaxis_range=[0,150000])
st.plotly_chart(fig, use_container_width=True)

st.markdown('<b><p style="color:blue;font-size:20px;text-align:center;">Saving Potential: $'+ str(int(savingpotential))+'</p></b>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
       st.markdown('<b><p style="color:green;font-size:20px;text-align:center;">Total Income: $'+str(int(totalincome))+'</p></b>', unsafe_allow_html=True)
       st.markdown('<b><p style="color:green;font-size:20px;text-align:center;">Taxable Income: $'+str(int(taxableincome))+'</p></b>', unsafe_allow_html=True)
       st.markdown('<b><p style="color:green;font-size:20px;text-align:center;">Tax Return: $'+str(int(taxreturn))+'</p></b>', unsafe_allow_html=True)
       st.markdown('<b><p style="color:green;font-size:20px;text-align:center;">Inpocket Income: $'+str(int(inpocketincome))+'</p></b>', unsafe_allow_html=True)
with col2:
       st.markdown('<b><p style="color:red;font-size:20px;text-align:center;">Total Deductions: $'+str(int(totaldeductions))+'</p></b>', unsafe_allow_html=True)
       st.markdown('<b><p style="color:red;font-size:20px;text-align:center;">Tax Owed: $' + str(int(taxowed)) +'</p></b>', unsafe_allow_html=True)
       st.markdown('<b><p style="color:red;font-size:20px;text-align:center;">Tax Paid: $' + str(int(taxpaid)) + '</p></b>', unsafe_allow_html=True)
# %%