# -*- coding: utf-8 -*-
"""
Python implementation of CDB reader
"""
import gc
import numpy as np
import copy

def Read(filename):
    """
    Reads ASCII CDB from ANSYS and returns elem_type, nnum, nodes, enum, elem,
    fixed
    
    USAGE:
    raw = ReadCDB(filename)
    
    where raw contains the fields:
    'ekey':  Element type keys
    'nnum':  Node numbering according to ANSYS
    'nodes': Node locations
    'enum':  Element numbers according to ANSYS
    'elem':  ANSYS Element matrix
    'etype': Element types
    
    """

    # Node components    
    node_comps = {}
    nfpos = -1 # NBLOCK numbering starting position
    efpos = -1 # EBLOCK numbering starting position
    
    # Read file as an iterator
    with open(filename) as fileObj:
        fpos = 0 # track position in file

        # Parse element types and read RLBLOCK
        elem_type = []
        rnum = []
        rdat = []
        for line in fileObj:
            fpos += len(line)
            if 'ET,' in line[:3]:
                elem_type.append(ParseEType(line))
                
            elif 'RLBLOCK' in line:
                rnum, rdat, fpos = RLBLOCK_Reader(fileObj, fpos, line)

            elif 'NBLOCK' in line:
                nfpos, fpos, n_isz, nfields, n_fsz, nnode = NBLOCK_Info(fileObj, line, fpos)
        
            elif 'EBLOCK' in line:
                # Identify element block location
                fpos, e_isz = EBLOCK_Info(fileObj, line, fpos)
                efpos = copy.copy(fpos) # Copy location of element block

            elif 'CMBLOCK' in line and 'NODE' in line:
                # Read node components
                comname, c_nodes = CMBLOCK_Reader(fileObj, line)
                node_comps[comname] = c_nodes 
    
    ############### End reading file as an iterator ############

    # Open file as a buffer
    fileObj = open(filename)

    # Read the block that comes first
#    if nfpos < efpos and nfpos != -1:
    if nfpos != -1:
        nnum, nodes = NBLOCK_Reader(filename, nfpos, n_isz, nfields, n_fsz, nnode)
        
    # Read element block (if it exists)
    if efpos != -1:
        etype, enum, elem, e_rcon = EBLOCK_Reader(filename, efpos, e_isz)
    else:
        etype = []
        enum = []
        elem = [[]]
        e_rcon = []
    
                                  
    # Return numpy arrays
    raw = {'rnum': np.asarray(rnum),
           'rdat': np.asarray(rdat),
           'ekey': np.array(elem_type),
           'nnum': nnum,
           'nodes': nodes,
           'enum': np.array(enum),
           'elem': np.array(elem, np.int32),
           'etype': np.array(etype, np.int32),
           'e_rcon': np.asarray(e_rcon),
           'node_comps': node_comps}

    # Garbage collect
    del elem_type, nnum, nodes, enum, elem, etype, node_comps
    gc.collect()
    
    return raw
    
    
def EBLOCK_Info(fileObj, line, fpos):
    """
    Get interger block size and store start position (fpos) for the
    element block
    """

    # Get total block size
    try:
        bsize = int(line[int(line.rfind(',')) + 1:])
        
        # Get block size and starting position of EBLOCK
        for line in fileObj:
            fpos += len(line)
            e_isz = int(line[line.find('i') + 1:line.find(')')])
            break
        
        # Seek to end of block
        c = 0
        for line in fileObj:
            c += 1
            if c > bsize:
                break
        
    except:
        # Get block size and starting position of EBLOCK
        for line in fileObj:
            fpos += len(line)
            e_isz = int(line[line.find('i') + 1:line.find(')')])
            break
        
        # Seek to end of block
        for line in fileObj:
            try:
                if int(line) == -1:
                    break
            except:
                continue
        
    return fpos, e_isz
    
    
