export function postCheckSite(req, res, checkSite, gemRequest) {
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
}
