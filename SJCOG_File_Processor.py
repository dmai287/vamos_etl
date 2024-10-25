import streamlit as st
import pandas as pd
import plotly as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def combine(flist):             # Used to merge new data file and old data file
    if flist:
        df = pd.DataFrame()
        for file in flist:
            new_df = pd.read_csv(file)
            df = pd.concat([df,new_df],axis=0)
        df = df.astype('str')
        df[df.columns[0]] = pd.to_datetime(df[df.columns[0]]) # change first column as timestampe
        df = df.sort_values(by=df.columns[0]) # sort the data as time ascending order
        # df.drop("no needed columns")
        return df




def sub(df) :              # Remove duplicated search records based on RequestTime
    title = df.columns[[0,1,14,15]]
    key = list(zip(df[df.columns[0]],df[df.columns[1]],df[df.columns[14]],df[df.columns[15]])) # # Combine date and userID as the key column
    key = set(key)              #  # Use set to remove the duplicated records
    df_key = pd.DataFrame(key) 
    df_key = df_key.sort_values(by=df_key.columns[0]) # Sort by date   
    #idx = df_key.index
    #new_df = df.iloc[idx,:].copy()
    df_key.columns = title
    df_key = df_key.reset_index()
    df_key = df_key.drop(['index'],axis = 1)
    return (df_key)

def selected(df):            # Remove duplicated search records based on DepartureTime
    title = [ 'DepartureTime','UserID','MinimumTravelTimeSeconds','StartBlockGeoID','EndBlockGeoID']
    df = df[df['LastSelected']==True]
    key =list(zip(df['DepartureTime'],df['UserID'],df['MinimumTravelTimeSeconds'],df['StartBlockGeoID'],df['EndBlockGeoID']))
    key = set(key)              
    select_df = pd.DataFrame(key)
    select_df.columns = title
    select_df[ 'DepartureTime'] = pd.to_datetime(select_df[ 'DepartureTime'])
    select_df = select_df.sort_values(by='DepartureTime')
    select_df['ArrivalTime'] = pd.to_datetime(select_df['DepartureTime']) + pd.to_timedelta(select_df['MinimumTravelTimeSeconds'], unit='s')
    select_df = select_df[[ 'DepartureTime','UserID','ArrivalTime','StartBlockGeoID','EndBlockGeoID']]
    #select_df = select_df[['UserID', 'DepartureTime','MinimumTravelTimeSeconds','StartBlockGeoID','EndBlockGeoID']]
    #select_df[ 'DepartureTime'] = pd.to_datetime(select_df[ 'DepartureTime'])
    #select_df = select_df.sort_values(by='DepartureTime')
    return select_df



def get_geo(geo_df,geo_file):            # Convert GeoID to Lon/LAT
    dic = pd.read_csv(geo_file)
    dic['Geoid'] = dic['Geoid'].astype('str')
    ori_long = []
    ori_lat = []
    end_long = []
    end_lat = []
    for ori in geo_df.StartBlockGeoID:
        if (ori in list(dic['Geoid'])):
            ori_long.append(list(dic[dic['Geoid'] == ori]['LONGITUDE']))
            ori_lat.append(list(dic[dic['Geoid'] == ori]['LATITUDE']))
        else:
            ori_long.append([0])
            ori_lat.append([0])
            
    for end in geo_df.EndBlockGeoID:
        if (end in list(dic['Geoid'])):
            end_long.append(list(dic[dic['Geoid'] == end]['LONGITUDE']))
            end_lat.append(list(dic[dic['Geoid'] == end]['LATITUDE']))
        else:
            end_long.append([0])
            end_lat.append([0])
    
    ori_long = [val for element in ori_long for val in element ]
    ori_lat = [val for element in ori_lat for val in element ]  
    end_long = [val for element in end_long for val in element ]  
    end_lat = [val for element in end_lat for val in element ]  
    geo_df['Origin_LON'] = ori_long
    geo_df['Origin_LAT'] = ori_lat
    geo_df['Destination_LON'] = end_long
    geo_df['Destination_LAT'] = end_lat
    geo_df = geo_df[(geo_df != 0).all(1)]
    return geo_df


# In[12]:


