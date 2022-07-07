# %%
import streamlit as st
import plotly as px
import seaborn as sns
import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl as op
from datetime import date,datetime,time,timedelta

st.title('Personal Finance')

status = pd.read_excel (r'E:/Administration/Life.xlsx', sheet_name='Status')
expenses = pd.read_excel (r'E:/Administration/Life.xlsx', sheet_name='Expenses')
today=date.today()
todayformatted = datetime.today().strftime('%Y-%m-%d')

mortgagerate=st.sidebar.slider('Insert a Mortgage Rate', min_value=0.0, max_value=0.15, value=0.0449, step=0.001)
proratahours=st.sidebar.slider('Insert Hours Worked', min_value=0, max_value=38, value=32)

carloanrate=0.0679
ftehours=38
prorata=proratahours/ftehours

housevalue = 600000
carvalue = 65400
furniture = 70000
super = 210862.21

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

#Car Cost Caluculations
odometer = 22500
carpurchase = date(2020,9,30)
cartimeowned = (today-carpurchase).days/365
kmperyr = (odometer-335)/cartimeowned
fuelprice=2.3
fuelusage=10.2
fuelperyr = kmperyr/100*fuelusage # fuel used each year
fuelcostpa = fuelperyr*fuelprice # cost of fuel each year
carservmean = pd.DataFrame(data={336,552,457,776,378,714,885}).mean()
carservpa = carservmean*(kmperyr/10000) # $ of servicing per year
tyrecost = 1800     # $for all 4 replaced
tyrefreq = 30000    # in Kms
tyrepa = tyrecost*(kmperyr/30000)
insurancecar = 12*137.76
rego = 837.09
carpa = fuelcostpa+carservpa+tyrepa+insurancecar+rego
carthousandkm = carpa/kmperyr*1000
businesscarcap = 60733 # the 2022 cap for car owned for business
unidistance = 58.8 # distance to uni
unifreq = 2 # how many times a week i go to uni
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
rentalincome = 52*625

#Expenses
mortgagemin = 26 * 1028.04
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
haircuts = 52/6*32
rateswang = 4*203
waterwang = 4*200
unifees =  1720.14 
rentalmanagement = (rentalincome*0.09)*1.1
rentalannual = rentalincome*1.1/52
rentaladmin = 12*15*1.1
advertising = 220
maintenance = 615

expenses = expenses[['Date', 'Invest Prop.', 'Shopping', 'Home', 'Groceries',
       'Transport', 'Utilities', 'Health', 'Eating Out', 'Entertainment',
       'Cash', 'Travel', 'Education', 'Fees & Interest']]       
expenses=expenses[14:]
expenses = expenses.reset_index(drop=True)

lifeexpenses = expenses[len(expenses.index)-12:len(expenses.index)-1]
lifeexpenses = lifeexpenses[['Groceries','Eating Out','Entertainment','Cash','Fees & Interest']]
lifeexpenses = lifeexpenses.mean().sum()*12

#Tax stuff
capitalworks = 9420
capitalallowances = 1631 

businessinternet = 0.5 * telstra
wfhdays = 199
wfhfixedrate = 0.52 * wfhdays
wfhcost = businessinternet+wfhfixedrate

extradeduction=1000

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

st.text(int(totaldeductions))
st.text(int(totalincome))
st.text(int(taxableincome))
st.text(int(taxowed))
st.text(int(taxpaid))
st.text(int(taxreturn))
st.text(int(inpocketincome))

st.text("Saving Potential")
st.text(int(savingpotential))




