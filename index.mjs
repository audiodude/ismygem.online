import path from 'path';
import url from 'url';

import request from '@derhuerst/gemini/client.js';
import express from 'express';

const app = express();
app.use(express.json());
const PORT = process.env.PORT || 3000;
const CUR_DIR = path.dirname(url.fileURLToPath(import.meta.url));

app.use(express.static(path.join(CUR_DIR, 'frontend/dist')));

function mapErrorCodeToString(code) {
  switch (code) {
    case 'ENOTFOUND':
      return '[Connection Error] Lookup of that host failed (ENOTFOUND)';
      break;
    case 'ECONNREFUSED':
      return '[Connection Error] Could not connect to that host/port (ECONNREFUSED)';
      break;
    case 'ERR_SSL_WRONG_VERSION_NUMBER':
      return '[SSL Error] It looks like there is no SSL server at that port (ERR_SSL_WRONG_VERSION_NUMBER)';
      break;
    case 'ECONNRESET':
      return '[SSL Error] Could not create a secure connection (ECONNRESET)';
      break;
    case 'ERR_SSL_SSLV3_ALERT_HANDSHAKE_FAILURE':
      return '[SSL Error]: Could not create a secure connection (ERR_SSL_SSLV3_ALERT_HANDSHAKE_FAILURE)';
      break;
    case 'CERT_HAS_EXPIRED':
      return '[SSL Error]: Certificate has expired (CERT_HAS_EXPIRED)';
      break;
    case 'ERR_TLS_CERT_ALTNAME_INVALID':
      return '[SSL Error]: Certificate hostname does not match URL (ERR_TLS_CERT_ALTNAME_INVALID)';
      break;
    default:
      return '[Unknown] An unknown error occurred while connecting to the Gemini site';
      break;
  }
}

app.post('/api/v1/check', (req, res) => {
  if (!req.body.url) {
    res.statusCode = 400;
    res.json({
      status: 400,
      message: 'POST request was not JSON or missing `url` field',
    });
    return;
  }

  request(
    req.body.url,
    { tlsOpt: { rejectUnauthorized: false }, followRedirects: true },
    (err, response) => {
      let result = null;
      let message = null;
      if (err) {
        const errorCode = err && err.code;
        result = false;
        message = errorCode ? mapErrorCodeToString(errorCode) : null;
      } else {
        const status = response.statusCode.toString();
        result = !(status.startsWith('4') || status.startsWith('5'));
        message = `Connected to Gemini site, with failure (${response.statusMessage})`;
      }
      res.json({ result, message });
    },
  );
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
