var settings = {
  url: "http://localhost:3000/",
  method: "GET",
  timeout: 0,
};

var timeTemp = ["timeTemp"];
var temperature = ["temperature"];
var timeHumR = ["timeHumR"];
var humidity = ["humidity"];
var timelumi = ["timelumi"];
var luminiscence = ["luminiscence"];
var timeSoilM1 = ["timeSoilM1"];
var soilMoisture1 = ["soilMoisture1"];
var timeSoilM2 = ["timeSoilM2"];
var soilMoisture2 = ["soilMoisture2"];
var timeSoilM3 = ["timeSoilM3"];
var soilMoisture3 = ["soilMoisture3"];

//Función de ajax que ejecuta el metodo get para obtener los datos que se envían desde
//el backend
$.ajax(settings).done(function (response) {
  //Se hace un mapeo por cada una de las variables para
  //separar los vectores de tiempo y de valores
  response[0].forEach(function setValues(item) {
    timeTemp.push(item.timestamp);
    temperature.push(item.value);
  });
  response[1].forEach(function setValues(item) {
    timeHumR.push(item.timestamp);
    humidity.push(item.value);
  });
  response[2].forEach(function setValues(item) {
    timelumi.push(item.timestamp);
    luminiscence.push(item.value);
  });
  response[3].forEach(function setValues(item) {
    timeSoilM1.push(item.timestamp);
    soilMoisture1.push(item.value);
  });
  response[4].forEach(function setValues(item) {
    timeSoilM2.push(item.timestamp);
    soilMoisture2.push(item.value);
  });
  response[5].forEach(function setValues(item) {
    timeSoilM3.push(item.timestamp);
    soilMoisture3.push(item.value);
  });

  //Se crea el objeto que genera el gráfico en base a los datos
  //de cada variable
  var chart1 = c3.generate({
    //Identificador de la etiqueta html en index.html
    //Que va a contener el gráfico de esta variable
    bindto: "#chart1",
    data: {
      //Se declara el eje x
      x: "timeTemp",
      //Se le asiganan los valores de tiempo y magnitud
      columns: [timeTemp, temperature],
    },
    axis: {
      x: {
        type: "category",
      },
    },
  });

  var chart2 = c3.generate({
    bindto: "#chart2",
    data: {
      x: "timeHumR",
      columns: [timeHumR, humidity],
    },
    axis: {
      x: {
        type: "category",
      },
    },
  });
  var chart3 = c3.generate({
    bindto: "#chart3",
    data: {
      x: "timelumi",
      columns: [timelumi, luminiscence],
    },
    axis: {
      x: {
        type: "category",
      },
    },
  });
  var chart4 = c3.generate({
    bindto: "#chart4",
    data: {
      x: "timeSoilM1",
      columns: [timeSoilM1, soilMoisture1],
    },
    axis: {
      x: {
        type: "category",
      },
    },
  });
  var chart5 = c3.generate({
    bindto: "#chart5",
    data: {
      x: "timeSoilM2",
      columns: [timeSoilM2, soilMoisture2],
    },
    axis: {
      x: {
        type: "category",
      },
    },
  });
  var chart1 = c3.generate({
    bindto: "#chart6",
    data: {
      x: "timeSoilM3",
      columns: [timeSoilM3, soilMoisture3],
    },
    axis: {
      x: {
        type: "category",
      },
    },
  });
});