def convert(file):              
    df = pd.read_csv(file)
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]]) # change first column as timestamped
    df = df.sort_values(by=df.columns[0]) # sort the data as time ascending order
    origin = (df['StartBlockGeoID']//1000).astype(str)
    destination = (df['EndBlockGeoID']//1000).astype(str)
    element_length = len(origin[0])
    if (element_length != 11):
        for i in range(len(origin)):
            origin[i] = origin[i][:-(element_length-11)]
        for j in range(len(destination)):
            destination[j] = destination[j][:-(element_length-11)]
    df['StartBlockGeoID'] = origin
    df['EndBlockGeoID'] = destination
        
    outlier = ['60770000000', '60770100000', '60990000000']
    df = df[~df['StartBlockGeoID'].isin(outlier)]
    df = sub(df)   
    # df.drop("no needed columns")
    #df = sub(df).reset_index(drop=True)
    geo_df = get_geo(df,geo_file)
    return df
    

def convert2(file):
    df = pd.read_csv(file)
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]]) # change first column as timestamped
    df = df.sort_values(by=df.columns[0]) # sort the data as time ascending order
    origin = (df['StartBlockGeoID']//1000).astype(str)
    destination = (df['EndBlockGeoID']//1000).astype(str)
    element_length = len(origin[0])
    if (element_length != 11):
        for i in range(len(origin)):
            origin[i] = origin[i][:-(element_length-11)]
        for j in range(len(destination)):
            destination[j] = destination[j][:-(element_length-11)]
    df['StartBlockGeoID'] = origin
    df['EndBlockGeoID'] = destination
        
    outlier = ['60770000000', '60770100000', '60990000000']
    df = df[~df['StartBlockGeoID'].isin(outlier)]
    df = selected(df)   
    # df.drop("no needed columns")
    #df = sub(df).reset_index(drop=True)
    geo_df = get_geo(df,geo_file)
    return df


# Functions for plots
def new_user_count(search): #users is a df with 2 columns ['RequestTime','UserID']
    
    user = search[['RequestTime','UserID']].copy()
    user['RequestTime'] = pd.to_datetime(user['RequestTime']).dt.floor('d')
    
    day_user = user.copy()
    day_user['RequestTime'] = (day_user['RequestTime']).dt.floor('d')
    daily_active = pd.DataFrame(day_user.groupby(['RequestTime'])['UserID'].nunique()).reset_index()
    daily_active.columns = ['RequestTime','Number Of Active']

    trace1 = go.Scatter(x =daily_active['RequestTime'] ,y=daily_active['Number Of Active'])  # x is date, y is counts
    fig1 = go.Figure(trace1)
    fig1.update_layout(title = 'Daily Active Users',
                 xaxis_title = 'Date',
                 yaxis_title = 'Active Users')
    #return daily_active
    month_user = user.copy()
    
    month_user['RequestTime'] = month_user['RequestTime'].dt.to_period('M')
    month_active = pd.DataFrame(month_user.groupby(['RequestTime'])['UserID'].nunique()).reset_index()
    month_active.columns = ['RequestTime','Number Of Active']
    trace2 = go.Scatter(x =month_active['RequestTime'].astype(str) ,y=month_active['Number Of Active'])  # x is date, y is counts
    fig2 = go.Figure(trace2)
    fig2.update_layout(title = 'Monthly Active Users',
                 xaxis_title = 'Date',
                 yaxis_title = 'Active Users')        

    #return month_active
    quarter_user = user.copy()

    quarter_user['RequestTime'] = quarter_user['RequestTime'].dt.to_period('Q')
    quarterly_active = pd.DataFrame(quarter_user.groupby(['RequestTime'])['UserID'].nunique()).reset_index()
    quarterly_active.columns = ['RequestTime','Number Of Active']
    trace3 = go.Scatter(x =quarterly_active['RequestTime'].astype(str) ,y=quarterly_active['Number Of Active'])  # x is date, y is counts
    fig3 = go.Figure(trace3)
    fig3.update_layout(title = 'Quarterly Active Users',
                 xaxis_title = 'Date',
                 yaxis_title = 'Active Users')
    #return quarterly_active
    
    return fig1,fig2,fig3


def count_by_period(dates,period): #dates is a column of timestamp，period can be (day,month, quarter)
    period = str.lower(period)    # Ignore case of input
    if (period == 'day'): 
        dates = dates.dt.floor('d').value_counts()
        return dates
    elif(period == 'month'):
        dates = dates.dt.to_period('M').value_counts()
        return dates
    elif(period == 'quarter'):
        dates = dates.dt.to_period('Q').value_counts()
        return dates
    elif (period == 'hour'):
        dates = dates.dt.to_period('H').value_counts()
        return dates
    else:
        print('Please input day,month,or quarter for the second argument.')

def count_use(df,period):       
    key = list(zip(df[df.columns[0]],df[df.columns[1]])) 
    key = set(key)              
    df_key = pd.DataFrame(key) 
    df_key = df_key.sort_values(by=df_key.columns[0]) 
    df_key[0] = df_key[0].astype('datetime64[ns]')
    counts = pd.DataFrame(count_by_period(df_key[0],period)) 
    counts = counts.sort_index() 
    return counts

def usage_count(file):
    daily = count_use(file,'day')
    trace1 = go.Scatter(x = list(daily.index),y=daily[0])  # x is date, y is counts
    fig1 = go.Figure(trace1)
    fig1.update_layout(title = 'Daily Counts',
             xaxis_title = 'Date',
             yaxis_title = 'Counts(times)')
    monthly = count_use(file,'month')
    monthly.index = monthly.index.strftime('%Y-%m') # Convert PeriodIndex to normal Index
    trace2 = go.Scatter(x = monthly.index.to_series(),y=monthly[0])
    fig2 = go.Figure(trace2)
    fig2.update_layout(title = 'Monthly Counts',
                      xaxis_title = 'Date',
                      yaxis_title = 'Counts(times)')
    quarterly = count_use(file,'quarter')
    trace3 = go.Scatter(x = (quarterly.index.to_series().astype(str)),y=list(quarterly[0]))
    fig3 = go.Figure(trace3)
    fig3.update_layout(title = 'Quarterly Counts',
                     xaxis_title = 'Quarter',
                     yaxis_title = 'Counts(times)')
    return fig1,fig2,fig3

def count_total(file):
    file['CreatedAt'] = file['CreatedAt'].astype('datetime64[ns]').dt.to_period('M')
    grouped = pd.DataFrame(zip(file['CreatedAt'],file['Price']))
    total = grouped.groupby(by = grouped.columns[0]).sum()
    return total

def ticket_sale(file):
    file1 = file.copy()
    total = count_total(file1)
    file2 = file.copy()
    monthly = count_use(file,'month')
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x = list(total.index.strftime('%Y-%m')),y=total[1], name = '$ Amount of Sale'))
    fig.add_trace(go.Scatter(x = list(monthly.index.strftime('%Y-%m')),y=monthly[0], name = 'Number of Sale'),secondary_y=True)
    fig.update_layout(title = 'Monthly Ticket Sale in USD 2021',
                     xaxis_title = 'Month',
                     yaxis_title = 'USD')
    fig.update_yaxes(title_text="Number of Ticket Sale", secondary_y=True)
    return fig
