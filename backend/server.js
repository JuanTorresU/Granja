const express = require('express')
const app = express()
const port = 3000
const API_KEY = "BBFF-b3808660343fa365f90b22577d679c88045"
var ubidots = require('ubidots');
var client = ubidots.createClient(API_KEY);
var cors = require('cors')

app.use(cors())
    
app.get('/', (req, res) => {

    client.auth(function () {
          var v = this.getVariable('5f973b400ff4c3359ef72e26');    
          v.getValues(function (err, data) {
            //console.log(data.results);
            res.send(data.results)
          });
        });

})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
