const temperaturaId = "5f973b400ff4c3359ef72e26";
const humedadRelativaId = "5f973b390ff4c3359ef72e25";
const luminiscenciaId = "5f973b3f0ff4c333e278add9";
const humedadSuelo3Id = "5f973b3e4763e75f806f0d9a";
const humedadSuelo2Id = "5f973b3c73efc33e0382dd7f";
const humedadSuelo1Id = "5f973b3b73efc33daecf8cd1";

const express = require("express");
const app = express();
const port = 3000;
const API_KEY = "BBFF-b3808660343fa365f90b22577d679c88045";
var ubidots = require("ubidots");
var client = ubidots.createClient(API_KEY);
var cors = require("cors");
var temperatura,
  humedadRelativa,
  luminiscencia,
  humedadSuelo1,
  humedadSuelo2,
  humedadSuelo3;

app.use(cors());

app.get("/", (req, res) => {
  client.auth(function () {
    f1(res);
  });
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});

async function f1(res) {
  temperatura = await getValuesFromVariable(temperaturaId);
  humedadRelativa = await getValuesFromVariable(humedadRelativaId);
  luminiscencia = await getValuesFromVariable(luminiscenciaId);
  humedadSuelo1 = await getValuesFromVariable(humedadSuelo1Id);
  humedadSuelo2 = await getValuesFromVariable(humedadSuelo2Id);
  humedadSuelo3 = await getValuesFromVariable(humedadSuelo3Id);
  res.send([
    temperatura,
    humedadRelativa,
    luminiscencia,
    humedadSuelo1,
    humedadSuelo2,
    humedadSuelo3,
  ]);
}
function timeConverter(UNIX_timestamp) {
  var a = new Date(UNIX_timestamp);
  var months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = date + " " + month + " " + hour + ":" + min + ":" + sec;
  return time;
}

function getValuesFromVariable(variableId) {
  return new Promise(function (resolve, reject) {
    //Se crea la promesa
    client.auth(function () {
      //Metodo del cliente Ubidots, se le pasa una
      //función anonima con l o que se quiera obtener de la API
      //Se declara una solicitud de la variable
      const variable = this.getVariable(variableId);
      //Este metodo de la variable devuelve los datos con el resolve
      variable.getValues(function (err, data) {
        if (err) {
          reject(err);
        }
        resolve(data.results);
      });
    });
  }).then((value) => {
    //Solamente se cogen los ultimos 10 mdatos y se eliminan los elementos
    //context y created_at que no son necesarios, ademas se convierte el
    //timestamp a una fecha legible
    let values = value.slice(0, 10);
    values.map((x) => {
      x.timestamp = timeConverter(x.timestamp);
      delete x.context;
      delete x.created_at;
    });
    return values;
  });
}
