const express = require('express');
const {MongoClient} = require('mongodb');
const { Socket } = require('engine.io');
const res = require('express/lib/response');
var app = express();
const server = require('http').createServer(app);
var io = require('socket.io')(server);

var dataBahamas = [];
var way_idBahamas = [];
var latBahamas = [];
var lngBahamas = [];
var resBahamas = [];
var areaBahamas = [];

var dataEl_salvador = [];
var way_idEl_salvador = [];
var latEl_salvador = [];
var lngEl_salvador = [];
var resEl_salvador = [];
var areaEl_salvador = [];

var dataGuinea_bissau = [];
var way_idGuinea_bissau = [];
var latGuinea_bissau = [];
var lngGuinea_bissau = [];
var resGuinea_bissau = [];
var areaGuinea_bissau = [];

var dataMauritius = [];
var way_idMauritius = [];
var latMauritius = [];
var lngMauritius = [];
var resMauritius = [];
var areaMauritius = [];

var dataVenezuela = [];
var way_idVenezuela = [];
var latVenezuela = [];
var lngVenezuela = [];
var resVenezuela = [];
var areaVenezuela = [];

var dataAngola = [];
var way_idAngola = [];
var latAngola = [];
var lngAngola = [];
var resAngola = [];
var areaAngola = [];

var dataChad = [];
var way_idChad = [];
var latChad = [];
var lngChad = [];
var resChad = [];
var areaChad = [];

var dataArray = [];

const hostname = '127.0.0.1';
const port = 3000;


app.use(express.static(__dirname));

server.listen(3000);
app.get('/',function(request, response){
    response.sendFile(__dirname+'/index.html')
});

/*server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});*/


var url = "mongodb+srv://ScorpionVSTU:VsTuBoY@scorpioncluster.kb9vl.mongodb.net/SpprDb?retryWrites=true&w=majority";
var k;
MongoClient.connect(url,
    function(err, db) {
    if (err) throw err;
    console.log("Database connected!");
    var dbo = db.db("SpprDb");
    var results = dbo.collection("bahamas").find({});
    results.forEach(row => {
        k = row.way_id;
        way_idBahamas.push(row.way_id);
        latBahamas.push(row.lat);
        lngBahamas.push(row.lon);
        resBahamas.push(row.residents);
        areaBahamas.push(row.area);
    });
    dataBahamas.push(way_idBahamas);
    dataBahamas.push(latBahamas);
    dataBahamas.push(lngBahamas);
    dataBahamas.push(resBahamas);
    dataBahamas.push(areaBahamas);

    var results = dbo.collection("el-salvador").find({});
    results.forEach(row => {
        k = row.way_id;
        way_idEl_salvador.push(row.way_id);
        latEl_salvador.push(row.lat);
        lngEl_salvador.push(row.lon);
        resEl_salvador.push(row.residents);
        areaEl_salvador.push(row.area);
    });
    dataEl_salvador.push(way_idEl_salvador);
    dataEl_salvador.push(latEl_salvador);
    dataEl_salvador.push(lngEl_salvador);
    dataEl_salvador.push(resEl_salvador);
    dataEl_salvador.push(areaEl_salvador);

    var results = dbo.collection("guinea-bissau").find({});
    results.forEach(row => {
        k = row.way_id;
        way_idGuinea_bissau.push(row.way_id);
        latGuinea_bissau.push(row.lat);
        lngGuinea_bissau.push(row.lon);
        resGuinea_bissau.push(row.residents);
        areaGuinea_bissau.push(row.area);
    });
    dataGuinea_bissau.push(way_idGuinea_bissau);
    dataGuinea_bissau.push(latGuinea_bissau);
    dataGuinea_bissau.push(lngGuinea_bissau);
    dataGuinea_bissau.push(resGuinea_bissau);
    dataGuinea_bissau.push(areaGuinea_bissau);

    var results = dbo.collection("mauritius").find({});
    results.forEach(row => {
        k = row.way_id;
        way_idMauritius.push(row.way_id);
        latMauritius.push(row.lat);
        lngMauritius.push(row.lon);
        resMauritius.push(row.residents);
        areaMauritius.push(row.area);
    });
    dataMauritius.push(way_idMauritius);
    dataMauritius.push(latMauritius);
    dataMauritius.push(lngMauritius);
    dataMauritius.push(resMauritius);
    dataMauritius.push(areaMauritius);

    var results = dbo.collection("venezuela").find({});
    results.forEach(row => {
        k = row.way_id;
        way_idVenezuela.push(row.way_id);
        latVenezuela.push(row.lat);
        lngVenezuela.push(row.lon);
        resVenezuela.push(row.residents);
        areaVenezuela.push(row.area);
    });
    dataVenezuela.push(way_idVenezuela);
    dataVenezuela.push(latVenezuela);
    dataVenezuela.push(lngVenezuela);
    dataVenezuela.push(resVenezuela);
    dataVenezuela.push(areaVenezuela);

    var results = dbo.collection("angola").find({});
    results.forEach(row => {
        k = row.way_id;
        way_idAngola.push(row.way_id);
        latAngola.push(row.lat);
        lngAngola.push(row.lon);
        resAngola.push(row.residents);
        areaAngola.push(row.area);
    });
    dataAngola.push(way_idAngola);
    dataAngola.push(latAngola);
    dataAngola.push(lngAngola);
    dataAngola.push(resAngola);
    dataAngola.push(areaAngola);

    var results = dbo.collection("chad").find({});
    results.forEach(row => {
        k = row.way_id;
        way_idChad.push(row.way_id);
        latChad.push(row.lat);
        lngChad.push(row.lon);
        resChad.push(row.residents);
        areaChad.push(row.area);
    });
    dataChad.push(way_idChad);
    dataChad.push(latChad);
    dataChad.push(lngChad);
    dataChad.push(resChad);
    dataChad.push(areaChad);

    dataArray.push(dataBahamas);
    dataArray.push(dataEl_salvador);
    dataArray.push(dataGuinea_bissau);
    dataArray.push(dataMauritius);
    dataArray.push(dataVenezuela);
    dataArray.push(dataAngola);
    dataArray.push(dataChad);
    console.log("Database loaded!")
});
connections = []

// Функция, которая сработает при подключении к странице
// Считается как новый пользователь
io.sockets.on('connection', function(socket) {
    console.log("Успешное соединение");
    // Добавление нового соединения в массив
    connections.push(socket);

    // Функция, которая срабатывает при отключении от сервера
    socket.on('disconnect', function(data) {
        // Удаления пользователя из массива
        connections.splice(connections.indexOf(socket), 1);
        console.log("Отключились");
    });
    
    
    // Функция чтения из файла
    socket.on('read database', function(data) {
        data = dataArray;
        io.sockets.emit('write database', {data: data});
        console.log('Лог отправлен');
    });

});

