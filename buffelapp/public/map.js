var map2 = L.map('map2', ({                  
	            maxZoom: 15
	        })).setView([32.1874446, -110.6185017],11);

var streets = L.tileLayer('http://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
{attribution: 'Map data &coipy OpenStreetMap contributors'
});

var imagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
}).addTo(map2);

var basemaps = {"Streets":streets, "ESRI Imagery":imagery}

var lyr1 = L.tileLayer('tiles/rmd/'+picCode+'/ndvi/{z}/{x}/{y}.png', { enable:true, tms: true, opacity: myAlpha, attribution: ""});
map2.addLayer(lyr1);

var lyr3 = L.tileLayer('tiles/tmd/'+picCode+'/ndvi/{z}/{x}/{y}.png', { enable:true, tms: true, opacity: myAlpha, attribution: ""});
map2.addLayer(lyr3);

var lyr2 = L.tileLayer('/tiles/rmd/'+picCode+'/qual/{z}/{x}/{y}.png', { enable:true, tms: true, opacity: myAlpha, attribution: ""});
var lyr4 = L.tileLayer('/tiles/tmd/'+picCode+'/qual/{z}/{x}/{y}.png', { enable:true, tms: true, opacity: myAlpha, attribution: ""});

var lyr5 = L.tileLayer('/tiles/ahps/delay01/{z}/{x}/{y}.png', { enable:true, tms: true, opacity: myAlpha, attribution: ""});
var lyr6 = L.tileLayer('/tiles/ahps/delay05/{z}/{x}/{y}.png', { enable:true, tms: true, opacity: myAlpha, attribution: ""});
var lyr7 = L.tileLayer('/tiles/ahps/delay09/{z}/{x}/{y}.png', { enable:true, tms: true, opacity: myAlpha, attribution: ""});
var lyr8 = L.tileLayer('/tiles/ahps/delay13/{z}/{x}/{y}.png', { enable:true, tms: true, opacity: myAlpha, attribution: ""});
var lyr9 = L.tileLayer('/tiles/ahps/delay17/{z}/{x}/{y}.png', { enable:true, tms: true, opacity: myAlpha, attribution: ""});


var overlaymaps = {"RMD_NDVI": lyr1, "RMD_QUAL":lyr2,"TMD_NDVI": lyr3, "TMD_QUAL":lyr4
		   , "1_Day_Ago":lyr5
		   , "5_Days_Ago":lyr6
		   , "9_Days_Ago":lyr7
		   , "13_Days_Ago":lyr8
		  , "17_Days_Ago":lyr9}

L.control.layers(basemaps, overlaymaps).addTo(map2);
map2.on("click", function (event){
    incominglat.defaultValue=  event.latlng.lat
    incominglong.defaultValue=  event.latlng.lng
    incomingjulday.defaultValue= updatejulday.innerHTML.slice(-3)

});

    //Downloads
