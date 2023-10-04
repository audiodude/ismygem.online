import request from 'supertest';
import { app } from './app.mjs';

describe('api', () => {
  describe('/v1/check', () => {
    it('returns JSON', () => {
      return request(app).post('/api/v1/check').expect('Content-Type', /json/);
    });

    describe('when no POST url is given in JSON', () => {
      it('returns a JSON object with 400 status and a message', () => {
        return request(app)
          .post('/api/v1/check')
          .expect('Content-Type', /json/)
          .expect(400)
          .then((res) => {
            // Status property on a JSON object: {"status": 400, ...}
            expect(res.body.status).toEqual(400);
          });
      });
    });
  });
});
