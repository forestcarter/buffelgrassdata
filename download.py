
import os
import shlex
import subprocess

def changedates(newdate,olddate,picname,year, julday,view):
     
    print("changing dates")
    htmlfile = open(os.path.join(os.getcwd(),"buffelapp","views",view),"r")
    print("html file is {}".format(htmlfile))
    readhtml=htmlfile.readlines()
    htmlfile.close()
    newhtml = open(os.path.join(os.getcwd(),"buffelapp","views",view),"w")
    
    mytext="updatedates{}".format(picname)
    myjulday="updatejulday"
    for num, line in enumerate(readhtml):           
        if mytext in line:
            print(mytext)
            print(line)
            targettext= "<strong>{5}.</strong>   {0}-{1} minus {2}-{3}      {4}".format(newdate-6,newdate,olddate-6,olddate, year,picname)
            texttowrite = "<p id='{0}' class='downloadable'>{1}</p>\n".format(mytext,targettext)
            newhtml.write(texttowrite)
        elif myjulday in line:
            newhtml.write("<p id='{0}'>Today is Day of Year {1}</p>\n".format(myjulday, julday))
        else:
            newhtml.write(line)
    newhtml.close()
    
def histdownload(newdate, olddate, picname, year):
    newdateworked=False
    olddateworked=False
    
    print("year is {}".format(year))
    staticPath = os.path.join(os.getcwd(),'static')
    if not os.path.isdir(staticPath):
        os.system("mkdir {}".format(staticPath))
                  
    filename4=os.path.join(staticPath,'histunzipped2')
    filename3=os.path.join(staticPath,'histunzipped')
    filename2=os.path.join(staticPath,'histindex.html.tmp')
                           
    if os.path.isdir(filename3):
        os.system('rm -rf {}'.format(filename3))
    os.system('mkdir {}'.format(filename3))
    print('removed histunzipped')
    if os.path.isdir(filename4):
        os.system('rm -rf {}'.format(filename4))
    os.system('mkdir {}'.format(filename4))
    print('removed histunzipped2')
    if os.path.isfile(filename2):
        os.system('rm {}'.format(filename2))

        
    endrange=str(olddate)
    endrange2=str(newdate)
    if len(endrange)==1:
        endrange="0"+endrange
    if len(endrange)==2:
        endrange="0"+endrange
    if len(endrange2)==1:
        endrange2="0"+endrange2
    if len(endrange2)==2:
            endrange2="0"+endrange2    
    

    #Download First Image

    indexFile = os.path.join(staticPath,'index.html.tmp')                       
    if os.path.isfile(indexFile):
        os.system("rm {}".format(indexFile))
                  

    dlhtml='/usr/bin/wget -O {2} --no-proxy -t 3 -o dlhtml1.txt --no-check-certificate -L --user=fcarter --password=dS6oaPNwEAB7 --no-parent -A "US_eMAE_NDVI.{0}.*.QKM.*.zip" https://dds.cr.usgs.gov/emodis/CONUS6/expedited/AQUA/{0}/comp_{1}/'.format(year,str(endrange),indexFile, staticPath)
    print(dlhtml)

    subprocess.call(shlex.split(dlhtml))

    #indexFile = os.path.join(staticPath,'index.html.tmp')                       
    if os.path.isfile(indexFile):
        olddateworked=True
        print("olddateworked set to true")
    else:
        print("olddate worked set to false {0} {1} {2} {3}")
    print("wget completed?")
    f1= open((indexFile), "r")
    f=f1.readlines()
    f1.close()
    print("marker1")
    for item in f:
        if "NDVI" in item and "QKM" in item and not ".sum" in item:
            target=item[9:68]
            print (target)
    download = '/usr/bin/wget --no-proxy -t 3 -o dldata1.txt -O {3}/ndvi1.zip --no-check-certificate -L --user=fcarter --password=dS6oaPNwEAB7 "https://dds.cr.usgs.gov/emodis/CONUS6/expedited/AQUA/{2}/comp_{0}/{1}"'.format(str(endrange), target, year, staticPath)
    print(download)
    subprocess.call(shlex.split(download))
    print("startingunzip")
    unzipCommand = "/usr/bin/unzip {1} -d {0}".format(os.path.join(staticPath,'histunzipped'),os.path.join(staticPath,'ndvi1.zip'))
    subprocess.call(shlex.split(unzipCommand))

    for item in os.listdir(os.path.join(staticPath,'histunzipped')):
        if "ACQI" in item:
            delacqi = "rm {}".format(os.path.join(staticPath,'histunzipped',item))
            subprocess.call(shlex.split(delacqi))
            
    #Download Second Image
    print("beginning second image")
    if os.path.isfile(filename2):
        os.system('rm {}'.format(filename2))
    
    if os.path.isfile(indexFile):
        os.system("rm {}".format(indexFile))

    dlhtml='/usr/bin/wget -O {2} --no-proxy -t 3 -o dlhtml2.txt --no-check-certificate -L --user=fcarter --password=dS6oaPNwEAB7 --no-parent -A "US_eMAE_NDVI.{0}.*.QKM.*.zip" https://dds.cr.usgs.gov/emodis/CONUS6/expedited/AQUA/{0}/comp_{1}/'.format(year,str(endrange2),indexFile, staticPath)
    print(dlhtml)
    subprocess.call(shlex.split(dlhtml))
    #os.system(dlhtml)
    #indexFile = os.path.join(staticPath,'index.html.tmp')                       
    if os.path.isfile(indexFile):
        newdateworked=True
        print("newdateworked set to true")
    else:
        print("newdate worked set to false {0} {1} {2} {3}")
    print("wget completed?")
    f1= open((indexFile), "r")
    f=f1.readlines()
    f1.close()
    print("marker1")
    for item in f:
        if "NDVI" in item and "QKM" in item and not ".sum" in item:
            target2=item[9:68]
            print (target2)
    download = '/usr/bin/wget --no-proxy -t 3 -o dlndvi2.txt -O {3}/ndvi2.zip --no-check-certificate -L --user=fcarter --password=dS6oaPNwEAB7 "https://dds.cr.usgs.gov/emodis/CONUS6/expedited/AQUA/{2}/comp_{0}/{1}"'.format(str(endrange2), target2, year, staticPath)
    print(download)
    subprocess.call(shlex.split(download))
    #os.system(download)
    unzipCommand2 = "/usr/bin/unzip {1} -d {0}".format(os.path.join(staticPath,'histunzipped2'),os.path.join(staticPath,'ndvi2.zip'))
    subprocess.call(shlex.split(unzipCommand2))
    #os.system("/usr/bin/unzip {1} -d {0}".format(os.path.join(staticPath,'histunzipped2'),os.path.join(staticPath,'ndvi2.zip')))
    #os.system("rm ndvi2.zip")

    for item in os.listdir(os.path.join(staticPath,'histunzipped2')):
        if "ACQI" in item:
            delacqi = "rm {}".format(os.path.join(staticPath,'histunzipped2',item))
            subprocess.call(shlex.split(delacqi))
            


#############

    print('t1 ', target)
    print('t2 ', target2)
    print ("done with download")
    print("{0}{1}".format(olddateworked,newdateworked))
    if newdateworked and olddateworked:
        print("True Returned")
        return True
        
    else:
        print("false returned")
        return False
        




