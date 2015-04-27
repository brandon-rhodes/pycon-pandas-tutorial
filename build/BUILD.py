"""Build the tutorial data files from the IMDB *.list.gz files."""

import csv
import gzip
import os
import re
from datetime import datetime

split_on_tabs = re.compile(b'\t+').split

def main():
    os.chdir(os.path.dirname(__file__))
    if not os.path.isdir('../data'):
        os.makedirs('../data')

    # Load movie titles.

    titles = set()
    uninteresting_titles = set()

    lines = iter(gzip.open('genres.list.gz'))
    line = next(lines)
    while line != b'8: THE GENRES LIST\n':
        line = next(lines)
    assert next(lines) == b'==================\n'
    assert next(lines) == b'\n'

    print('Reading "genres.list.gz" to find interesting movies')

    for line in lines:
        if not_a_real_movie(line):
            continue

        fields = split_on_tabs(line.strip(b'\n'))
        raw_title = fields[0]
        genre = fields[1]

        try:
            raw_title.decode('ascii')
        except UnicodeDecodeError:
            continue

        if genre in (b'Adult', b'Documentary', b'Short'):
            uninteresting_titles.add(raw_title)
        else:
            titles.add(raw_title)

    interesting_titles = titles - uninteresting_titles
    del titles
    del uninteresting_titles

    print('Found {0} titles'.format(len(interesting_titles)))

    print('Writing "titles.csv"')

    with open('titles.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(('title', 'year'))
        for raw_title in interesting_titles:
            title_and_year = parse_title(raw_title)
            w.writerow(title_and_year)

    print('Finished writing "titles.csv"')
    print('Reading release dates from "release-dates.list.gz"')

    lines = iter(gzip.open('release-dates.list.gz'))
    line = next(lines)
    while line != b'RELEASE DATES LIST\n':
        line = next(lines)
    assert next(lines) == b'==================\n'

    output = csv.writer(open('release_dates.csv', 'w'))
    output.writerow(('title', 'year', 'country', 'date'))

    for line in lines:
        if not_a_real_movie(line):
            continue

        if line.startswith(b'----'):
            continue

        fields = split_on_tabs(line.strip(b'\n'))
        if len(fields) > 2:     # ignore "DVD premier" lines and so forth
            continue

        raw_title = fields[0]
        if raw_title not in interesting_titles:
            continue

        title, year = parse_title(raw_title)
        if title is None:
            continue

        country, datestr = fields[1].decode('ascii').split(':')
        try:
            date = datetime.strptime(datestr, '%d %B %Y').date()
        except ValueError:
            continue  # incomplete dates like "April 2014"
        output.writerow((title, year, country, date))

    print('Finished writing "release_dates.csv"')


def not_a_real_movie(line):
    return (
        line.startswith(b'"')       # TV show
        or b'{' in line             # TV episode
        or b' (????' in line        # Unknown year
        or b' (TV)' in line         # TV Movie
        or b' (V)' in line          # Video
        or b' (VG)' in line         # Video game
        )


match_title = re.compile(r'^(.*) \((\d+)(/[IVXL]+)?\)$').match

def parse_title(raw_title):
    try:
        title = raw_title.decode('ascii')
    except UnicodeDecodeError:
        return None, None

    m = match_title(title)
    title = m.group(1)
    year = int(m.group(2))
    numeral = m.group(3)

    if numeral is not None:
        numeral = numeral.strip('/')
        if numeral != 'I':
            title = '{} ({})'.format(title, numeral)

    return title, year

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


#     # In[24]:

#     cast.head()


#     # In[25]:

#     cast.to_csv('../data/cast.csv', index=False)


# def swap_names(name):
#     if ',' in name:
#         last, first = name.split(',', 1)
#         name = first.strip() + ' ' + last.strip()
#     return name


if __name__ == '__main__':
    main()
