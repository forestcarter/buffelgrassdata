import os 
import subprocess
import shlex
def process(newdate, olddate, picname, year, outzoom, inzoom, district, num=1):    

    print ("starting process.py")
    
    if district=="rmd":
        xmin=-110.761518
        xmax=-110.4760646
        ymin=32.1035758
        ymax=32.2712308
    if district=="tmd":
        xmin=-111.264
        xmax=-111.054
        ymin=32.229
        ymax=32.369    
    mypath = os.path.join(os.getcwd(),'static')
    pypath="/usr/bin/python"
    mainpath = "/usr/bin/" 
    print("step1")
    print(os.listdir(os.path.join(mypath,'histunzipped')))
    for item in os.listdir(os.path.join(mypath,'histunzipped')):
        if 'QKM.VI_NDVI' in item and item[-3:]=='tif':
            oldtif=os.path.join(mypath,'histunzipped',item)
            oldtifname=item
            print("found old ndvi")
        if 'QKM.VI_QUAL' in item and item[-3:]=='tif':
            oldqual=os.path.join(mypath,'histunzipped',item)
            print("found old qual")
    for item2 in os.listdir(os.path.join(mypath,'histunzipped2')):
        if 'QKM.VI_NDVI' in item2 and item2[-3:]=='tif':
            newtif=os.path.join(mypath,'histunzipped2',item2)
            newtifname=item2
            print("found new ndvi")
        if 'QKM.VI_QUAL' in item2 and item2[-3:]=='tif':
            newqual=os.path.join(mypath,'histunzipped2',item2)
            print("found new qual")
    print("step2")            
    projfirstcalc = os.path.join(mypath,"histprojfirstcalc.vrt")
    projfirstnew = os.path.join(mypath,"histprojfirstnew.vrt")
    projfirstold = os.path.join(mypath,"histprojfirstold.vrt")
    projclippednew=os.path.join(mypath,"histprojclippednew.vrt")
    projclippedold=os.path.join(mypath,"histprojclippedold.vrt")
    
    colorvrt=os.path.join(mypath,"colorvrt.vrt")
    rgbvrt=os.path.join(mypath,"rgbvrt.vrt")
    #colorpng=os.path.join(mypath,"buffelapp/public/colorpng.png")
    tilefolder=os.path.join(os.getcwd(),'buffelapp','public','tiles')
    downloadfolder=os.path.join(tilefolder,'downloads')
    dbvrtfolder=os.path.join(tilefolder,'dbvrt')
    ndvitif=os.path.join(downloadfolder,"ndvi{0}{1}.tif".format(picname,district))
    qualtif=os.path.join(downloadfolder,"qual{0}{1}.tif".format(picname,district))                     

    #new db variables
    dbfilename="{0}{1}{2}.tif".format(district,'%03d'%newdate,year)
    projclippednewdb=os.path.join(dbvrtfolder,dbfilename)

        #NDVI
    print os.getcwd()
   
    print type(tilefolder)
    if os.path.isdir(tilefolder)==False:
        print("step4")
        subprocess.call(shlex.split("mkdir {}".format(tilefolder)))
        subprocess.call(shlex.split("mkdir {}".format(downloadfolder)))
        for newdist in ["tmd","rmd"]:
            for newpicname in xrange(1,9):
                for newtype in ['ndvi','qual']:
                   print("step5")
                   subprocess.call(shlex.split("mkdir {}".format(os.path.join(tilefolder,newpicname,newdist,newtype))))

    ndvifolder=os.path.join(tilefolder,district,str(picname),'ndvi')
    print(ndvifolder)
    subprocess.call(shlex.split("{2}gdalwarp -s_srs EPSG:2163 -t_srs EPSG:4326 -of VRT -overwrite {0} {1} ".format(newtif, projfirstnew,mainpath)))
    subprocess.call(shlex.split("{2}gdalwarp -s_srs EPSG:2163 -t_srs EPSG:4326 -of VRT -overwrite {0} {1} ".format(oldtif, projfirstold,mainpath)))
    subprocess.call(shlex.split("{6}gdal_translate {0} {1} -of VRT -projwin {2} {3} {4} {5}".format(projfirstnew, projclippednew, xmin,ymax, xmax,ymin,mainpath)))
    subprocess.call(shlex.split("{6}gdal_translate {0} {1} -of VRT -projwin {2} {3} {4} {5}".format(projfirstold, projclippedold, xmin,ymax, xmax,ymin,mainpath)))
    #Save raw values for database
    
    if num==0:
        
        subprocess.call(shlex.split("{6}gdal_translate {0} {1} -of GTiff -projwin {2} {3} {4} {5}".format(projfirstnew, projclippednewdb, xmin,ymax, xmax,ymin,mainpath)))
        
        projnum="4326"
        schema="public"   
        districtDim = {"rmd":"105x62", "tmd":"77x51"}

        mystring =("raster2pgsql -s {0} -I -C -M {1} -F -t {4} {2}.{3} | psql -d ndvidb").format(projnum,projclippednewdb,schema,dbfilename[:10],districtDim[district])
   
        os.system(mystring)
        subprocess.call(shlex.split("rm {0}".format(projclippednewdb)))
    calc = "A-B"

        #New minus old, high values have greened up
    subprocess.call(shlex.split("{5} {4}gdal_calc.py -A {0} -B {1} --outfile={2} --calc={3} --overwrite".format(projclippednew,projclippedold,projfirstcalc,calc, mainpath,pypath)))
    
    subprocess.call(shlex.split("{1}gdal_translate -of GTiff {0} {2}".format(projfirstcalc, mainpath, ndvitif)))    
    subprocess.call(shlex.split("{2}gdaldem color-relief -of VRT {0} {3} {1}".format(projfirstcalc,colorvrt,mainpath,os.path.join(os.getcwd(),'colors.txt'))))
    subprocess.call(shlex.split("cp {0} {1}".format(os.path.join(os.getcwd(),'colors.txt'),os.path.join(os.getcwd(),'buffelapp','public', 'colors.txt'))))
    subprocess.call(shlex.split("{1}gdal_translate {0} {2}".format(colorvrt, mainpath, rgbvrt)))

    subprocess.call(shlex.split("{0}gdal2tiles.py -z {2}-{3} {1} {4} ".format(mainpath,colorvrt, outzoom, inzoom,ndvifolder)))

    #Qual
   
    qualfolder=os.path.join(tilefolder,district,str(picname),'qual')        
    subprocess.call(shlex.split("{2}gdalwarp -s_srs EPSG:2163 -t_srs EPSG:4326 -of VRT -overwrite {0} {1} ".format(newqual, projfirstnew,mainpath)))
    subprocess.call(shlex.split("{2}gdalwarp -s_srs EPSG:2163 -t_srs EPSG:4326 -of VRT -overwrite {0} {1} ".format(oldqual, projfirstold,mainpath)))
    subprocess.call(shlex.split("{6}gdal_translate {0} {1} -of VRT -projwin {2} {3} {4} {5}".format(projfirstnew, projclippednew, xmin,ymax, xmax,ymin,mainpath)))
    subprocess.call(shlex.split("{6}gdal_translate {0} {1} -of VRT -projwin {2} {3} {4} {5}".format(projfirstold, projclippedold, xmin,ymax, xmax,ymin,mainpath)))
    qualcalc = "A+B"

        #New minus old, high values have greened up
    subprocess.call(shlex.split("{5} {4}gdal_calc.py -A {0} -B {1} --outfile={2} --calc={3} --overwrite".format(projclippednew,projclippedold,projfirstcalc,qualcalc, mainpath,pypath)))
    
    subprocess.call(shlex.split("{1}gdal_translate -of GTiff {0} {2}".format(projfirstcalc, mainpath, qualtif)))  
    subprocess.call(shlex.split("{2}gdaldem color-relief -of VRT {0} {3} {1}".format(projfirstcalc,colorvrt,mainpath,os.path.join(os.getcwd(),'colorsq.txt'))))

    
    #os.system("{1}gdal_translate -of GTiff {0} {2}".format(colorvrt, mainpath, qualtif))
    subprocess.call(shlex.split("{0}gdal2tiles.py -z {2}-{3} {1} {4} ".format(mainpath,colorvrt, outzoom, inzoom,qualfolder)))     


#def process(newdate, olddate, picname, 20, 10, 15, "rmd):    
