#**********************************************************************
# Importing  used libraries
#**********************************************************************
import sys
import os    
from enum import Enum
from decimal import Decimal
import copy
import numpy as np
import pandas as pd
import dash
from dash import Dash, dcc, html,Input, Output
from dash import dash_table as dt
import plotly.express as px
import logging
"""Parsing a existing contact data base file.     
       1. Reading a cnd file and storing the data in list and arrays.
       2. Writing the contact information in a spreadsheet.
       3. Plotting a contact information for a contact pair as requested.
       
        Parameters
        ----------
        filename : str
            Contact diagnosis input file with .cnd extention.
        num_row  : int, in [10:80:10]
            number of rows to be displayed in the spreadsheet
        spairid : int 
            cont pair real identity number for which data visualization is requested.  
        yvalues: str
            Short names of the column need to be plotted as lited in (NLHIST,CONT)
        xvalue: str
            x-axis of the plot, LoadStep,SubStep,IteretionNo,Time  
            
       Raises  
       -----------   
        FileNotFoundError : If contact data base file, {filename} is missing in the current directory.        
        RuntimeError      : If ShortName is not assigned for a discriptive name. 
        
       Note
       -----------
        1. Plotting a contact pair data for an exiting cnd file.
        2. Plotting a contact pair data with changing cnd file for monitering solution. ...
        3. Hooking it with with remote server data. ...          
"""
#now we will Create and configure logger
logging.basicConfig(filename="cndparser.log", 
					format='%(asctime)s %(message)s', 
					filemode='w')
