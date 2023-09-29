import path from 'path';
import url from 'url';
import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000;
const CUR_DIR = path.dirname(url.fileURLToPath(import.meta.url));

app.use(express.static(path.join(CUR_DIR, 'frontend/dist')));

app.get('/api/v1/hello', (req, res) => {
  res.json({ result: false });
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
