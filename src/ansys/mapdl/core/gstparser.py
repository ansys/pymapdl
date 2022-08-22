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
"""Parsing a existing graphical solution tracking (gst) file.     
       1. Reading a gst file and storing the data in list and arrays.
       2. Plotting a selected parameter with respect to cummulative error.
       
        Parameters
        ----------
        filename : str
            Graphical solution tracking (gst) file with .gst extention. 
        yvalues: str
            Names of the column need to be plotted.
        xvalue: str
            x-axis of the plot,cumulative iteration.  
            
       Raises  
       -----------   
        FileNotFoundError : If gst file, {filename} is missing in the current directory.  
        
       Note
       -----------
        1. Plotting a convergence parameter for an exiting gst file.                
"""
#now we will Create and configure logger
logging.basicConfig(filename="gstparser.log", 
					format='%(asctime)s %(message)s', 
					filemode='w')
#Let us Create an object 
logger=logging.getLogger()
#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)
#filename='td64.gst' 
#filename='ev174d-2si.gst'                
def parse_gst_data(filename):
    if not (os.path.exists(filename)):
       logger.error(f'The file {filename} does not exist.')
       raise FileNotFoundError(f'The file {filename} does not exist.')    
    #Name of the  information for in the gst file
    gst_name_header = []   
    #number of  columns for each load step
    ninfo_per_ls = []   
    #gst_column_info[frq,ncontpair,:] = [time, load step, substep,cum iter, ...] 
    gst_column_infof = []
    gst_column_infos = []   
    #local variables
    cntr = 0  
    ls_num=1 
    frq_num=0
    char_index=[]
    with open(filename, 'r') as reader:
        for line in reader:
            cntr = cntr + 1         
            if cntr == 1:                     # <SOLUTION> 
               pass 
            elif cntr == 2:                   # <LOADSTEPDATA>
               pass
            elif cntr == 3:                   # <HEADER>
                pass
            elif (line[2:11] == 'COLUMN ID'  and ls_num ==1):  # The column heading             
               gst_name_header.append(line[20:-10])
            elif line[2:7] == 'UNITS' :       # Reading UNITS Info   
                pass 
            elif line[2:-2] == 'HEADER' :     # Last line of the header              
                ninfo_per_ls = len(gst_name_header)  
                ls_num=ls_num+1                 
            elif(line[1:8] == 'COLDATA'):                    
                pass
            elif(line[:3].isspace()):
                nline = line.split()
                fline=[]
                sline=[]
                clmn=0
                if not char_index:                                   
                   for item in nline:
                       if (any(char.isdigit() for char in item)):
                           fline.append(float(item))                                                 
                       else:
                           sline.append(item) 
                           char_index.append(clmn)                           
                       clmn=clmn+1
                else:                    
                   for clmn in range(ninfo_per_ls):
                       if(clmn in char_index):
                           sline.append(nline[clmn]) 
                       else:
                           fline.append(float(nline[clmn]))
                                        
                gst_column_infof.append(fline)
                gst_column_infos.append(sline)
                frq_num=frq_num+1               
            else:
                pass   
    #Data in the cnd file is fetched
    logger.info(f'The file {filename} successfully read.')  
    logger.info(f'Number information per load step:  {ninfo_per_ls} .')
    logger.info(f'gst data is written  for {frq_num}  times. ')
    #short name  is avoided for the generality of the input parameters.     
       

    #converting the list into array
    gst_column_infof = np.array(gst_column_infof)
    #finding the index for the load and substep lines   
    ls_index=[]    
    sbs_index=[]
    for i in range(0,frq_num-1):
        cntr = gst_column_infof[i+1,1]-gst_column_infof[i,1]                
        if (cntr==1): 
            ls_index.append(i)        
        if ((gst_column_infof[i+1,2]-gst_column_infof[i,2])== 1 and cntr ==0):  
            sbs_index.append(i)
    #seprating float and string value headers        
    gst_name_headers=[]      
    for item in char_index:           
        gst_name_headers.append(gst_name_header[item])       
    for item in gst_name_headers:           
        gst_name_header.remove(item)     
    return gst_name_header,gst_name_headers,gst_column_infof,gst_column_infos,frq_num,ls_index,sbs_index