#Let us Create an object 
logger=logging.getLogger()
#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)                  
def parse_cnd_data(filename):
    if not (os.path.exists(filename)):
         logger.error(f'The file {filename} does not exist.')
         raise FileNotFoundError(f'The file {filename} does not exist.')  
    #**********************************************************************
    #String variables
    #**********************************************************************
    #Writing frequency of contact variables 
    #FRQ = ["ITERATION","SUBSTEP","LOAD_STEP"]
    #Name of the contact information for each pair 
    cont_name_header = []
    #Name of the information for the each writing frequency
    load_time_header0 = [ 'LOADSTEP', 'SUBSTEP', 'ITERATION', 'TIME', 'SCALED TIME' ]
    load_time_header = [ 'LdStp', 'CumSbStp', 'CumIter', 'Time', 'ScaledTime' ]
    #Numeric variables
    #Information per contact pair
    ninfo_per_pair = [] 
    #Number of contact pair
    paircount = 0  
    #cont_pair_info[frq,ncontpair,:] = [ContPair ID, p2, p3, ... nInfoPerContPair] 
    cont_pair_info = [] 
    #load_time[frq,:] = [ 'LOADSTEP', 'SUBSTEP', 'ITERATION', 'TIME', 'SCALED TIME' ]
    load_time = [] 
    #list of contact pair ids
    pair_ids = []
    #local variables
    cntr = 0
    frq_num = 0
    scaletimeflg = 0  
    with open(filename, 'r') as reader:
        for line in reader:
            cntr = cntr + 1         
            if cntr == 1:                     # <SOLUTION> 
               pass 
            elif cntr == 2:                   # <HEADER FRQ=...>
               frq_nam = line[13:-3]
            elif line[2:11] == 'COLUMN ID' :  # The Contact Pair Info              
               cont_name_header.append(line[20:-10])
            elif line[2:7] == 'UNITS' :       # Reading UNITS Info   
               pass 
            elif line[2:-2] == 'HEADER' :     # Last line of the header              
                ninfo_per_pair = len(cont_name_header)             
            elif((line[1:8] == 'COLDATA' or line[:3].isspace())):         
                if(line[1:8] == 'COLDATA'):
                   #<COLDATA LOAD_STEP="        1" SUBSTEP="        1" ITERATION="        4" TIME="   0.1000000    " PHYSICAL TIME FOR WEAR="   0.1000000    ">   
                   load_time.append(float(line[20:29])) # LOAD_STEP
                   load_time.append(float(line[40:49])) # SUBSTEP 
                   load_time.append(float(line[62:71])) # ITERATION
                   load_time.append(float(line[79:95])) # TIME 
                   paircount = 0
                   if(len(line) == 140):
                      load_time.append(float(line[121:136])) # PHYSICAL TIME FOR WEAR
                      scaletimeflg = 1                        
                   frq_num = frq_num + 1
                elif(line[:3].isspace()):                     
                   nline = list(map(float,line.split()))                                               
                   cont_pair_info.append(nline) 
                   paircount = paircount + 1
            else:
                pass  
    #Data in the cnd file is fetched
    logger.info(f'The file {filename} successfully read.')
    logger.info(f'Number of contact pair:  {paircount}')
    logger.info(f'Number information per contact pair:  {ninfo_per_pair}')
    logger.info(f'Contact data is written  for {frq_num}  {frq_nam}S. ')
    
    #print( 'Number of contact pair: ' , paircount)
    #print( 'Number information per contact pair: ' , ninfo_per_pair)
    #print('Contact data is written  for  ', frq_num , '   ', frq_nam+'S')
    #pair ids list
    for pair in range(paircount):
        pair_ids.append(int(cont_pair_info[pair][0]))
    #short name    
    short_name = list(cont_name_header)        # <-- makes a *copy* of the list
    for col_num, data in enumerate(cont_name_header):
        if(data == 'Contact Pair ID'):
            short_name[ col_num] = 'CNID'     
        elif(data == 'Number of Contact Elements in Contact'):
            short_name[ col_num] = 'ELCN'
        elif(data == 'Number of Contact Elements in Contact (Sticking)'):
            short_name[ col_num] = 'ELST'
        elif(data == 'Max. Chattering Level'):
            short_name[ col_num] = 'CNOS' 
        elif(data == 'Max. Penetration/Min. Gap'):
            short_name[ col_num] = 'PENE'
        elif(data == 'Max. Geometric Gap'):
            short_name[ col_num] = 'CLGP' 
        elif(data == 'Max. Normal Stiffness'):
            short_name[ col_num] = 'KNMX' 
        elif(data == 'Min. Normal Stiffness'):
            short_name[ col_num] = 'KNMN'
        elif(data == 'Max. Resulting Pinball'):
            short_name[ col_num] = 'PINB'
        elif(data == 'Max. Elastic Slip Distance'):
            short_name[ col_num] = 'ESLI'
        elif(data == 'Max. Tangential Stiffness'):
            short_name[ col_num] = 'KTMX'
        elif(data == 'Min. Tangential Stiffness'):
            short_name[ col_num] = 'KTMN'
        elif(data == 'Max. Sliding Distance of Entire Solution'):
            short_name[ col_num] = 'SLID'
        elif(data == 'Max. Contact Pressure'):
            short_name[ col_num] = 'PRES'
        elif(data == 'Max. Friction Stress'):
            short_name[ col_num] = 'SFRI'
        elif(data == 'Average Contact Depth'):
            short_name[ col_num] = 'CNDP'
        elif(data == 'Max. Geometric Penetration'):
            short_name[ col_num] = 'CLPE'
        elif(data == 'Number of Contact Points Have Too Much Penetration'):
            short_name[ col_num] = 'LGPE' 
        elif(data == 'Contacting Area'):
            short_name[ col_num] = 'CAREA'
        elif(data == 'Max. Contact Damping Pressure'):
            short_name[ col_num] = 'NDMP'
        elif(data == 'Max. Contact Damping Tangential stress'):
            short_name[ col_num] = 'TDMP'
        elif(data == 'Max. Sliding Distance including near field'):
            short_name[ col_num] = 'GSMX'
        elif(data == 'Min. Sliding Distance including near field'):
            short_name[ col_num] = 'GSMN'
        elif(data == 'Max. normal fluid penetration pressure on contact surface'):
            short_name[ col_num] = 'FPSC'
        elif(data == 'Max. normal fluid penetration pressure on target surface'):
            short_name[ col_num] = 'FPST'
        elif(data == 'Total volume loss due to wear on contact surface'):
            short_name[ col_num] = 'WEAR'
        elif(data == 'Total strain energy due to contact'):
            short_name[ col_num] = 'CTEN'
        elif(data == 'Frictional dissipation energy'):
            short_name[ col_num] = 'CFEN'
        elif(data == 'Contact damping dissipation energy'):
            short_name[ col_num] = 'CDEN'
        elif(data == 'WB contact pair ID'):
            short_name[ col_num] = 'WBCNID'
        elif(data == 'Total contact force due to pressure -x component'):
            short_name[ col_num] = 'CFNX'
        elif(data == 'Total contact force due to pressure -y component'):
            short_name[ col_num] = 'CFNY' 
        elif(data == 'Total contact force due to pressure -z component'):
            short_name[ col_num] = 'CFNZ'
        elif(data == 'Maximum torque in axisymmetric analysis with MU=1.0'):
            short_name[ col_num] = 'CTRQ'            
        elif(data == 'Total contact force due to tangential stress -x component'):
            short_name[ col_num] = 'CFSX'
        elif(data == 'Total contact force due to tangential stress -y component'):
            short_name[ col_num] = 'CFSY'
        elif(data == 'Total contact force due to tangential stress -z component'):
            short_name[ col_num] = 'CFSZ'
        elif(data == 'Number of Contact Points Have Too Much sliding'):
            short_name[ col_num] = 'LGSL'
        elif(data == 'Contact pair force convergence norm'):
            short_name[ col_num] = 'NORM'
        elif(data == 'Contact pair force criterion'):
            short_name[ col_num] = 'CRIT'
        elif(data == 'Max. tangential fluid penetration pressure on contact surface'):
            short_name[ col_num] = 'FPTC'
        elif(data == 'Max. tangential fluid penetration pressure on target surface'):
            short_name[ col_num] = 'FPTT' 
        elif(data == 'Max. sliding distance of current substep for closed contact'):
            short_name[ col_num] = 'SLMX'
        else: 
            logger.error(f'short_name is not assigned for {data}.')       
            raise RuntimeError(f'short_name is not assigned for {data}.')    
    if (scaletimeflg == 1):
       fqnum = 5
    else:
       fqnum = 4
       del load_time_header0[4]
       del load_time_header[4]
    #converting the list into array,
    cont_pair_info = np.array(cont_pair_info)
    #rearranging contact parameters
    maparray=[0,1,2,3,4,5,16,8,15,18,6,7,13,9,12,21,22,10,11,14,26,27,17,36,37,38,19,20,28,
              23,24,39,40,25,29,41,30,31,32,33,34,35]
    maparray=np.array(maparray)       
    cont_pair_info=cont_pair_info[:,maparray]     
    cont_name_header=[cont_name_header[i] for i in maparray]    
    short_name=[short_name[i] for i in maparray]        
    #delete first column (contact ids)
    cont_pair_info = np.delete(cont_pair_info,0,1)
    #cumulative iteration
    cum_list=[] 
    if (frq_nam == 'SUBSTEP' or frq_nam == 'LOADSTEP'):
        data1 = list(load_time[2:fqnum*frq_num:fqnum])
        cum_list = [sum(data1[0:x:1]) for x in range(0, frq_num+1)]        
        data1 = cum_list[1:]
        load_time[2:fqnum*frq_num:fqnum] = data1
    else:
        data1=list(load_time[2:fqnum*frq_num:fqnum])
        data2=list(load_time[2:fqnum*frq_num:fqnum])
        #print(*data1,sep='\n')
        for i in range(0,frq_num-1):                           
            if (data2[i] == 0 and i >= 1):                      
               data1[i:] = [x+data1[i-1] for x in data2[i:]]     
        load_time[2:fqnum*frq_num:fqnum]=data1 
    #converting list into array
    load_time = np.array(load_time)
    load_time = np.reshape(load_time,(frq_num,fqnum))
    #cumulative substeps      
    #ldlist=list(set(load_time[0:fqnum*frq_num:fqnum]))
    data1=list(load_time[:,1])
    ls_index=[]
    bs_index=[]
    sbs_index=[]
    for i in range(0,frq_num-1):
         cntr = load_time[i+1,0]-load_time[i,0]                
         if (cntr==1): 
            ls_index.append(i)         
            data1[(i+1):]=load_time[(i+1):,1]+data1[i]            
         if ( (load_time[i+1,0]-load_time[i,0])== 0 and (load_time[i+1,1]-load_time[i,1])== 0 and (load_time[i+1,2]-load_time[i,2])==0):  
            bs_index.append(i)
         if (frq_nam == 'ITERATION'): 
             if ( (load_time[i+1,1]-load_time[i,1])== 1):  
                sbs_index.append(i)  
    load_time[:,1]=data1             
    del short_name[0]
    del cont_name_header[0]    
    comb_short_name = list(short_name)
    comb_short_name = [*load_time_header,*comb_short_name]
    comb_long_name  =  [*load_time_header0,*cont_name_header]
    return cont_pair_info,load_time,comb_short_name,comb_long_name,pair_ids,frq_num,ls_index,bs_index,sbs_index
