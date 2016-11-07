"""
functions, tables for working with database via sqlalchemy
"""

try:
    import sqlalchemy
except ImportError:
    input('PyQt4 is missing u need to instal this ')

DB_PATH = 'sqlite:///beatbox.db'

def init_db():
    """
        initialize Database with 2 tables

        create 2 tables with columns and constraints, meatadata, connection, engine
    """

    global engine, connection, metadata, sounds, beats
    engine = sqlalchemy.create_engine(DB_PATH)

    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    sounds = sqlalchemy.Table \
        ('sounds', metadata,
         sqlalchemy.Column('literal', sqlalchemy.String(10), primary_key=True, unique=True, nullable=False, index=True),
         sqlalchemy.Column('name', sqlalchemy.String(255)),
         sqlalchemy.Column('difficulty', sqlalchemy.Integer()),
         sqlalchemy.Column('sample', sqlalchemy.String(255)),
         sqlalchemy.Column('type', sqlalchemy.String(10)),
         sqlalchemy.Column('lesson_url', sqlalchemy.String(255)))
    beats = sqlalchemy.Table \
        ('beats', metadata,
         sqlalchemy.Column('beat_text', sqlalchemy.String(1023), primary_key=True, unique=True, nullable=False),
         sqlalchemy.Column('difficulty', sqlalchemy.Integer()),
         sqlalchemy.Column('bpm', sqlalchemy.Integer()),
         sqlalchemy.Column('index', sqlalchemy.Integer(), unique=True, default=(lambda: get_index(beats))))

    metadata.create_all(engine)


def get_index(table):
    """
        get_index(sqlalchemy.Table) -> integer

        Return last index of table which equal count of rows
    """

    s = sqlalchemy.select([sqlalchemy.func.count(list(table.c)[0]).label('count')])
    rp = connection.execute(s)
    result = rp.first()
    return result[0]


def add_item_to_beats(beat, diff=None, bpm=90):
    """
        add_item_to_beats(beat[, diff[, bpm]])

        insert data into 'beats' table
    """

    ins = beats.insert().values(
        beat_text=beat,
        difficulty=diff,
        bpm=bpm

    )
    ins.compile().params
    connection.execute(ins)


def add_item_to_sounds(liter, name, diff=None, sample=None, type_=None, url=None):
    """
        add_item_to_sounds(liter, name, diff=None, sample=None, type_=None, url=None)

        insert data into 'sounds' table
    """

    ins = sounds.insert().values(
        literal=liter,
        name=name,
        difficulty=diff,
        sample=sample,
        type=type_,
        lesson_url=url
    )

    ins.compile().params
    connection.execute(ins)


def show_table(table):
    """
        show_table(sqlalchemy.Table) -> sqlalchemy.engine.result.ResultProxy

        return whole table as ResultProxy object
    """

    s = sqlalchemy.select([table])
    return connection.execute(s)


    # Print results for debug
    # for row in connection.execute(s):
    # 	for element in row:
    # 		if element is not None:
    # 			print('{:15}'.format(element), end='')
    # 	print()
    # 	print('__'*35)


def show_table_beats(beat=None, diff=None, bpm=None):
    """
        show_table_beats(beat=None, diff=None, bpm=None) -> list

        return result from beats table with apllied filters as list of RowProxies
        filters:
        beat: all of splited by comma str element exist in beat_text
        diff: table column difficulty euqal
        bpm: table column bpm euqal
    """

    s = sqlalchemy.select([beats])
    if diff:
        s = s.where(beats.c.difficulty == diff)

    if bpm:
        s = s.where(beats.c.bpm == bpm)
    result = connection.execute(s).fetchall()
    # Checkin if all of splited by comma *beat* element exist in beat_text
    #all stuff casefolded

    if beat:
        array = beat.casefold()
        array = array.replace(' ', '')
        array = set(array.split(','))
        result_with_beat = []
        for i in result:

            if not array.difference(i.beat_text.split('-')) :
                result_with_beat.append(i)
        result = result_with_beat

    return result


def show_table_sounds(liter=None, diff=None, type_=None):
    """
        show_table_sounds(liter=None, diff=None, type_=None) -> list

        return result from beats table with apllied filters as list of RowProxies
        filters:
        liter: table column difficulty euqal no matter case
        diff: table column difficulty euqal
        type_: table column type euqal
    """

    if liter:
        #return value no matter of uppercase or lowercase literal
        s = sqlalchemy.select([sounds])
        s = s.where(sounds.c.literal == liter.casefold())
        s_up = sqlalchemy.select([sounds])
        s_up = s_up.where(sounds.c.literal == liter.upper())
        s_value = connection.execute(s).fetchall()
        s_up_value = connection.execute(s_up).fetchall()

        # return  ONLY liter match (ignore diff and type)
        return s_value if len(s_value) > len(s_up_value)  else s_up_value

    s = sqlalchemy.select([sounds])
    if diff:
        s = s.where(sounds.c.difficulty == diff)

    if type_:
        s = s.where(sounds.c.type == type_)
    return connection.execute(s).fetchall()


