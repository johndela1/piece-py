from sqlalchemy import *
import model


attempt = model.Attempt.__table__
delta = model.Delta.__table__
extra = model.Extra.__table__
miss = model.Miss.__table__

session = model.session
conn = model.engine.connect()
from pprint import pprint as pp

if __name__ == '__main__':
    rs = conn.execute(
        select([
            func.count(),
            func.date_trunc('minute', attempt.c.created).label('foo')])
        .order_by('foo')
        # .group_by(attempt.c.id, func.trunc(attempt.c.bpm, -2))
        .group_by('foo')
        .where(attempt.c.result)
#        .having(attempt.c.result)
        #.select_from(attempt).having(attempt.c.result)
       ).fetchall()
    print(len(rs))
    pp(rs)
    import pdb;pdb.set_trace()
   # pp(rs)