#testing the parse_cnd_data
#[cont_pair_info,load_time,comb_short_name,comb_long_name,pair_ids,frq_num,ls_index,bs_index,sbs_index]=parse_cnd_data('ev174d-2s_iter.cnd')
#[cont_pair_info,load_time,comb_short_name,comb_long_name,pair_ids,frq_num,ls_index,bs_index,sbs_index]=parse_cnd_data('ev174d-2s_subs.cnd')
#[cont_pair_info,load_time,comb_short_name,comb_long_name,pair_ids,frq_num,ls_index,bs_index,sbs_index]=sparse_cnd_data('ev174d-8s.cnd')
#[cont_pair_info,load_time,comb_short_name,comb_long_name,pair_ids,frq_num,ls_index,bs_index,sbs_index]=parse_cnd_data('BJA_R2900K_trans_BJA_v_4g_ANS.cnd')  
#print(*comb_short_name,sep='\n')
#print(*comb_long_name,sep='\n')
#print(load_time[:,0])
#print(*load_time[:,2],sep='\n') 
#exit()
#data required to multiple functions
cont_pair_info=[]
load_time=[]
comb_short_name=[]
comb_long_name=[]
pair_ids=[]
frq_num=[]
font1='16px'
#App layout
app = dash.Dash(__name__, prevent_initial_callbacks=True) 
app.title = 'CND Visualizer'
app.layout = html.Div([
    html.Div(className='row',children=[
    html.Div(children=[    
    dcc.Upload(              
        html.Div([
            'Drag and Drop or ',
            html.A('Import cnd File')
        ],style={ 'width': '100%',
            'height': '50px',
            'lineHeight': '50px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            #'margin': '5px',                    
            'font-weight': 'bold',
            'font-size':'14px',
            #'background-color': 'blue'           
        }),               
        # Allow one or multiple files to be uploaded
        multiple=False,
        id='upload_cnd_data'
        )
        ],style= dict(width='15%')), 
    
    html.Div(children=[
              html.Label(['Select No. of Rows to Display'], 
                   style={ 'font-size':font1,
                          'font-weight': 'bold', 
                          'text-align':  'center',
                          'offset': 5}
                ),             
              dcc.Dropdown(
                  id='rows_to_display',
                  options=[10,20,30,40,50,60,70,80], 
                  value =20,
                  clearable=False                        
                ) 
        ],style=dict(width='15%')),
     
    html.Div(children=[
              html.Label(['Select a Contact Pair'], 
                   style={'font-size': font1,
                           'font-weight': 'bold', 
                           "text-align": "center"}
              ),
              dcc.Dropdown(
                  id='contpair_selection',
                  options =[],#cont_ids
                  clearable=False                
              )
        ],style=dict(width='10%')), 
    
    html.Div(children=[
              html.Label(['Select X Value'],
              style={'font-size': font1,
                           'font-weight': 'bold', 
                           "text-align": "center"}
              ),           
              dcc.Dropdown(                                   
                  id='xvalue_selection' ,
                  options=[],#comb_long_name,
                  #value = 'TIME',
                  clearable=False
              )
        ],style=dict(width='20%')), 
    
    html.Div(children=[
              html.Label(['Select Y Values'],
              style={'font-size': font1,
                           'font-weight': 'bold', 
                           "text-align": "center"}
              ),             
              dcc.Dropdown(
                  id='yvalues_selection',
                  options=[],#comb_long_name,
                  #value = 'Max. Contact Pressure',
                  multi = True,
                 clearable=True                           
                ) 
        ],style=dict(width='40%')), 
    ],style=dict(display='flex')),       
    html.Hr(),
    html.Div(id='spreadsheet_container'), 
    html.Hr(),
    #html.H2('Contact Plot'), 
    dcc.Graph(id='graph_container', figure={})   
 ])