def del_table(table):
    """
        del_table(sqlalchemy.Table) -> integer

        Clear whole table in DB
    """

    s = sqlalchemy.delete(table)
    connection.execute(s)


if __name__ == '__main__':

    # Fill db with defaul values
    init_db()
    del_table(beats)
    add_item_to_beats('b-t-pf-t', 10, bpm=90)
    add_item_to_beats('b-ttt-pf-ttt-b-tt-b-pf-ttt', 20, bpm=90)
    add_item_to_beats('b-t-bt-pf-kch-(x2)-ttt', 20, bpm=90)
    add_item_to_beats('b-t-kch-bt-b-kha', 10, bpm=90)
    add_item_to_beats('b-t-pf-tt-b-pf-t', 20, bpm=90)
    add_item_to_beats('b-t-pf-t-bb-b-pf-t', 20, bpm=120)
    add_item_to_beats('b-t-pf-b-t-b-pf-t', 20, bpm=90)
    add_item_to_beats('b-tt-b-pf-tt-b-tt-b-t-pf-ttt', 20, bpm=120)
    add_item_to_beats('b-tt-b-pf-tt-bdb-bb-t-pf-tt', 30, bpm=90)
    add_item_to_beats('b-t-kch-tt-b-kch-t', 20, bpm=120)
    add_item_to_beats('b-t-kch-t-bb-b-kch-t', 20, bpm=90)
    add_item_to_beats('b-t-kch-b-t-b-kch-t', 20, bpm=90)
    add_item_to_beats('b-tt-b-kch-tt-b-tt-b-t-kch-ttt', 20, bpm=120)
    add_item_to_beats('b-tt-b-kch-tt-bdb-bb-t-kch-tt', 30, bpm=120)
    add_item_to_beats('bws-pfsh-budu-kha-pfsh-budu-kha-pfsh-budu-kha-pfsh-(x2)-b-bz', 30, bpm=120)

    print(show_table(beats).fetchall())
    del_table(sounds)
    add_item_to_sounds('b', 'kickdrum', diff= 10, type_='outward', url='https://www.youtube.com/watch?v=dBDOU3Wt2UI')
    add_item_to_sounds('bdb', 'drumroll', diff=30, type_='outward')
    add_item_to_sounds('pf', 'pf snare', diff= 10, type_='inward', url='https://www.youtube.com/watch?v=YIJ5oN32EHw')
    add_item_to_sounds('pfs', 'pf-s snare', diff=10, type_='outward', url='https://www.youtube.com/watch?v=YIJ5oN32EHw')
    add_item_to_sounds('pfsh', 'pf-sh snare', diff=10, type_='outward', url='https://www.youtube.com/watch?v=YIJ5oN32EHw')
    add_item_to_sounds('t', 'high hat', diff=10, type_='outward', url='https://www.youtube.com/watch?v=AE0tl1xftEY')
    add_item_to_sounds('tt', 'double high hat', diff=10, type_='outward', url='https://www.youtube.com/watch?v=AE0tl1xftEY')
    add_item_to_sounds('ttt', 'triple hat', diff=20, type_='outward', url='https://www.youtube.com/watch?v=AE0tl1xftEY')
    add_item_to_sounds('c', 'humming hat', diff=10, type_='free')
    add_item_to_sounds('hmm', 'humming', diff=20, type_='outward')
    add_item_to_sounds('dkch', 'inward double clap', diff= 20, type_='inward', url='')
    add_item_to_sounds('kch', 'inward euroclap', diff= 20, type_='inward', url='https://www.youtube.com/watch?v=70nGbvHYxxE')

    add_item_to_sounds('wut', 'woblebass', diff=20, type_='outward', url='https://www.youtube.com/watch?v=0eyjSBBBje0')
    add_item_to_sounds('kha', 'inward drag', diff=10, type_='inward', url='https://www.youtube.com/watch?v=0eyjSBBBje0')
    add_item_to_sounds('bws', 'bws oscilation', diff=30, type_='outward', url='https://www.youtube.com/watch?v=0eyjSBBBje0')
    add_item_to_sounds('budu', 'b-budu oscilation', diff=30, type_='outward', url='https://www.youtube.com/watch?v=0eyjSBBBje0')
    add_item_to_sounds('voot', 'zip sound', diff=20, type_='inward', url='https://www.youtube.com/watch?v=0eyjSBBBje0')
    add_item_to_sounds('ta', 'ta click', diff=10, type_='free')
    add_item_to_sounds('to', 'to click', diff=10, type_='free')
    add_item_to_sounds('ty', 'ty click', diff=10, type_='free')
    add_item_to_sounds('trrr', 'clickroll', diff=20, type_='free')
    print(show_table(sounds).fetchall())

'''
assertion
try:
    print(is_data_correct(name='gggggggggg'*100))
except ValueError as f:
    print(f)
except TypeError:
    print(' nope')
'''





