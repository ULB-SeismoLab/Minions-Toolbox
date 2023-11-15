import csv
import numpy as np
import datetime
import utm
import os 

def csv_export(filename, fields, ROW) :
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 

        # writing the fields 
        csvwriter.writerow(fields) 

        # writing the data rows 
        csvwriter.writerows(ROW)
        
def utm_converter(X, Y) :
    outX = []
    outY = []
    for i in range(len(X)) :
        UTM = utm.from_latlon(Y[i],X[i])
        outX.append(UTM[0]), outY.append(UTM[1])
    return outX, outY

def nodes_gnss_temp(root, nodenbr=None, startdate = None, enddate = None, utm_bool = False) :
    
    TEMP = []
    TEMPUTC = []
    GNSSUTC = []
    LAT = []
    LONG = []
    COMPASS = []
    TILT = []
    ALTI = []

    LATUTM = []
    LONGUTM = []
    
    acttemp = 0
    actgnss = 0
    
    path = root 
    
    if nodenbr != None :
        path = root+'DigiSolo_'+nodenbr+'.LOG'

    with open(path) as file :
        readcsv = csv.reader(file, delimiter=' ')
        line = 0
        for row in readcsv :
            if row != [] :
                if nodenbr == None and row[0].startswith('Serial') :
                    nodenbr = row[-1]
                if row[0].startswith('[Temperature') :
                    acttemp = 1 #active la boucle actemp
                if acttemp == 1 :
                    if row[0] == 'UTC' :
                        TEMPUTC.append(np.datetime64(row[-1].replace(',','T').replace('/','-')))
                    elif row[0] == 'Temperature' :
                        TEMP.append(float(row[2]))
                        acttemp = 0
                if len(row) > 3 and row[3] == 'GPS' and row[4]=='Synchronization' :
                    actgnss = 1 #active la boucle actgnss
                if actgnss == 1 :
                    if row[0] == 'Latitude':
                        lat = float(row[-1])
                        #WGS 84
                        LAT.append(lat)
                        LONG.append(long)
                        #UTM
                        UTM = utm.from_latlon(lat,long, force_zone_letter='W', force_zone_number=28)
                        LATUTM.append(UTM[1])
                        LONGUTM.append(UTM[0])
                        
                    elif row[0] == 'Longitude' :
                        long = float(row[-1])
                    elif row[0] == 'eCompass' :
                        COMPASS.append(float(row[-1]))
                    elif row[0] == 'UTC' :
                        GNSSUTC.append(np.datetime64(row[-1].replace(',','T').replace('/','-')))
                    elif row[0] == 'Tilted' :
                        TILT.append(float(row[-1]))
                    elif row[0] == 'Altitude' :
                        if row[-1] == 'Unknown' :
                            ALTI.append(ALTI[-1])
                        else :
                            ALTI.append(float(row[-1]))
                        actgnss = 0
    if startdate != None :
        startdate = np.datetime64(startdate)
        GNSSUTC = np.array(GNSSUTC)
        binaryGPS = np.where(GNSSUTC > startdate, 1, 0)
        binaryTEMP = np.where(TEMPUTC > startdate, 1, 0)
        if enddate != None :
            enddate = np.datetime64(enddate)
            GNSSUTC = np.array(GNSSUTC)
            binGPSend = np.where(GNSSUTC < enddate, 1, 0)
            binaryGPS *= binGPSend
            
            TEMPUTC = np.array(TEMPUTC)
            binTEMPend = np.where(TEMPUTC < enddate, 1, 0)
            binaryTEMP *= binTEMPend
            
            #print(binend)
            #print(binary)
        
   ##### Extracting the "needed" data based on the date binary array #####     
        
        #WGS84
        LAT = np.extract(binaryGPS, LAT)
        LONG =  np.extract(binaryGPS, LONG)
        #UTM
        LATUTM = np.extract(binaryGPS, LATUTM)
        LONGUTM =  np.extract(binaryGPS, LONGUTM)
                
        ALTI =  np.extract(binaryGPS, ALTI)
        GNSSUTC =  np.extract(binaryGPS, GNSSUTC)
        TILT =  np.extract(binaryGPS, TILT)
        COMPASS = np.extract(binaryGPS, COMPASS)
        
        TEMPUTC = np.extract(binaryTEMP, TEMPUTC)
        TEMP = np.extract(binaryTEMP, TEMP)
        
    ##### Save the position of the nodes over time #####                    
    if os.path.exists('./LogData/') == False :
        os.mkdir('./LogData/')
    
    POS = []
    headers = ['TIME','LONG','LAT']
    for i in range(len(LONG)) :
        POS.append([GNSSUTC[i],LONG[i],LAT[i]])
    
    csv_export('./LogData/pos_'+nodenbr+'.csv', headers, POS)
    
    outTEMP = []
    headers = ['TIME','TEMPERATURE']
    for i in range(len(TEMP)) :
        outTEMP.append([TEMPUTC[i],TEMP[i]])
    
    csv_export('./LogData/temp_'+nodenbr+'.csv', headers, outTEMP) 
    
    if utm_bool == True :
        return TEMP, TEMPUTC, GNSSUTC, LATUTM, LONGUTM, ALTI, COMPASS, TILT    
    
    return TEMP, TEMPUTC, GNSSUTC, LAT, LONG, ALTI, COMPASS, TILT