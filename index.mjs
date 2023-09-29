import express from 'express';
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/api/v1/hello', (req, res) => {
  res.json({ result: false });
});

app.listen(PORT, () => {
  console.log(`Running on port ${PORT}.`);
});
