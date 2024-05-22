const axios = require('axios');
const http = require('http');

function extract(inp) {
  const match = inp.match(/\d+/);
  return match ? match[0] : null;
}

async function fetcher(kw){
  const res = [];
  let n = 1;
  while (true) {
    axios.get(`https://jsonmock.hackerrank.com/api/weather/search?name=${kw}&page=${n}`)
      .then(response => {
        const raw_data = response.data;
        console.log(raw_data);
        for (const row of raw_data.data) {
          const wind = extract(row.status[0]);
          const hum = extract(row.status[1]);
          res.push(`${row.name},${row.weather.split(' ')[0]},${wind},${hum}`);
        }

        if (raw_data.page >= raw_data.total_pages) {
          console.log(res);
        } else {
          n++;
        }
      })
      .catch(error => console.error(error));

    if (n > 10) break;
  }
}


const requestListener = function (req, res) {
    res.writeHead(200);
    res.end("My first server!");
};

const host = 'localhost';
const server = http.createServer(requestListener);
server.listen(8080, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});

// http.createServer(function (req, res) {
//   res.writeHead(200, {'Content-Type': 'text/html'});
//   res.end('Hello World!');
//   // fetcher("all");
// }).listen(8080);
