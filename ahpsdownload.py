import os
import datetime
import subprocess
import shlex

def changedates(julday, view):
    print("changing dates")
   
    htmlfile = open(os.path.join(os.getcwd(),"buffelapp","views",view),"r")
    readhtml=htmlfile.readlines()
    htmlfile.close()
    newhtml = open(os.path.join(os.getcwd(),"buffelapp","views",view),"w")
    mytext="updatep"
    
    for num, line in enumerate(readhtml):           
        if mytext in line:
            print(mytext)
            print(line)
            targettext=julday
            
            texttowrite = "<p id='{0}'>Precipitation data updated Day of Year {1}</p>\n".format(mytext,targettext)
            newhtml.write(texttowrite)
       
        else:
            newhtml.write(line)
    newhtml.close()
    
def histdownload(precipdays, delay, startday):

 
    staticPath = os.path.join(os.getcwd(),'static', 'precipdata')
    if os.path.isdir(staticPath):
        subprocess.call(shlex.split("rm -r {}".format(staticPath)))
    subprocess.call(shlex.split("mkdir {}".format(staticPath)))
    
    for back1 in xrange(precipdays):
    
        date1=startday-datetime.timedelta(days=(back1+int(delay)))
        print ("Downloading Precip date {}".format(date1))
        download = '/usr/bin/wget --no-proxy -t 3 -O {3}/precip1_{4}.tif --no-check-certificate "https://water.weather.gov/precip/downloads/{0}/{1}/{2}/nws_precip_1day_{0}{1}{2}_conus.tif"'.format(str(date1)[:4],str(date1)[5:7],str(date1)[8:10], staticPath, back1+1)
        print download
        subprocess.call(shlex.split(download))


        

        
