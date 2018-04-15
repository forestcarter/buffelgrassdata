# Set environment variables for database connection
import os
import subprocess
import shlex
#subprocess.call(shlex.split("echo hi"))

folderpath = os.path.join(os.getcwd(),'buffelapp','public',"tiles","dbvrt")
vrtlist=[]
for item in os.listdir(folderpath):
    if item[-4:]==".vrt":
        vrtlist.append(item)


projnum="4226"
schema="public"

for item in vrtlist:

    
    itempath= os.path.join(folderpath,item)
    mystring =("raster2pgsql -s {0} -I -C -M {1} -F -t 105x62 {2}.{3} | psql -d ndvidb").format(projnum,itempath,schema,item[:10])
    

    os.system(mystring)

