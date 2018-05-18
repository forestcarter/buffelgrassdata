var express = require('express');
var app = express();
var fs = require('file-system');
var path = require('path');
const db = require('./db')

app.set("view engine", "ejs");
app.use( express.static( "public" ) );
//app.set('views','./views');

app.get("/", function(req, res){
    console.log("landing hit");
if(req.query.alpha){
	var myAlpha=req.query.alpha;
}else{ var myAlpha = 0.7;}
if(req.query.picCode){
	var picCode=req.query.picCode;
}else{ var picCode = 1;}
  
    res.render("landing",{picCode:picCode, myAlpha:myAlpha});
});

//app.get("/graph", function(req, res){
function findDataPoints(req,res,next){
    pointsList=[]
    if(req.query.mylat){
	var mylat=req.query.mylat;
    }
    if(req.query.mylong){
	var mylong=req.query.mylong;
    }
    if(req.query.julDay){
	var julDay=req.query.julDay;
	var maxDay=julDay-1;
	var minDay=julDay-16;
	var step=3;
	req.maxDay=maxDay;
	req.minDay=minDay;
	req.step=step;
    }
    var district = "rmd"
    if (mylong<-110.9){
	var district="tmd"
    }   
    for(var i=minDay; i<=maxDay; i+=req.step){
	var dbRequest ="SELECT ST_Value(rast, foo.pt_geom) AS b1pval FROM rmd1142018 CROSS JOIN (SELECT ST_SetSRID(ST_MakePoint(-110.6182,32.20), 4326) AS pt_geom) AS foo;"
	var dbRequest =`SELECT ST_Value(rast, foo.pt_geom) AS b1pval FROM ${district}${i}2018 CROSS JOIN (SELECT ST_SetSRID(ST_MakePoint(${mylong},${mylat}), 4326) AS pt_geom) AS foo;`
    console.log(dbRequest)
	db.query(dbRequest, function(error, rows){
	    if (error){
		console.log(error);
	    }
	parsedRows=rows.rows[0].b1pval
	    console.log(`i =${i}  val =${parsedRows}`);
	if(typeof(parsedRows) === "number") {
	    pointsList.push(parsedRows);
	    console.log("local"+pointsList.length)
	    console.log(pointsList.length)
	    if (pointsList.length==6){
		req.point1 = pointsList
		return next()}

	}
    });
    }
    	    	
};


function renderGraphPage(req, res) {
    console.log("render graph2");
    console.log(req.point1[0])
    res.render('graph', {
	minDay: req.minDay,
	maxDay: req.maxDay,
	step: req.step,
	point1: req.point1[0],
	point2: req.point1[1],
	point3: req.point1[2],
	point4: req.point1[3],
	point5: req.point1[4],
	point6: req.point1[5]
	});
}
        
app.get("/graph",findDataPoints,renderGraphPage);  
//    res.render("graph",{mylat:mylat, mylong:mylong});




app.get("/download", function(req, res){  
    res.render("download");
});

app.get("/download2", function(req, res){  
    
    if(req.query.dlnum){
	filenum=String(req.query.ndviorqual)+String(req.query.dlnum)+String(req.query.rmdortmd)+".tif";
	console.log(filenum);
	console.log("That was filenum");
	pathToFile =  (__dirname + '/public/tiles/downloads/'+filenum);
	console.log("Path to file="+pathToFile);
	pathToFile2 = path.join(__dirname, '/public/tiles/downloads/',filenum)
	console.log("Path to file2="+pathToFile2);
	//console.log(path.exists(pathToFile2));
	console.log(fs.existsSync(pathToFile2));
	res.download(pathToFile2,function(err){
	    console.log(err);
	    res.end();
	});	     
    }
//res.redirect("/download");
       
});

app.get("/legend", function(req, res){  
    res.render("legend");
});
	
app.listen(80, function(){
  console.log("Server has started");
});
