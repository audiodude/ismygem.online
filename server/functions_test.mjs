import { postCheckSite } from './functions.mjs';

describe('functions test', () => {
  describe('postCheckSite', () => {
    let res;
    let checkSiteSpy;
    let gemRequestSpy;

    beforeEach(() => {
      res = jasmine.createSpyObj('res', ['json']);
      checkSiteSpy = jasmine.createSpy('checkSite');
      gemRequestSpy = jasmine.createSpy('gemRequest');
    });

    describe(`when the request body doesn't have a url property`, () => {
      it('returns an error message in JSON', () => {
        postCheckSite({ body: { foo: 42, bar: null } }, res, null, null);
        expect(res.statusCode).toEqual(400);
        expect(res.json).toHaveBeenCalledWith({
          status: 400,
          message: 'POST request was not JSON or missing `url` field',
        });
      });
    });

    it('passes the right parameters to checkSite', () => {
      postCheckSite(
        { body: { url: 'gemini://foo.bar.fake' } },
        res,
        checkSiteSpy,
        gemRequestSpy,
      );
      expect(checkSiteSpy).toHaveBeenCalledWith(
        'gemini://foo.bar.fake',
        gemRequestSpy,
        jasmine.any(Function),
      );
    });

    it('returns the result from checkSite to res.json', () => {
      let resultCallback;
      checkSiteSpy.and.callFake((url, gemRequest, callback) => {
        resultCallback = callback;
      });

      postCheckSite(
        { body: { url: 'gemini://foo.bar.fake' } },
        res,
        checkSiteSpy,
        gemRequestSpy,
      );

      resultCallback({ result: true, message: null });
      expect(res.json).toHaveBeenCalledWith({ result: true, message: null });
    });
  });

  it('test failure for CI', () => {
    fail('boom');
  });
});
