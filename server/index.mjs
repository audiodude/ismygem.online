import { app } from './app.mjs';

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Running on port ${PORT}.`);
});