#testing the parse_cnd_data
#[gst_name_headerf,gst_name_headers,gst_column_infof,gst_column_infos,frq_num,ls_index,sbs_index]=parse_gst_data('td64.gst')
#[gst_name_headerf,gst_name_headers,gst_column_infof,gst_column_infos,frq_num,ls_index,sbs_index]=parse_gst_data('ev174d-2si.gst')
#print(*gst_name_headerf,sep='\n')
#print('\n')
#print(*gst_name_headers,sep='\n')
#print(gst_column_infof)
#print(*gst_column_infof,sep='\n')
#print(*gst_column_infos,sep='\n')
#print(frq_num) 
#exit()
font1='16px'
#App layout
app = dash.Dash(__name__, prevent_initial_callbacks=True) 
app.title = 'GST Visualizer'
app.layout = html.Div([
    html.Div(className='row', children=[
    html.Div(children=[    
    dcc.Upload(              
        html.Div([
            'Drag and Drop or ',
            html.A('Import gst File')
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
        }),               
        # Allow one or multiple files to be uploaded
        multiple=False,
        id='upload_gst_data'
        )
        ],style= dict(width='15%')), 
    
    html.Div(children=[
              html.Label(['Select X Value'], 
                   style={ 'font-size':font1,
                          'font-weight': 'bold', 
                          'text-align':  'center',
                          'offset': 5}
                ),             
              dcc.Dropdown(
                  id='xvalue_selection',
                  options=['Cum Iter'], 
                  value ='Cum Iter',
                  clearable=False                        
                ) 
        ],style=dict(width='10%')),
     
    html.Div(children=[
              html.Label(['Select Y Values'], 
                   style={'font-size': font1,
                           'font-weight': 'bold', 
                           "text-align": "center"}
                ),
              dcc.Dropdown(
                  id='yvalues_selection',
                  options =[],
                  multi =True,
                  clearable= True                
                )
        ],style=dict(width='25%')), 
        
    html.Div(children=[
              html.Label(['Select Vertical Lines'], 
                   style={'font-size': font1,
                           'font-weight': 'bold', 
                           "text-align": "center"}
                ),
              dcc.Dropdown(
                  id='vlines_selection',
                  options =['Load Step','SubStep', 'Bisection', 'Remesh'],
                  #value ='Load Step',
                  multi =True,
                  clearable= True                
                )
        ],style=dict(width='20%')), 
    ],style=dict(display='flex')),
    #html.Hr(),
    #html.Div(id='spreadsheet_container'),   
    html.Hr(),     
    dcc.Graph(id='graph_container', figure={})   
 ])
# #-------------------------------------------------------------------------------------
#upload_cnd_data
@app.callback(
    [     
     Output('yvalues_selection','options')
    ],
    [
     Input('upload_gst_data', 'filename')
    ]
    )
def upload_data(filename):
    global gst_name_headerf,gst_name_headers,gst_column_infof,gst_column_infos,frq_num,ls_index,sbs_index
    [gst_name_headerf,gst_name_headers,gst_column_infof,gst_column_infos,frq_num,ls_index,sbs_index]=parse_gst_data(filename)      
    return [gst_name_headerf]
#-------------------------------------------------------------------------------------
#plot the selected x-y graph
@app.callback(
    [
     #Output('spreadsheet_container','children'),
     Output('graph_container','figure')
    ],
    [  
    Input('xvalue_selection',   'value'),
    Input('yvalues_selection',  'value'),
    Input('vlines_selection',   'value')     
    ]
    )
