import {Miro} from '@mirohq/miro-api';

export default function middlware(req, res, next) {
  req.miro = new Miro({
    storage: {
      async get(_userId) {
        try {
          return JSON.parse(req.cookies.state);
        } catch (err) {
          return undefined;
        }
      },

      set(userId, state) {
        res.cookie('id', userId, {path: '/', secure: true});
        res.cookie('state', JSON.stringify(state), {path: '/', secure: true});
      },
    },
  });
  next();
}
