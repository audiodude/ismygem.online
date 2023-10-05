import path from 'path';
import url from 'url';

import gemRequest from '@derhuerst/gemini/client.js';
import express from 'express';

import { checkSite } from './check.mjs';

export const app = express();
app.use(express.json());
const CUR_DIR = path.dirname(url.fileURLToPath(import.meta.url));

app.use(express.static(path.join(CUR_DIR, 'frontend/dist')));

app.post('/api/v1/check', (req, res) => {
  if (!req.body.url) {
    res.statusCode = 400;
    res.json({
      status: 400,
      message: 'POST request was not JSON or missing `url` field',
    });
    return;
  }

  checkSite(req.body.url, gemRequest, (result) => {
    res.json(result);
  });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(CUR_DIR, 'frontend/dist/index.html'));
});