#-------------------------------------------------------------------------------------
#upload_cnd_data
@app.callback(
    [
     Output('contpair_selection','options'),
     Output('xvalue_selection','options'),
     Output('yvalues_selection','options')
    ],
    [Input('upload_cnd_data', 'filename')
    ]
    )
def upload_data(filename):
    global cont_pair_info,load_time,comb_short_name,comb_long_name,pair_ids,frq_num,ls_index,bs_index,sbs_index 
    [cont_pair_info,load_time,comb_short_name,comb_long_name,pair_ids,frq_num,ls_index,bs_index,sbs_index]=parse_cnd_data(filename)      
    return pair_ids,comb_long_name,comb_long_name
#-------------------------------------------------------------------------------------
#generate the spreadsheet for the selected pair
#hilight the selected x-value with blue color
#hilight selected y-values with different colors
#plot the selected x-y graph
@app.callback(
    [
     Output('spreadsheet_container','children'),
     Output('graph_container','figure')
    ],
    [
    Input('rows_to_display',    'value'),
    Input('contpair_selection', 'value'),
    Input('xvalue_selection',   'value'),
    Input('yvalues_selection',  'value'),
    #Input('upload_cnd_data', 'filename')
    ]
    )
#def spreadsheet_gen(num_row,spairid,xvalue,yvalues,filename):
def spreadsheet_gen(num_row,spairid,xvalue,yvalues):       
        global cont_pair_info,load_time,comb_short_name,comb_long_name,pair_ids,frq_num,ls_index,bs_index,sbs_index
        #[cont_pair_info,load_time,comb_short_name,comb_long_name,pair_ids,frq_num]=parse_cnd_data(filename)
        if(spairid != None):
            cnid = pair_ids.index(spairid) 
        else:
            cnid = 0                      
        if(xvalue == None):
          xvalue='ITERATION'          
        if(yvalues == None):
          yvalues=['Number of Contact Elements in Contact']  
        #print(comb_long_name) 
        #print(comb_short_name)       
        xvalue=comb_short_name[comb_long_name.index(xvalue)]            
        for p in range(len(yvalues)):
            yvalues[p]=comb_short_name[comb_long_name.index(yvalues[p])]   
        paircount=len(pair_ids)
        pairdata_cnid = np.concatenate((load_time,cont_pair_info[cnid:frq_num*paircount+cnid:paircount,:]),1)
        df = pd.DataFrame(pairdata_cnid, columns= comb_short_name)
        return [dt.DataTable(        
                id='datatable-interactivity',
                columns=[
                 {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": True}            
                 for i in df.columns
                ],
               data=df.to_dict('records'), # the contents of the table
               editable=True,              # allow editing of data inside all cells
               filter_action="native",     # allow filtering of data by user ('native') or not ('none')
               sort_action="native",       # enables data to be sorted per-column by user or not ('none')
               sort_mode="single",         # sort across 'multi' or 'single' columns
               column_selectable="multi",  # allow users to select 'multi' or 'single' columns
               row_selectable="multi",     # allow users to select 'multi' or 'single' rows
               row_deletable=False,        # choose if user can delete a row (True) or not (False) 
               page_action="native",       # all data is passed to the table up-front or not ('none')
               page_current=0,             # page number that user is on
               # ids of columns that user selects
               selected_columns=[],        #comb_long_name.index(yvalues),               
               selected_rows=[],           # indices of rows that user selects
               page_size=num_row,          # number of rows visible per page
               style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
               style_cell={                # ensure adequate header width when text is shorter than cell's text
                   'minWidth': 110, 'maxWidth': 130, 'width': 100,
                   #'font-family': 'cursive',
                   #'font-size': '14px'
                },
               style_data={                # overflow cells' content into multiple lines
                 'whiteSpace': 'normal',
                 'height': 'auto',
                 'color': 'black',
                 'backgroundColor': 'white'            
                },        
               style_data_conditional=[
                {# alternate color lines                    
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)' 
                },
                
                {    
                'if': {'column_id': xvalue},
                'background_color': '#808000'                                 
                },
                
                {                 
                'if': {'column_id': yvalues},
                'background_color': '#D2F3FF'
                }               
                ] 
                    
        ),        
         graphgen(df, xvalue, yvalues,ls_index,bs_index,sbs_index)        
        ]   
def graphgen(df,x,y,ls_index,bs_index,sbs_index):
    fig = px.line(df,x,y)
    xx=df[x]
    if ls_index:
        for i in ls_index:         
            fig.add_vline(xx[i], line_width=2, line_dash="dash", line_color="blue")
    if bs_index:
        for i in bs_index:         
           fig.add_vline(xx[i], line_width=2, line_dash="dash", line_color="red") 
           
    if sbs_index:
        for i in sbs_index:         
           fig.add_vline(xx[i], line_width=2, line_dash="dash", line_color="green") 
    return fig    
if __name__ == '__main__':
    app.run_server(debug=True,host='127.0.0.1', port='7080')
