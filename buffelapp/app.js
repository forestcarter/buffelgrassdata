var express = require('express');
var app = express();
var fs = require('file-system');
var path = require('path');
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

app.get("/download", function(req, res){  
    res.render("download");
});
app.get("/download2", function(req, res){  
    
    if(req.query.dlnum){
	filenum=String(req.query.ndviorqual)+String(req.query.dlnum)+".tif";
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
	
app.listen(80, function(){
  console.log("Server has started");
});