def NBLOCK_Info(fileObj, line, fpos):
    """
    Get interger block size and store start position (fpos) for the node block
    """

    # Get total block size
    # Try to get total number of nodes
    try:
        nnode = int(line[int(line.rfind(',')) + 1:])
    except:
        nnode = -1
    
    # Get block size and starting position of EBLOCK
    for line in fileObj:
        fpos += len(line)
        i_sz = int(line[line.find('i') + 1:line.find(',')])
        nfields = int(line[line.find(',') + 1:line.find('e')])
        f_sz = int(line[line.find('e') + 1:line.find('.')])
        break
    
    # Store starting nblock position for future seek
    nstart = copy.copy(fpos)
    
    # If number of nodes has been obtained
    if nnode != -1:
        # Seek to end of block
        c = 0
        for line in fileObj:
            fpos += len(line)
            c += 1
            if c > nnode:
                break
    else:
        # Manually to end of block
        c = 0
        for line in fileObj:
            fpos += len(line)
            try:
                if int(line) == -1:
                    break
                c += 1
            except:
                continue
            
        # Number of lines is equal to the number of nodes
        nnode = c
        
    return nstart, fpos, i_sz, nfields, f_sz, nnode
    
    
def ParseEType(line):
    """ Returns element type and element number """
    elnum = int(line[3:line.find(',', 5)]) # element number
    etype = int(line[line.find(',', 5) + 1:]) # element type
    return [elnum, etype]


def RLBLOCK_Reader(fileObj, fpos, line):
    """
    Reads RLBLOCK from ANSYS *.cdb 
    
    RLBLOCK Format:
    RLBLOCK,NUMSETS,MAXSET,MAXITEMS,NPERLINE
    Format1
    Format2 
    
    Format1
    Data descriptor defining the format of the first line. For the RLBLOCK
    command, this is always (2i8,6g16.9).  The first i8 is the set number, the
    second i8 is the number of values in this set, followed by up to 6 real
    constant values.    
 
   """

    # Get number of sets
    ist = line.find(',') + 1
    ien = line[ist:].find(',') + ist
    nset = int(line[ist:ien])

    # Skip Format1 (always 2i8,6g16.9)
    for line in fileObj:
        fpos += len(line)
        break
    
    # Skip Format 2 (always 7g16.9)
    for line in fileObj:
        fpos += len(line)
        break
    
    # Read data
    rnum = []
    rdat = []
    c_set = 0
    for line in fileObj:
        fpos += len(line)
        rcon = [] # real constants
        
        c_set += 1
        if c_set > nset:
            break
        
        # Get real constant number
        rnum.append(int(line[:8]))
        
        # Number of constants
        ncon = int(line[8:16])
        
        # Get constant data
        if ncon > 6: # if multiple lines
            for i in range(6):
                rcon.append(float(line[16 + 16*i:32 + 16*i]))
                ncon -= 1
                
            # advance line
            for line in fileObj:
                fpos += len(line)
                break   
             
            # read next line
            while True:
                if ncon > 7:
                    for i in range(7):
                        rcon.append(float(line[16*i:16*(i + 1)]))
                        ncon -= 1
                        
                    # advance
                    for line in fileObj:
                        fpos += len(line)
                        break
                        
                else:
                    for i in range(ncon):
                        try:
                            rcon.append(float(line[16*i:16 + 16*i]))  
                        except:
                            rcon.append(0.0)
                        
                    break
                
        # If only one in constant data
        else:
            for i in range(ncon):
                rcon.append(float(line[16 + 16*i:32 + 16*i]))   
                ncon -= 1

        rdat.append(rcon)
                        
    return rnum, rdat, fpos

    
def CMBLOCK_Reader(fileObj, line):
    """ Reads a componenet block """
    # Get component name and nodes
    ind1 = line.find(',') + 1
    ind2 = line.find(',', ind1)
    comname = line[ind1:ind2]
    nodes = ComponentInterperter(GetComponent(fileObj))

    return comname, nodes
    
    

def NBLOCK_Reader(filename, nfpos, n_isz, nfields, n_fsz, nnode):
    """ Read NBLOCK """
    
    # Seek the start of the NBLOCK
    fileObj = open(filename)
    fileObj.seek(nfpos)
    
    nnum = np.empty(nnode, np.int32)
    nodes = np.zeros((nnode, nfields))
    for i in range(nnode):
            
        # Field 1 - Node number
        string = fileObj.read(n_isz)
        nnum[i] = int(string)
        
        # Ignore fields 2 and 3
        fileObj.read(n_isz*2) # ignored
        
        # Read fields 4-9 (or 4-6)
        for j in range(nfields):
            # Check if next character is an eol character
            bcheck = fileObj.read(1)
            if '\r' in bcheck: # if dos EOL
                # read the next eol character and continue
                fileObj.read(1)
                break
            
            elif '\n' in bcheck:
                break
            
            else:
                # Read remaining characters and convert to float
                nodes[i, j] = float(bcheck + fileObj.read(n_fsz - 1))
    
        # If all fields have been read
        if j == nfields - 1:
            bcheck = fileObj.read(1)
            if '\r' in bcheck:
                # read the next eol character and continue
                fileObj.read(1)

    # Close file                
    fileObj.close()
                
    # Return node numbers and node positions
    return nnum, nodes


