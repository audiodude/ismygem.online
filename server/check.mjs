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
export function checkSite(url, gemRequest, callback) {
  gemRequest(
    url,
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
        if (!result) {
          message = `Connected to Gemini site, with failure (${response.statusMessage})`;
        }
      }
      callback({ result, message });
    },
  );
}
