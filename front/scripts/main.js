var settings = {
  url: "http://localhost:3000/",
  method: "GET",
  timeout: 0,
};

var timestamp = ["timestamp"];
var value = ["value"];

$.ajax(settings).done(function (response) {
  response.forEach(function setValues(item) {
    timestamp.push(item.timestamp);
    value.push(item.value)
  });
  console.log(timestamp);
  console.log(value);

  var chart = c3.generate({
    bindto: "#chart",
    data: {
      columns: [
        //timestamp,
        value,
      ],
    },
    axis: {
        x: {
            type: 'category',
            timestamp
        }
    }
  });
  
});

