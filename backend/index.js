const API_KEY = "BBFF-b3808660343fa365f90b22577d679c88045"
//const API_TOKEN = "BBFF-JzakIetJeyZbpTQeBzw76KxKp1Amrx"
// Authorize API with an API Key

var ubidots = require('ubidots');
var client = ubidots.createClient(API_KEY);
    
    client.auth(function () {
    //   this.getDatasources(function (err, data) {
    //     console.log(data.results);
    //   });
    
    //   var ds = this.getDatasource('xxxxxxxx');
    
    //   ds.getVariables(function (err, data) {
    //     console.log(data.results);
    //   });
    
    //   ds.getDetails(function (err, details) {
    //     console.log(details);
    //   });
    
      var v = this.getVariable('5f973b400ff4c3359ef72e26');
    
    //   v.getDetails(function (err, details) {
    //     console.log(details);
    //   });

      v.getValues(function (err, data) {
        console.log(data.results);
      });
    
      //v.saveValue(22);
    
    //   v.getValues(function (err, data) {
    //     console.log(data.results);
    //   });
    });