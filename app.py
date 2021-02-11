import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

df1 = pd.read_csv('SMEs Survey Data.csv')

context      = df1.columns[0:20]
use          = df1.columns[20:29]
potential    = df1.columns[29:]

potential_df = df1[potential]
use_df       = df1[use]
context_df   = df1[context]

df2          = pd.read_excel('book1.xlsx')
df2          = df2[df2['country'] == 'ID']
dfcoba       = df2.groupby('question').sum()
question     = list(dfcoba.index)

techFac = context_df[context_df.columns[1:]]
techFac = techFac.drop(['O_PROAC_4','E_ENV_6'],axis = 1)

challenges                           = df2[df2['question'] == 'What are the two most important challenges your business currently faces?']
ordering_via_ecommerce               = df2[df2['question'] == 'Did your business order products or services via e-commerce during the last 12 months?']
receive_order_via_ecommerce          = df2[df2['question'] == 'Did your business receive orders via e-commerce during the last 12 months?']
current_business_state               = df2[df2['question'] == 'How would you evaluate the current state of your business?']
sector                               = df2[df2['question'] == 'In which sector does your business operate?']
upskill                              = df2[df2['question'] == 'Over the past 12 months, have you undergone any training to improve your technology (such as internet or computer) skills?']
ecommerce_netsales                   = df2[df2['question'] == 'What is the share of e-commerce orders in your businessÕs net sales?']
expected_business_state              = df2[df2['question'] == 'What is your outlook for the next 6 months on your business?']
ecommerce_orders_within_home_country = df2[df2['question'] == 'What share of e-commerce orders by your business were placed within your home country?']
ecommerce_orders_received            = df2[df2['question'] == 'What share of e-commerce orders received by your business were from your home country?']
ecommerce_business_purchase          = df2[df2['question'] == 'What share of your businessÕs purchases are made through e-commerce?']
expected_thing_to_have               = df2[df2['question'] == 'Which two of the following would you most want your business to have?']
online_anxiety                       = df2[df2['question'] == 'Which two of these are you most concerned about when thinking about your business\'s activity online?']
ecommerce_customer_target            = df2[df2['question'] == 'Who does your business sell to via e-commerce?']
reason_starting_business             = df2[df2['question'] == 'Why did you start or join this business? Please select up to three reasons that are most important to you.']
foreign_market_challenge             = df2[df2['question'] == 'You said that Òselling to foreign marketsÓ is a challenge for your business. What particular challenges does this include?']

# dict for replacement

scale_dict = {
    1 : 'strongly disagree',
    2 : 'disagree',
    3 : 'neutral',
    4 : 'agree',
    5 : 'strongly agree'
}

usedict = {
    'COMM':'Communication ',
    'CUST':'Customer management',
    'FINMAN':'Financial management',
    'HRM':'Human resource management',
    'MARKET':'Marketing management',
    'ORSALE':'Order&sales',
    'PROD':'Production','PURINV':'Purchasing&inventory',
    'IEM':'Integrated enterprise management'
}

contextdict = {
    'O_MGTSUP_1':'Management Support',
    'O_BENEF_2':'Perceived Benefits',
    'O_INNO_3':'Innovativeness',
    'O_FIN_5':'Finacial Resource',
    'O_EXPERT_6':'E-business Expertise',
    'O_PROC_7':'Process Management',
    'T_COST_1':'Perceived Cost',
    'T_RISK_2':'Perceived Risk',
    'T_COMPAT_3':'Compatibiliy',
    'T_COMPLEX_4':'Complexity',
    'T_TRIAL_5':'Trialability',
    'T_OBSERV_6':'Observability',
    'E_FINSUP_1':'Financial Support',
    'E_GOV_2':'Government Suppoer',
    'E_VENDOR_3':'Vendor Support',
    'E_COMPRES_4':'Competitive Preasure',
    'E_INFRA_5':'Technology Infrastructure'
}

perfodict = {
    'OPERATION_1':'Productivity',
    'OPERATION_2':'Cost reduction',
    'OPERATION_3':'Product quality',
    'OPERATION_4':'Customer service',
    'TACMAN_1':'Resource management',
    'TACMAN_2':'Decision making',
    'TACMAN_3':'Performance control',
    'STRAT_1':'Business growth',
    'STRAT_2':'Competitive advantage',
    'STRAT_3':'Partner synergy',
    'STRAT_4':'Business innovation'
}

# dataframe manipulation function

