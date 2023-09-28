const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/api/hello', (req, res) => {
  res.send('Hello API');
});

app.listen(PORT, () => {
  console.log(`Running on port ${PORT}.`);
});