# In[ ]:


options = ['1.File Merger','2.Usage Report','3.Purchase Report','4.Get Geo Data(Request)','5.Get Geo Data（Departure）']
page = st.sidebar.selectbox('Choose a function',options)
if (page == '1.File Merger'):
    st.header('CSV File Merger')
    st.write('You can upload csv files with same format and merge them into one file. ')

    files = st.file_uploader('Upload CSV Files Below',type = ['csv'],accept_multiple_files = True)
    df = combine(files)
    note = 'Please make sure the uploaded csv files are in exactly the same format.(i.e.Same number of columns and same columns names.'
    st.markdown(f'<h1 style="color:#f20f12;font-size:16px;">{note}</h1>', unsafe_allow_html=True)
    if files:
        if st.checkbox("Show Merged File"):
            st.write('This is how the merged file looks like: ')
            st.dataframe(df)


        fname = st.text_input('Output file name(No suffixes):')
        fname = fname+'.csv'
        csv = df.to_csv(index = False)
        st.download_button('Download merged file',data = csv,file_name=fname)
elif (page == '2.Usage Report'):     
    ff = st.file_uploader('Upload CSV File Below',type = ['csv'])
 
    if ff:
        search = pd.read_csv(ff)
        active_day, active_month, active_q  = new_user_count(search)
        usage_d, usage_m,usage_q =  usage_count(search)
        
        st.plotly_chart(active_day)
        note_d = 'The plot above is showing the number of active user by day. '
        st.markdown(f'<h1 style="color:#000080;font-size:16px;">{note_d}</h1>', unsafe_allow_html=True)
        
        st.plotly_chart(active_month)
        note_m = 'The plot above is showing the number of active user by month. '
        st.markdown(f'<h1 style="color:#000080;font-size:16px;">{note_m}</h1>', unsafe_allow_html=True)
        
        st.plotly_chart(active_q)
        note_q = 'The plot above is showing the number of active user by quarter. '
        st.markdown(f'<h1 style="color:#000080;font-size:16px;">{note_q}</h1>', unsafe_allow_html=True)
        
        st.plotly_chart(usage_d)
        note_dd = 'The plot above is showing the app usage by day. '
        st.markdown(f'<h1 style="color:#000080;font-size:16px;">{note_dd}</h1>', unsafe_allow_html=True)
        
        st.plotly_chart(usage_m)
        note_mm = 'The plot above is showing the app usage by month. '
        st.markdown(f'<h1 style="color:#000080;font-size:16px;">{note_mm}</h1>', unsafe_allow_html=True)
        

        st.plotly_chart(usage_q)
        note_qq = 'The plot above is showing the app usage by quarter. '
        st.markdown(f'<h1 style="color:#000080;font-size:16px;">{note_qq}</h1>', unsafe_allow_html=True)
        