def EBLOCK_Reader(filename, fpos, isz):
    """ Reads an element block
    
    Field 1 - The material number.
    Field 2 - The element type number.
    Field 3 - The real constant number.
    Field 4 - The section ID attribute (beam section) number. See elements BEAM188 and BEAM189 for more information.
    Field 5 - The element coordinate system number.
    Field 6 - The birth/death flag.
    Field 7- The solid model reference number.
    Field 8 - The element shape flag.
    Field 9 - 0
    Field 10 - The exclude key (p-elements).
    Field 11 - The element number.
    Field 12-19 - The node numbers. The next line will have the additional node numbers if there are more than eight
    """
    
    # Open and seek the start of the EBLOCK
    fileObj = open(filename)
    fileObj.seek(fpos)
    
    etype = []
    enum = []
    elem = []
    e_rcon = [] # real constant
    
    # Read on a block basis
    while True: # Run until reaching eblock
    
        # Field 1 - The material number.
        block = fileObj.read(isz) # do not store
    
        # Check if block contains an end of a line
        if '\r\n' in block:
            block = block[2:] + fileObj.read(2)
        elif '\n' in block:
            block = block[1:] + fileObj.read(1)
    
        # Check if at end of EBLOCK
        if '-1' in block:
            break
        
        # Field 2 - The element type number.
        etype.append(int(fileObj.read(isz)))
        
        # Field 3 - The real constant number.
        e_rcon.append(int(fileObj.read(isz)))

        # Skip fields 4 - 8
        fileObj.seek(isz*5, 1)
    
        # Field 9 - Number of nodes in the element
        nnode = int(fileObj.read(isz))
            
        # Field 10 - The exclude key (p-elements).
        fileObj.seek(isz, 1) # do not store
        
        # Field 11 - The element number.    
        enum.append(int(fileObj.read(isz)))
        
        # Read nodes
        eline = []
        while len(eline) < nnode:
            
            # Read a block
            block = fileObj.read(isz)
            
            # Check if a block contains an end of a line
            if '\r\n' in block:
                block = block[2:] + fileObj.read(2)
            elif '\n' in block:
                block = block[1:] + fileObj.read(1)
                
            nodenum = int(block)
            eline.append(nodenum)

    
        eline.extend((-1,)*(20 - nnode))
        elem.append(eline)
    
    fileObj.close()
        
    return etype, enum, elem, e_rcon#, nnode
    
    
def GetComponent(fileObj):
    """ Extract fixed nodes from fileObj """
    component = []
    for line in fileObj:
         
        # Get interger size
        isz = int(line[line.find('i') + 1:line.find(')')])
        
        # Number of intergers
        nblock = int(line[line.find('(') + 1:line.find('i')])
        break
            
    for line in fileObj:
        for i in range(nblock):
            try:
                component.append(int(line[isz*i:isz*(i + 1)]))
            except:
                return component # exit when complete
        
        
def GetBlockFormat(formatstring):
    """ Get node block format """
    
    # Digit Size
    d_size = int(formatstring[formatstring.find('i') + 1:formatstring.find(',')])
    f_size = int(formatstring[formatstring.find('e') + 1:formatstring.find('.')])
    
    # Node end
    idx = [d_size, d_size*3]
    
    # Node location indicies
    for i in range(3):
        idx.append(idx[-1] + f_size)
    
    return idx


def ComponentInterperter(fixed):
    """
    If a node is negative, it is describing a list from the previous node.  This is ANSYS's way of 
    saving file size when writing components.
    
    """
    
    f_new = []
    for i in range(len(fixed)):
        if fixed[i] > 0: # Append if positive
            f_new.append(fixed[i])
        else: # otherwise, append list
            f_new.append(range(abs(fixed[i - 1]) + 1, abs(fixed[i]) + 1))
    
    return np.hstack(f_new)