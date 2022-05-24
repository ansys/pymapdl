#**********************************************************************
# Importing  used libraries
#**********************************************************************
import sys
import os    
from enum import Enum
from decimal import Decimal
import copy
import numpy as np
import xlsxwriter
import matplotlib.pyplot as plt
def cndparser( filename, exclflg, contsrno, columinfo):
    """1. Reading a cnd file and storing the data in list and arrays.
       2. Writing the contact information in an excel sheet if requested (excflg = 1).
       3. Plotting a contact information for a contact pair if requested.  
        Parameters
        ----------
        filename : str
            Contact diagnosis input file with .cnd extention.
        exclflg  : int, in [0,1]
            if 1  spread sheet is generated
        contsrno : int, optional
            cont pair serial number for which a time evolution plot is requested.  
        columinfo: str, optional
            Short name of the column need to be plotted as lited in (NLHIST,CONT)            
    """
    if not (os.path.exists(filename)):
        sys.exit('The file, ' + filename +' does not exist.')     
    #**********************************************************************
    #String variables
    #**********************************************************************
    #Writing frequency of contact variables 
    #FRQ = ["ITERATION","SUBSTEP","LOAD_STEP"]
    #Name of the contact information for each pair 
    ContNameHeader = []
    #Name of the information for the each writing frequency
    LoadTimeHeader = [ 'LoadStep', 'SubStep', 'IterationNo', 'Time', 'Scaled Time for Wear' ]
    # Numeric variables
    #Information per contact pair
    nInfoPerPair = [] 
    #Number of contact pair
    paircount = 0  
    #ContPairInfo[frq,ncontpair,:] = [ContPair ID, p2, p3, ... nInfoPerContPair] 
    ContPairInfo = [] 
    #LoadTime[frq,:] = [ LoadStep, SubStep, IterationNo, Time, Scaled Time for Wear]
    LoadTime = []  
    #reading the full file line by line   
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
               ContNameHeader.append(line[20:-10])
            elif line[2:7] == 'UNITS' :       # Reading UNITS Info   
               pass 
            elif line[2:-2] == 'HEADER' :     # Last line of the header              
               nInfoPerPair = len(ContNameHeader)             
            elif((line[1:8] == 'COLDATA' or line[:3].isspace())):         
                if(line[1:8] == 'COLDATA'):
                   #<COLDATA LOAD_STEP="        1" SUBSTEP="        1" ITERATION="        4" TIME="   0.1000000    " PHYSICAL TIME FOR WEAR="   0.1000000    ">   
                   LoadTime.append(float(line[20:29])) # LOAD_STEP
                   LoadTime.append(float(line[40:49])) # SUBSTEP 
                   LoadTime.append(float(line[62:71])) # ITERATION
                   LoadTime.append(float(line[79:95])) # TIME 
                   paircount = 0
                   if(len(line) == 140):
                        LoadTime.append(float(line[121:136])) # PHYSICAL TIME FOR WEAR
                        scaletimeflg = 1                        
                   frq_num = frq_num + 1
                elif(line[:3].isspace()):                     
                   nline = list(map(float,line.split()))                                               
                   ContPairInfo.append(nline) 
                   paircount = paircount + 1
            else:
                pass  
        #Data in the cnd file is fetched             
        print( 'Number of contact pair: ' , paircount)
        print( 'Number information per contact pair: ' , nInfoPerPair)
        print('Contact data is written  for  ', frq_num , '   ', frq_nam+'S')
    if(contsrno > paircount):
       sys.exit('contact serial number ', contsrno, 'should be less than ', paircount)
    
    ShortName = list(ContNameHeader)        # <-- makes a *copy* of the list
    for col_num, data in enumerate(ContNameHeader):
        if(data == 'Contact Pair ID'):
            ShortName[ col_num] = 'CNID'     
        elif(data == 'Number of Contact Elements in Contact'):
            ShortName[ col_num] = 'ELCN'
        elif(data == 'Number of Contact Elements in Contact (Sticking)'):
            ShortName[ col_num] = 'ELST'
        elif(data == 'Max. Chattering Level'):
            ShortName[ col_num] = 'CNOS' 
        elif(data == 'Max. Penetration/Min. Gap'):
            ShortName[ col_num] = 'PENE'
        elif(data == 'Max. Geometric Gap'):
            ShortName[ col_num] = 'CLGP' 
        elif(data == 'Max. Normal Stiffness'):
            ShortName[ col_num] = 'KNMX' 
        elif(data == 'Min. Normal Stiffness'):
            ShortName[ col_num] = 'KNMN'
        elif(data == 'Max. Resulting Pinball'):
            ShortName[ col_num] = 'PINB'
        elif(data == 'Max. Elastic Slip Distance'):
            ShortName[ col_num] = 'ESLI'
        elif(data == 'Max. Tangential Stiffness'):
            ShortName[ col_num] = 'KTMX'
        elif(data == 'Min. Tangential Stiffness'):
            ShortName[ col_num] = 'KTMN'
        elif(data == 'Max. Sliding Distance of Entire Solution'):
            ShortName[ col_num] = 'SLID'
        elif(data == 'Max. Contact Pressure'):
            ShortName[ col_num] = 'PRES'
        elif(data == 'Max. Friction Stress'):
            ShortName[ col_num] = 'SFRI'
        elif(data == 'Average Contact Depth'):
            ShortName[ col_num] = 'CNDP'
        elif(data == 'Max. Geometric Penetration'):
            ShortName[ col_num] = 'CLPE'
        elif(data == 'Number of Contact Points Have Too Much Penetration'):
            ShortName[ col_num] = 'LGPE' 
        elif(data == 'Contacting Area'):
            ShortName[ col_num] = 'CAREA'
        elif(data == 'Max. Contact Damping Pressure'):
            ShortName[ col_num] = 'NDMP'
        elif(data == 'Max. Contact Damping Tangential stress'):
            ShortName[ col_num] = 'TDMP'
        elif(data == 'Max. Sliding Distance including near field'):
            ShortName[ col_num] = 'GSMX'
        elif(data == 'Min. Sliding Distance including near field'):
            ShortName[ col_num] = 'GSMN'
        elif(data == 'Max. normal fluid penetration pressure on contact surface'):
            ShortName[ col_num] = 'FPSC'
        elif(data == 'Max. normal fluid penetration pressure on target surface'):
            ShortName[ col_num] = 'FPST'
        elif(data == 'Total volume loss due to wear on contact surface'):
            ShortName[ col_num] = 'WEAR'
        elif(data == 'Total strain energy due to contact'):
            ShortName[ col_num] = 'CTEN'
        elif(data == 'Frictional dissipation energy'):
            ShortName[ col_num] = 'CFEN'
        elif(data == 'Contact damping dissipation energy'):
            ShortName[ col_num] = 'CDEN'
        elif(data == 'WB contact pair ID'):
            ShortName[ col_num] = 'WBCNID'
        elif(data == 'Total contact force due to pressure -x component'):
            ShortName[ col_num] = 'CFNX'
        elif(data == 'Total contact force due to pressure -y component'):
            ShortName[ col_num] = 'CFNY' 
        elif(data == 'Total contact force due to pressure -z component'):
            ShortName[ col_num] = 'CFNZ'
        elif(data == 'Maximum torque in axisymmetric analysis with MU=1.0'):
            ShortName[ col_num] = 'CTRQ'            
        elif(data == 'Total contact force due to tangential stress -x component'):
            ShortName[ col_num] = 'CFSX'
        elif(data == 'Total contact force due to tangential stress -y component'):
            ShortName[ col_num] = 'CFSY'
        elif(data == 'Total contact force due to tangential stress -z component'):
            ShortName[ col_num] = 'CFSZ'
        elif(data == 'Number of Contact Points Have Too Much sliding'):
            ShortName[ col_num] = 'LGSL'
        elif(data == 'Contact pair force convergence norm'):
            ShortName[ col_num] = 'NORM'
        elif(data == 'Contact pair force criterion'):
            ShortName[ col_num] = 'CRIT'
        elif(data == 'Max. tangential fluid penetration pressure on contact surface'):
            ShortName[ col_num] = 'FPTC'
        elif(data == 'Max. tangential fluid penetration pressure on target surface'):
            ShortName[ col_num] = 'FPTT' 
        elif(data == 'Max. sliding distance of current substep for closed contact'):
            ShortName[ col_num] = 'SLMX'
        else:
            sys.exit('ShortName is not assigned for  ', data)  
    if (columinfo  in ShortName):
        col_numo = ShortName.index(columinfo)
        #print(col_num, ShortName[col_num])        
        #print(*ShortName,sep='\n')
    else:
        sys.exit('The provided ShortName, ' + columinfo + ' is not in the list')               
    PairIds = []
    if (scaletimeflg == 1):
        fqnum = 5
    else:
        fqnum = 4    
    for pair in range(paircount):
        PairIds.append(int(ContPairInfo[pair][0])) 
    #converting the list into array,     
    ContPairInfo = np.array(ContPairInfo)
    if (exclflg == 1):
        #**********************************************************************
        #Writing the data into an excel file
        #Contact information is written in seprate sheet in the file
        #**********************************************************************        
        workbook = xlsxwriter.Workbook(filename[:-4]+'.xlsx')
        cell_format1 = workbook.add_format({'bold': True, 'font_color': 'black'})
        cell_format1.set_font_size(10)
        #cell_format1.set_bg_color('gray')
        cell_format1.set_font_name('calibri')
        cell_format1.set_align('center')
        cell_format1.set_valign('center')
        #cell_format1.set_rotation(90)
        cell_format1.set_text_wrap()
        for pair in range(paircount):
            pairid = PairIds[pair] 
            #First write the headings for each pair in seprate sheet    
            worksheet = workbook.add_worksheet('ContPairID_'+str(pairid))    
            worksheet.write(0,0, LoadTimeHeader[3],cell_format1)
            for col_num, data in enumerate(ShortName[1:]):
                worksheet.write(0,col_num+1, data,cell_format1)
        #Write contact pair data  for a pair at each frequency point 
        cntr = 0 
        for frq in range(frq_num):        
            data = LoadTime[frq*fqnum+3]
            worksheet.write(frq+1,0, data) 
            for col_num, data in enumerate(ContPairInfo[cntr,1:]):
                worksheet.write(frq+1,col_num+1, data)      
            cntr = cntr + paircount
        workbook.close()
        print('Writing contact data in the excel file, ', filename[:-4]+'.xlsx', ' is completed.')
    #**********************************************************************
    #Ploting a contactpair information over the time
    #**********************************************************************      
    cnid = contsrno-1    
    #start:end:increment
    data1 = []
    data2 = []
    data1 = LoadTime[3:fqnum*frq_num:fqnum]
    data2 = ContPairInfo[cnid:paircount*frq_num:paircount,col_numo]
    #figsize lets use say how big the figure (our canvas) should be in inches (horizontal by vertical)
    fig = plt.figure(figsize=(10.5, 7.5))
    ax = fig.add_subplot()
    #set the labels for each plot starting with ax1
    ax.set_ylabel(ContNameHeader[col_numo])
    ax.set_xlabel('Time')  
    fig.suptitle(filename[:-4]+'_'+ShortName[col_numo] )
    #ax.title(filename)
    fig.tight_layout()  
    plt.plot(data1, data2)
    plt.show()
    #Finally we can save the figure as the filename but with .png instead of .txt
    fig.savefig(filename[:-4]+'_'+ShortName[col_numo] + '.png')
if __name__== "__main__":
    cndparser(str(sys.argv[1]), int(sys.argv[2]),int(sys.argv[3]),str(sys.argv[4]))