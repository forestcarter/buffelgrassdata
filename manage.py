import datetime
import os
import download
import process
import ahpsdownload
import ahpsprocess

os.chdir(os.path.dirname(os.path.realpath(__file__)))
preciplag=0
zoomout=10
zoomin=15
dlcurrent=True
dlhist=True
dlprecipitation=True
precipdays=24
today=str(datetime.datetime.now())
startday=datetime.datetime.now()-datetime.timedelta(days=preciplag)
s="{0}{1}{2}".format(today[8:10], today[5:7],today[:4])
n= datetime.date.toordinal(datetime.date(int(s[4:8]), int(s[2:4]), int(s[0:2])))-125
julday=n%365+1
print ("startday is {}".format(startday))
olddate=str(julday-8)
newdate=str(julday-1)
landingvar="landing.ejs"
downloadvar="download.ejs"

pages=[1,2,3,4]
histpages=[5,6,7,8]
newdate = [julday-1,julday-8, julday-15, julday-22]
olddate = [julday-8,julday-15, julday-22, julday-29]
julday2=224
histnewdate = [julday2-1,julday2-8, julday2-15, julday2-22]
histolddate = [julday2-8,julday2-15, julday2-22, julday2-29]


#Historical
if dlhist==True:
    for num in xrange(len(histpages)):
        try:
            if download.histdownload(histnewdate[num], histolddate[num], histpages[num],"2017"):
                print ("dlworked")
                download.changedates(histnewdate[num], histolddate[num], histpages[num],"2017",julday,landingvar)
                download.changedates(histnewdate[num], histolddate[num], histpages[num],"2017",julday,downloadvar)
                process.process(histnewdate[num], histolddate[num], histpages[num],"2017",zoomout,zoomin,"rmd")
                process.process(histnewdate[num], histolddate[num], histpages[num],"2017",zoomout,zoomin,"tmd")
                print ("Completed request {} ".format(num))
        except Exception as e:
            print(" failed {0} {1} {2} {3}".format(histnewdate[num], histolddate[num], histpages[num],"2017"))
            print (e)
if dlcurrent==True:
    for num in xrange(len(pages)):  
        try:
            if download.histdownload(newdate[num], olddate[num], pages[num],today[:4]):
                print ("dlworked")
                download.changedates(newdate[num], olddate[num], pages[num],today[:4],julday,landingvar)
                download.changedates(newdate[num], olddate[num], pages[num],today[:4],julday,downloadvar)
                process.process(newdate[num], olddate[num], pages[num],today[:4],zoomout,zoomin,"rmd")
                process.process(newdate[num], olddate[num], pages[num],today[:4],zoomout,zoomin,"tmd")
                print ("Completed request {} ".format(num))
        except Exception as e2:
            print(" failed {0} {1} {2} {3}".format(newdate[num], olddate[num], pages[num],today[:4]))
            print(e2)


if dlprecipitation==True:
    
    for delay in ["01","05","09","13","17"]:
        ahpsdownload.histdownload(precipdays,delay,startday)
        ahpsprocess.ahpsprocess(7, 13, precipdays, delay)
    ahpsdownload.changedates(julday, landingvar)