def replace_column_labels(df,dictionary):
    numpang = pd.DataFrame({'kolom':df.columns})
    numpang['kolom'] = numpang['kolom'].replace(dictionary)
    df.columns = list(numpang['kolom'])
    return df

def replace_values(df,column_list,dictionary):
    df[column_list] = df[column_list].replace(dictionary)
    return df

techFac = replace_column_labels(techFac,contextdict)
eBusUse = replace_column_labels(use_df,usedict)
eBusPero = replace_column_labels(potential_df,perfodict)

techFac = replace_values(techFac,techFac.columns,scale_dict)
eBusUse = replace_values(eBusUse,eBusUse.columns,scale_dict)
eBusPero = replace_values(eBusPero,eBusPero.columns,scale_dict)

def WBneut_counts(df):
    neutanslist= ['Don\'t know or prefer not to say','Prefer not to say','Neutral','Don\'t know or prefer not to respond','Don\'t know/Prefer not to say']
    lenlist = []
    neutlist = []
    rasio = []

    for neut in neutanslist:
        totalneut = list(df[df['value'] == neut]['statistic'])
        neutlist = neutlist +totalneut
        lenght =list(df[df['value'] == neut]['total_asked'])
        lenlist = lenlist+lenght
    for i in neutlist:
        for j in lenlist:
            a = round(i/j*100)
        rasio.append(a)

    neutrata2 = sum(rasio)/len(rasio)
    return neutrata2

def UIneut_counts(df):
    neutralList = []
    for i in df.columns:
        total = df[i].value_counts()[3]
        neutralList.append(total)

    UIneut = sum(neutralList)/len(neutralList)/325*100
    return UIneut

# plotting function

