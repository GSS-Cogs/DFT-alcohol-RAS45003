# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Table RAS45003 Reported road casualties by severity (estimates): Great Britain, quarterly and annual

# +
from gssutils import *

scraper = Scraper('https://www.gov.uk/government/statistical-data-sets/ras45-quarterly-statistics')
scraper
# -

df = scraper.distribution(
    title='Reported road casualties by severity (estimates): Great Britain, quarterly and annual'
).as_pandas(sheet_name='ras45003', start_row = 6,
            row_limit = 30, start_column = 0, column_limit = 7)
observations = df.rename(columns=df.iloc[0]).drop(df.index[0])
observations

observations.columns.values[0] = 'Year'
observations.columns.values[1] = 'Quarter'
observations.columns.values[2] = 'killed'
observations.columns.values[3] = 'ksi'
observations.columns.values[4] = 'slightly-injured'
observations.columns.values[5] = 'total'
observations.columns.values[6] = 'motor-traffic'

new_table = pd.melt(observations,
                       ['Year','Quarter'], var_name="Severity",
                       value_name="Value")


# +
def user_perc(x):
    
    if str(x) == '2010-2014 average':
        return 'Average Count'
    else:
        return 'Count'
    
new_table['Measure Type'] = new_table.apply(lambda row: user_perc(row['Year']), axis = 1)


# +
def user_perc(x):
    
    if (str(x) == 'Q1(P)') | (str(x) == 'Q2(P)') :
        return 'Provisional'
    else:
        return 'Original Value'
    
new_table['Revision'] = new_table.apply(lambda row: user_perc(row['Quarter']), axis = 1)
# -

new_table.Year = new_table.Year[new_table.Year.str.strip() != '']

new_table.Year = new_table.Year.ffill()

new_table['Quarter'] = new_table['Quarter'].str.rstrip('(P)')

# +
new_table['Year'] = new_table['Year'].map(str)
new_table['Quarter'] = new_table['Quarter'].map(str)
def user_perc(x,y):    
    if x.strip() == '':
        return 'year/'+ y
    else:
        return 'quarter/'+ y +'-'+ x        
    
new_table['Period'] = new_table.apply(lambda row: user_perc(row['Quarter'], row['Year']), axis = 1)
# -

new_table['Unit'] = 'casualties'

new_table['Period'] = new_table['Period'].map(
    lambda x: {
        'year/2010-2014 average' : 'gregorian-interval/2010-01-01T00:00:00/P4Y'
        }.get(x, x))

new_table = new_table[['Period','Severity','Measure Type','Value','Unit','Revision']]

# +
from pathlib import Path

out = Path('out')
out.mkdir(exist_ok=True, parents=True)

new_table.to_csv(out / 'observations.csv', index = False)
# -

scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(out / 'dataset.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

new_table


