import { postCheckSite } from './functions.mjs';

describe('functions test', () => {
  describe('postCheckSite', () => {
    let res;
    beforeEach(() => {
      res = jasmine.createSpyObj('res', ['json']);
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
  });
});