def pie_neutral():
    # Pie chart
    labels1 = ['Neutral', 'Non-neutral']
    sizes1 = [UIneut_counts(df1)*360/100,360 - UIneut_counts(df1)*360/100]
    labels2 = ['Neutral', 'Non-neutral']
    sizes2 = [WBneut_counts(df2)*360/100,360 - WBneut_counts(df2)*360/100]
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = (0.1, 0)
    #add colors
    colors = ['#ff9999','#66b3ff']
    colorss = ['#99ff99','#ffcc99']
    fig1, ax = plt.subplots(1,2,figsize = (9,9))
    ax[0].pie(sizes1, explode=explode, labels=labels1, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax[1].pie(sizes2, explode=explode, labels=labels2, colors=colorss, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax[0].set_title('Universitas Indonesia')
    ax[1].set_title('World Bank')
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()

    st.pyplot(fig1)

def grouped_hist(df):    
    fig = px.histogram(df,barmode='group',histnorm = 'percent')
    st.plotly_chart(fig)
    
def challenge():    
    x = challenges['value']
    y = challenges['statistic']
    fig = px.histogram(challenges,x = y,y = x)
    fig.update_layout(margin=dict(l=510, r=0, t=0, b=0))
    st.plotly_chart(fig) 

def digital_anxiety():    
    x = online_anxiety['value']
    y = online_anxiety['statistic']
    fig = px.histogram(online_anxiety,x = y,y = x)
    fig.update_layout(margin=dict(l=100, r=0, t=0, b=0))
    st.plotly_chart(fig)
    
def expectation():
    x = expected_thing_to_have['value']
    y = expected_thing_to_have['statistic']
    fig = px.histogram(expected_thing_to_have,x = y,y = x)
    fig.update_layout(margin=dict(l=100, r=0, t=0, b=0))
    st.plotly_chart(fig)
    
def UpSkill():
    x = upskill['value']
    y = upskill['statistic']
    fig = px.histogram(upskill,x = y,y = x, height = 300)
    st.plotly_chart(fig)
    
def enetsales():    
    x = ecommerce_netsales['value']
    y = ecommerce_netsales['statistic']
    fig = px.histogram(ecommerce_netsales,x = y,y = x)
    fig.update_layout(margin=dict(l=80, r=0, t=0, b=0))
    st.plotly_chart(fig)
    
def online_target():
    x = ecommerce_customer_target['value']
    y = ecommerce_customer_target['statistic']
    fig = px.histogram(ecommerce_customer_target,x = y,y = x)
    st.plotly_chart(fig)
    
def orderingViaEcommerce():     
    x = ordering_via_ecommerce['value']
    y = ordering_via_ecommerce['statistic']
    fig = px.histogram(ordering_via_ecommerce,x = y,y = x)
    st.plotly_chart(fig)
    
def receiveOrderViaEcommerce():
    x = receive_order_via_ecommerce['value']
    y = receive_order_via_ecommerce['statistic']
    fig = px.histogram(receive_order_via_ecommerce,x = y,y = x)
    st.plotly_chart(fig)
    
def Sector():    
    x = sector['value']
    y = sector['statistic']
    fig = px.histogram(sector,x = y,y = x)
    fig.update_layout(margin=dict(l=650, r=0, t=0, b=0))
    st.plotly_chart(fig)

def eorderWithinHomeCountry():
    x = ecommerce_orders_within_home_country['value']
    y = ecommerce_orders_within_home_country['statistic']
    fig = px.histogram(ecommerce_orders_within_home_country,x = y,y = x)
    st.plotly_chart(fig)

def eordersreceived():    
    x = ecommerce_orders_received['value']
    y = ecommerce_orders_received['statistic']
    fig = px.histogram(ecommerce_orders_received,x = y,y = x)
    st.plotly_chart(fig)

def ebuspurchase():    
    x = ecommerce_business_purchase['value']
    y = ecommerce_business_purchase['statistic']
    fig = px.histogram(ecommerce_business_purchase,x = y,y = x)
    st.plotly_chart(fig)

def formarketchal():    
    x = foreign_market_challenge['value']
    y = foreign_market_challenge['statistic']
    fig = px.histogram(foreign_market_challenge,x = y,y = x)
    st.plotly_chart(fig)

wdywk1 = [
    'Select What You Want To Know',
    'challenge faced by SMEs',
    'orders by SMEs via E-commerce locally',
    'orders received by SMEs vie E-commerce from locals',
    'E-commerce order share in net sales',
    'SMEs sector share',
    'business owner undergone skill improvement training',
    'things owners would like their business to have',
    'concerns over SMEs business activities',
    'SMEs E-commerce customer target',
    'challenge faced by SMEs in entering foreign market',
    'SMEs E-commerce business purchase'
]

wdywk2 = [
    'Select What You Want To Know',
    'Contextual Factors',
    'E-business use',
    'E-business Performance Impact'

]


st.markdown('<h1 align = "center">SMEs Survey Data</h1>',unsafe_allow_html=True)
st.subheader('Summary')
st.markdown('<p align = "justify">Datas used in the analysis are the ones coming from two resources. The first data is taken from the World Bank Data Catalog which consist of 2019 survey of SMEs worldwide including 448 Indonesian SMEs. The second one is coming from a 2020 survey dataset of 325 Indonesian SMEs deposited to Mendeley by researchers from Universitas Indonesia.</p>',unsafe_allow_html = True) 
pie_neutral()
st.markdown('<p align = "justify">For a brief shape, the datas contains small amount of neutral answers or answers that suggest business owner prefers not to disclose the state of their business</p>',unsafe_allow_html = True)
st.markdown('<p align = "justify">Based on the survey, SMEs are strunggling to find skilled employes, attracting customers, and developing innovative products. These are the top 3 challenges faced by our SMEs. the rest found it hard to deal with financing and official regulations. Most of the answers suggest that these businesses hope for a better reach and understanding over local and international customers - which means they didn\'t - as well as better advertisement.</p>',unsafe_allow_html = True)     



option1 = st.selectbox('World Bank Indonesian SMEs\' Insights', wdywk1)
if option1 is wdywk1[1]:
    challenge()
if option1 is wdywk1[2]:
    eorderWithinHomeCountry()
if option1 is wdywk1[3]:
    eordersreceived()
if option1 is wdywk1[4]:
    enetsales()
if option1 is wdywk1[5]:
    Sector()
if option1 is wdywk1[6]:
    UpSkill()
if option1 is wdywk1[7]:
    expectation()
if option1 is wdywk1[8]:
    digital_anxiety()
if option1 is wdywk1[9]:
    online_target()
if option1 is wdywk1[10]:
    formarketchal()
if option1 is wdywk1[11]:
    ebuspurchase()
    
option2 = st.selectbox('Indonesian SMEs\' Insights (a research of Universitas Indonesia)', wdywk2) 
if option2 is wdywk2[1]:
    st.subheader('Factors SMEs have to use E-business')
    grouped_hist(techFac)
if option2 is wdywk2[2]:
    st.subheader('SMEs are using E-business for:')
    grouped_hist(eBusUse)
if option2 is wdywk2[3]:
    st.subheader('The impact of E-business on SMEs performance')
    grouped_hist(eBusPero)  
