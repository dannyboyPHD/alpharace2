import pandas as pd
import plotly.express as px


#--------------------------------------------------
#      data directory and reading in data
#--------------------------------------------------
data_dir = './results_test/'

#results csvs
summary = 'CallDallFall_summary.csv'
archive = 'CallDallFall_archive.csv'
last_race = 'CallDallFall_lastrace.csv'

summary = pd.read_csv(data_dir+summary)
archive = pd.read_csv(data_dir+archive)
last_race = pd.read_csv(data_dir+last_race)

#-------------------------------------------------
#   user input for horses to be analysed
#-------------------------------------------------

h = pd.read_csv('postproc_horses.csv')

required_hid = 195986

h_results = archive[archive['horse_id'] == required_hid]
n_races = [i for i in range(len(h_results))]


#--------------------------------------------------
#   reference dates for races
#--------------------------------------------------

r = pd.read_csv('./data_test/race_test.csv')
r.set_index('race_id', inplace=True)

r = r['start_time']

#--------------------------------------------------
# get appropriate races and dates for h in question
#--------------------------------------------------

r = r.loc[h_results['race_id']]
horse_names = pd.read_csv('./data_test/horse_test.csv')  # contains names, stables, parents ect..
horse_names.set_index('horse_id', inplace=True)

#--------------------------------------------------
#   merging race start_times
#--------------------------------------------------

h_results.set_index('race_id', inplace = True)

h = h_results.merge(r,on = 'race_id')

print(h)
print(horse_names)
#--------------------------------------------------
# pre - plotting
#--------------------------------------------------

h_id = h['horse_id'][0]
h_name = horse_names.loc[h_id]['name']
address = horse_names.loc[h_id]['address']


#--------------------------------------------------
# plotting
#--------------------------------------------------

fig = px.line(h,x = 'no_races', y = 'mean_speed_t',text = 'start_time',title = h_name+': '+str(h_id)+' @ '+address)
fig.update_traces(textposition="bottom right")
# fig.update_traces(mode='markers+lines')



fig.show()


















