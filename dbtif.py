# Set environment variables for database connection
import  subprocess

subprocess.call(shlex.split("set PGUSER=root"))
subprocess.call(shlex.split("set PGDATABASE=ndvidb"))

tiflist=["dbold.tif","dbnew.tif"]
projnum="4226"



#set PGHOST=db.qgiscloud.com
#set PGPORT=5432

#set PGPASSWORD=enter_qgiscloud_pw
#set PGDATABASE=ndvidb




# Call the raster2pqsql utility

schema="public"

for myfile in tiflist:
    
    mypath = os.path.join(os.getcwd(),'buffelapp','public',"tiles","dbtif",)

    subprocess.call(shlex.split("raster2pgsql -s {0} -C -F -t auto {1} {2}.{3} | psql").format(projnum,mypath,schema,myfile[:5]))
