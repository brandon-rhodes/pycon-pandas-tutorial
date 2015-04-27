"""Build the tutorial data files from the IMDB *.list.gz files."""

import csv
import gzip
import os
import re

#import pandas as pd

def main():
    os.chdir(os.path.dirname(__file__))
    if not os.path.isdir('../data'):
        os.makedirs('../data')

    #m = gzip.open('movies.list.gz')

    # Load movie titles.

    titles = set()
    uninteresting_titles = set()

    lines = iter(gzip.open('genres.list.gz'))
    line = next(lines)
    while line != b'8: THE GENRES LIST\n':
        line = next(lines)
    assert next(lines) == b'==================\n'
    assert next(lines) == b'\n'

    match = re.compile(r'^(.*) \((\d+)(/[IVXL]+)?\)\t+(.*)$').match

    for line in lines:
        if (line.startswith(b'"')       # TV show
            or b'{' in line             # TV episode
            or b' (????' in line        # Unknown year
            or b' (TV)' in line         # TV Movie
            or b' (V)' in line          # Video
            or b' (VG)' in line         # Video game
            ):
            continue

        try:
            line = line.strip().decode('ascii')
        except UnicodeDecodeError:
            continue

        m = match(line.strip())
        if m is None:
            print(repr(line))
            break
            continue

        title = m.group(1).strip('"')
        year = int(m.group(2))
        numeral = m.group(3)
        genre = m.group(4)

        if numeral is not None:
            numeral = numeral.strip('/')
            if numeral != 'I':
                title = '{} ({})'.format(title, numeral)

        ty = (title, year)

        if genre in ('Adult', 'Documentary', 'Short'):
            uninteresting_titles.add(ty)
        else:
            titles.add(ty)

    titles = titles - uninteresting_titles
    del uninteresting_titles

    with open('titles.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(('title', 'year'))
        for ty in titles:
            w.writerow(ty)

    # output = open('titles.csv', 'wb')
    # output.write(b'title,year\n')
    # for title, year in titles:
    #     output.write('{},{}\n'.format(title, year).encode('ascii'))


# def reduce_data():

    # names = pd.read_csv('name.csv', usecols=[0,1,2,4], index_col=0,
    #                     names=['id', 'name', 'numeral', 'sex'],
    #                     dtype={'sex': str})

#     names.name = names.name.apply(swap_names)

#     n = names.numeral.notnull() & (names.numeral != 'I')
#     names.loc[n, 'name'] = names.name[n] + ' (' + names.numeral[n] + ')'
#     del names['numeral']

#     print(len(names))
#     print(names.dtypes)
#     names.head()

#     names[names.name.str.startswith('George Clooney')]

#     names.sex.unique()

#     titles = pd.read_csv('title.csv', usecols=[0,1,2,3,4], index_col=0,
#                          names=['id', 'title', 'numeral', 'type', 'year'])

#     # 1 Feature film
#     # 2 TV series
#     # 3 TV movie
#     # 4 Adult film
#     # 5 (no rows match)
#     # 6 Video game
#     # 7 TV series episode

#     titles = titles[(titles.type == 1) & (titles.year.notnull())]
#     del titles['type']

#     n = titles.numeral.notnull() & (titles.numeral != 'I')
#     titles.title[n] = titles.title[n] + ' (' + titles.numeral[n] + ')'
#     del titles['numeral']

#     titles = titles.drop_duplicates()

#     print('{:,}'.format(len(titles)))
#     print(titles.dtypes)
#     titles.head()

#     avoid_ids = set()
#     with open('movie_info.csv') as f:
#         for row in csv.reader(f):
#             if row[2] == '3' and row[3] in ('Adult', 'Short', 'Documentary'):
#                 avoid_ids.add(int(row[1]))
#     print('Number of movies to avoid:', len(avoid_ids))

#     titles = titles.drop(titles.select(avoid_ids.__contains__).index)

#     print('{:,}'.format(len(titles)))
#     print(titles.dtypes)
#     print(titles.head())

#     characters = pd.read_csv('char_name.csv', usecols=[0,1], index_col=0,
#                              names=['id', 'character'])
#     characters.sort_index()
#     print('Number of movie characters: {:,}'.format(len(characters)))

#     characters = characters.drop_duplicates()
#     print('{:,}'.format(len(characters)))

#     characters.head()

#     for i, role_type_name in enumerate((
#             None, 'actor', 'actress', 'producer', 'writer',
#             'cinematographer', 'composer', 'costume designer',
#             'director', 'editor', 'miscellaneous crew',
#             'production designer', 'guest')):
#         print(i, role_type_name)

#     if 'raw_cast' in dir():
#         del raw_cast

#     column_names = ['name_id', 'title_id', 'character_id', 'n', 'role_type']

#     raw_cast = pd.read_csv(
#         'cast_info.csv', usecols=[1,2,3,5,6], names=column_names,
#         dtype=dict.fromkeys(['name_id', 'title_id', 'title', 'role_type'], 'int32'))

#     print('{:,}'.format(len(raw_cast)))
#     print(raw_cast.dtypes)
#     raw_cast.head()


#     # In[17]:

#     if 'cast' in dir():
#         del cast

#     # Other columns:
#     # 3  Role id, or 1 if they appeared as themselves
#     # 4  Notes like "(archive footage)" and "(uncredited)"
#     # 5  Order of actor/actress in billing
#     # 6  Role type (see role types in previous cell)

#     # Only keep rows for actors and actresses, in named roles.

#     cast = raw_cast.loc[
#         ((raw_cast.role_type == 1) | (raw_cast.role_type == 2))
#         & raw_cast.character_id.notnull()
#         ].copy()

#     cast['type'] = cast.pop('role_type').map({1: 'actor', 2: 'actress'})

#     # Only keep rows that match our table of feature films.

#     print(cast.head())
#     cast = pd.merge(titles[['title', 'year']], cast,
#                     left_index=True, right_on='title_id', sort=False)
#     del cast['title_id']

#     cast = pd.merge(names[['name']], cast, left_index=True, right_on='name_id', sort=False)
#     del cast['name_id']

#     cast = pd.merge(characters[['character']], cast, left_index=True, right_on='character_id', sort=False)
#     del cast['character_id']

#     # Re-order columns

#     cast['year'] = cast['year'].astype('int32')

#     cast = cast[['title', 'year', 'name', 'type', 'character', 'n']]

#     print('{:,}'.format(len(cast)))
#     print(cast.dtypes)


#     # In[18]:

#     cast.drop_duplicates().reindex().head()


#     # In[19]:

#     cast[cast.title == 'Star Wars'].sort('n')


#     # # Release Dates

#     # In[20]:

#     def filter_csv(chunk):
#         r = chunk
#         r = r[r.code == 16]
#         #print(r.head())
#         r = r[r.note.isnull()]
#         r = r[['title_id', 'data']]
#         print(len(r), end=' '),
#         return r

#     iter_csv = pd.read_csv(
#         'movie_info.csv',
#         usecols=[1,2,3,4],
#         names=['title_id', 'code', 'data', 'note'],
#         dtype={'note': 'str'},
#         iterator=True,
#         chunksize=100000,
#         )
#     release_dates_raw = pd.concat([filter_csv(chunk) for chunk in iter_csv])
#     print()

#     release_dates_raw.head()


#     # In[21]:

#     r = release_dates_raw

#     r['country'] = r.data.str.extract('^(.*):')
#     r['date'] = r.data.str.extract(':(.*)$')
#     del r['data']

#     r['date'] = pd.to_datetime(r.date, infer_datetime_format=True)
#     release_dates_all = r
#     release_dates_all.head()


#     # In[22]:

#     release_dates = pd.merge(titles[['title', 'year']], release_dates_all,
#                              left_index=True, right_on='title_id', sort=False)
#     del release_dates['title_id']
#     release_dates = release_dates.drop_duplicates()
#     release_dates.head()


#     # # Save

#     # In[23]:

#     titles.to_csv('../data/titles.csv', index=False)


#     # In[24]:

#     cast.head()


#     # In[25]:

#     cast.to_csv('../data/cast.csv', index=False)


#     # In[26]:

#     release_dates.head()


#     # In[27]:

#     release_dates.to_csv('../data/release_dates.csv', index=False)


# def swap_names(name):
#     if ',' in name:
#         last, first = name.split(',', 1)
#         name = first.strip() + ' ' + last.strip()
#     return name


if __name__ == '__main__':
    main()