def graph_gen(xvalue,yvalues,vlines):       
    global gst_name_headerf,gst_name_headers,gst_column_infof,gst_column_infos,frq_num,ls_index,sbs_index        
    if(xvalue == None):
       xvalue='Cum Iter'          
    if(yvalues == None):
       yvalues=['F   CRIT'] 
    if(vlines == None):
       vlines=['Load Step']      
    #check to remove  
    # xvalue=gst_name_headerf[gst_name_headerf.index(xvalue)]            
    # for p in range(len(yvalues)):
        # yvalues[p]=gst_name_headerf[gst_name_headerf.index(yvalues[p])]            
    df = pd.DataFrame(gst_column_infof, columns= gst_name_headerf)
    return [#dt.DataTable(        
                # id='datatable-interactivity',
                # columns=[
                # {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": True}            
                # for i in df.columns
                # ],
               # data=df.to_dict('records'), # the contents of the table
               # editable=True,              # allow editing of data inside all cells
               # filter_action="native",     # allow filtering of data by user ('native') or not ('none')
               # sort_action="native",       # enables data to be sorted per-column by user or not ('none')
               # sort_mode="single",         # sort across 'multi' or 'single' columns
               # column_selectable="multi",  # allow users to select 'multi' or 'single' columns
               # row_selectable="multi",     # allow users to select 'multi' or 'single' rows
               # row_deletable=False,        # choose if user can delete a row (True) or not (False) 
               # page_action="native",       # all data is passed to the table up-front or not ('none')
               # page_current=0,             # page number that user is on
               # # ids of columns that user selects
               # selected_columns=[],        #comb_long_name.index(yvalues),               
               # selected_rows=[],           # indices of rows that user selects
               # page_size=15,               # number of rows visible per page
               # style_header={
                    # 'backgroundColor': 'rgb(210, 210, 210)',
                    # 'color': 'black',
                    # 'fontWeight': 'bold'
                # },
               # style_cell={                # ensure adequate header width when text is shorter than cell's text
                   # 'minWidth': 110, 'maxWidth': 130, 'width': 100,
                   # #'font-family': 'cursive',
                   # #'font-size': '14px'
                # },
               # style_data={                # overflow cells' content into multiple lines
                 # 'whiteSpace': 'normal',
                 # 'height': 'auto',
                 # 'color': 'black',
                 # 'backgroundColor': 'white'            
                # },        
               # style_data_conditional=[
                # {# alternate color lines                    
                    # 'if': {'row_index': 'odd'},
                    # 'backgroundColor': 'rgb(220, 220, 220)' 
                # },
                
                # {    
                # 'if': {'column_id': xvalue},
                # 'background_color': '#808000'                                 
                # },
                
                # {                 
                # 'if': {'column_id': yvalues},
                # 'background_color': '#D2F3FF'
                # }               
                # ] 
                    
            # ),        
            graphgen(df, xvalue,yvalues,ls_index,sbs_index,vlines)        
        ]   
def graphgen(df,x,y,ls_index,sbs_index,vlines):
    fig = px.line(df,x,y)
    xx=df[x]    
    for item in vlines:                
        if (item == 'Bisection'):
            tmp=df[item]
            nz_index=[i for i, e in enumerate(tmp) if e != 0]            
            if nz_index:
               for i in nz_index:         
                   fig.add_vline(xx[i], line_width=2, line_dash="dash", line_color="red")
        if (item == 'SubStep' and sbs_index):
            for i in sbs_index:         
                fig.add_vline(xx[i], line_width=2, line_dash="dash", line_color="green") 
        if (item == 'Load Step' and ls_index):
            for i in ls_index:         
                fig.add_vline(xx[i], line_width=2, line_dash="dash", line_color="blue") 
        if (item == 'Remesh'):
            tmp=df[item]
            nz_index=[i for i, e in enumerate(tmp) if e != 0]
            if nz_index:
               for i in nz_index:         
                   fig.add_vline(xx[i], line_width=2, line_dash="dash", line_color="magenta")                
    return fig     
if __name__ == '__main__':
    app.run_server(debug=True)
