import os
import subprocess
import shlex

def ahpsprocess(outzoom,inzoom,precipdays, delay):      
    
    print("ahpsprocess now working in {}".format(os.getcwd))
    xmin=-112.11518
    xmax=-109.4760646
    ymin=31.1035758
    ymax=33.6212308
    
    mypath = os.path.join(os.getcwd(),'static')
    pypath="/usr/bin/python"
    mainpath = "/usr/bin/"
    dolater=[]
    for idnum, item in enumerate(os.listdir(os.path.join(mypath,'precipdata'))):
        if idnum==0:
            #oldtif='{0}histunzipped/{1}'.format(mypath,item)
            #oldtifname=item
            ahpsfile="static/precipdata/{}".format(item)
            print("ahpsfile here",ahpsfile)
        else:
            dolater.append("static/precipdata/{}".format(item))
    ahpsvrt = "{}/ahpsvrt.vrt".format(mypath)
    print(ahpsvrt)
    ahpsadd = "{}/ahpsadd.vrt".format(mypath)
    ahpsbase = "{}/ahpsbase.vrt".format(mypath)
    ahpsvrtclipped = "{}/ahpavrtclipped.vrt".format(mypath)
    colorahps = "{}/colorahps.vrt".format(mypath)
    projfirstnew = "{}/histprojfirstnew.vrt".format(mypath)
    projfirstold = "{}/histprojfirstold.vrt".format(mypath)
    projclippednew="{}/histprojclippednew.vrt".format(mypath)
    projclippedold="{}/histprojclippedold.vrt".format(mypath)
    colorvrt="{}/colorvrt.vrt".format(mypath)
    rgbvrt="{}/rgbvrt.vrt".format(mypath)
    colorpng="{}/buffelapp/public/colorpng.png".format(mypath)
   
    #ndvitif="{0}/buffelapp/public/downloads/ndvi{1}.tif".format(mypath,picname)
    #qualtif="{0}/buffelapp/public/downloads/qual{1}.tif".format(mypath,picname)    
    #NDVI
    tilefolder=os.path.join(os.getcwd(),'buffelapp','public','tiles')
 
    ahpsfolder=os.path.join(tilefolder,'ahps')
    delayfolder=os.path.join(tilefolder,'ahps',"delay"+delay)
    if not os.path.isdir(ahpsfolder):
        subprocess.call(shlex.split("mkdir {}".format(ahpsfolder)))
    if not os.path.isdir(delayfolder):
        subprocess.call(shlex.split("mkdir {}".format(delayfolder)))
                           
    #Make bil vrt
    subprocess.call(shlex.split("{2}gdalwarp -t_srs EPSG:4326 -of VRT -overwrite {0} {1} ".format(ahpsfile, ahpsvrt,mainpath)))
    #subprocess.call(shlex.split("{2}gdalwarp -of VRT -overwrite {0} {1} ".format(bilfile, bilvrt,mainpath))


    
    #subprocess.call(shlex.split("{2}gdalwarp -s_srs EPSG:2163 -t_srs EPSG:4326 -of VRT -overwrite {0} {1} ".format(oldtif, projfirstold,mainpath))
    subprocess.call(shlex.split("{6}gdal_translate {0} {1} -of VRT -b 1 -projwin {2} {3} {4} {5}".format(ahpsvrt, ahpsbase, xmin,ymax, xmax,ymin,mainpath)))
    #subprocess.call(shlex.split("{6}gdal_translate {0} {1} -of VRT -projwin {2} {3} {4} {5}".format(projfirstold, projclippedold, xmin,ymax, xmax,ymin,mainpath))
    calc = "A*(A>0)+B*(B>0)"
    calc2 = "A*100+B*0"    
    for item in dolater:
        subprocess.call(shlex.split("{2}gdalwarp -t_srs EPSG:4326 -of VRT -overwrite {0} {1} ".format(item, ahpsvrt,mainpath)))
    
        subprocess.call(shlex.split("{6}gdal_translate {0} {1} -of VRT -b 1 -projwin {2} {3} {4} {5}".format(ahpsvrt, ahpsadd, xmin,ymax, xmax,ymin,mainpath)))
        #subprocess.call(shlex.split("{6}gdalinfo -stats {1}".format(ahpsvrt, ahpsadd, xmin,ymax, xmax,ymin,mainpath))
        subprocess.call(shlex.split('{5} {4}gdal_calc.py -A {0} -B {1} --outfile={2} --calc="{3}" --overwrite'.format(ahpsbase,ahpsadd,ahpsbase,calc, mainpath,pypath)))
    #subprocess.call(shlex.split("{1}gdal_translate -of GTiff {0} {2}".format(projfirstcalc, mainpath, ndvitif))
    #subprocess.call(shlex.split("{5} {4}gdal_calc.py -A {0} --outfile={2} --calc=A*(A>=0) --overwrite".format(ahpsbase,ahpsadd,ahpsbase,calc2, mainpath,pypath))
    subprocess.call(shlex.split("{2}gdaldem color-relief -of VRT {0} colorsahps.txt {1}".format(ahpsbase,colorahps,mainpath)))

    subprocess.call(shlex.split("cp {0} {1}".format(os.path.join(os.getcwd(),'colorsahps.txt'),os.path.join(os.getcwd(),'buffelapp','public', 'colorsahps.txt'))))
    #subprocess.call(shlex.split("{1}gdal_translate {0} {2}".format(colorvrt, mainpath, rgbvrt))
    
    subprocess.call(shlex.split("{0}gdal2tiles.py -z {2}-{3} {1} {4} ".format(mainpath,colorahps, outzoom, inzoom,delayfolder)))

    #subprocess.call(shlex.split("{2}gdaldem color-relief -of PNG {0} {3}colorsbil.txt {1}".format(bilvrtclipped,colorpng,mainpath,mypath))
#precipprocess(7,13,24)
