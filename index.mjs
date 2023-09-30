import path from 'path';
import url from 'url';

import request from '@derhuerst/gemini/client.js';
import express from 'express';

const app = express();
app.use(express.json());
const PORT = process.env.PORT || 3000;
const CUR_DIR = path.dirname(url.fileURLToPath(import.meta.url));

app.use(express.static(path.join(CUR_DIR, 'frontend/dist')));

app.post('/api/v1/check', (req, res) => {
  console.log(req.body);
  request(req.body.url, {}, (err, gemResponse) => {
    console.log(err);
    res.json({ result: !err, error: err });
  });
});

app.get('/', (req, res) => {
  res.sendFile(
    path.join(
      dirname(fileURLToPath(import.meta.url)),
      'frontend/dist/index.html',
    ),
  );
});

app.listen(PORT, () => {
  console.log(`Running on port ${PORT}.`);
});