elif (page == '3.Purchase Report'):     
    pp = st.file_uploader('Upload CSV File Below',type = ['csv'])
 
    if pp:
        purchase = pd.read_csv(pp)
        st.plotly_chart(ticket_sale(purchase))
        note_pp = 'The red line represent the number of tickets sold by month, the blue line represent the sales amount of ticket by month. '
        st.markdown(f'<h1 style="color:#000080;font-size:16px;">{note_pp}</h1>', unsafe_allow_html=True)        
        
    
elif (page == '4.Get Geo Data(Request)'):
    st.header('Get Geo Data By Request Time From File')
    st.write('Upload a csv file and get geo data(LON/LAT) from it. ')
    note = 'Please make sure the uploaded csv file is generated from the File Merger '
    st.markdown(f'<h1 style="color:#f20f12;font-size:16px;">{note}</h1>', unsafe_allow_html=True)
    f = st.file_uploader('Upload CSV File Below',type = ['csv'])
    st.write('Upload The Geo Dctionary File ')
    geo_file = st.file_uploader('Upload Geo Dictionary Files Below',type = ['csv'])
    if f and geo_file:
        geo_df = convert(f)
        if st.checkbox("Show Data"):
            st.write('This is how the Geo Data looks like: ')
            st.dataframe(geo_df) 
        l = len(geo_df)
        st.write('There are',l,'rows in the file.')
        fname = st.text_input('Output file name(No suffixes):')
        fname = fname+'.csv'
        csv = geo_df.to_csv(index = False)
        
        st.download_button('Download geo file',data = csv,file_name=fname)

elif (page == '5.Get Geo Data（Departure）'):
    st.header('Get Geo Data By Departure Time From File')
    st.write('Upload a csv file and get geo data(LON/LAT) from it. ')
    note = 'Please make sure the uploaded csv file is generated from the File Merger '
    st.markdown(f'<h1 style="color:#f20f12;font-size:16px;">{note}</h1>', unsafe_allow_html=True)
    f = st.file_uploader('Upload CSV File Below',type = ['csv'])
    st.write('Upload The Geo Dctionary File ')
    geo_file = st.file_uploader('Upload Geo Dictionary Files Below',type = ['csv'])
    if f and geo_file:
        geo_df = convert2(f)
        if st.checkbox("Show Data"):
            st.write('This is how the Geo Data looks like: ')
            st.dataframe(geo_df) 
        l = len(geo_df)
        st.write('There are',l,'rows in the file.')
        fname = st.text_input('Output file name(No suffixes):')
        fname = fname+'.csv'
        csv = geo_df.to_csv(index = False)
        st.download_button('Download geo file',data = csv,file_name=fname)
    
