import request from 'supertest';

import { app } from './app.mjs';
import * as checkModule from './check.mjs';

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
            expect(typeof res.body.message).toEqual('string');
          });
      });
    });

    describe('when a POST url is given', () => {
      describe('and it is a valid Gemini site', () => {
        beforeEach(() => {
          spyOn(checkModule, 'checkSite').and.callFake(
            (url, gemRequest, callback) => {
              callback({ result: true, message: null });
            },
          );
        });

        it('returns result:true and null message', () => {
          return request(app)
            .post('/api/v1/check')
            .send({ url: 'gemini://gemini.circumlunar.space/' })
            .expect('Content-Type', /json/)
            .expect(200)
            .then((res) => {
              expect(res.body.result).toBe(true);
              expect(res.body.message).toBeNull();
            });
        });
      });
    });
  });
});
