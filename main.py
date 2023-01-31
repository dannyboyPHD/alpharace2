import pandas as pd
from pre_proc_CDF import*
from sim_engine import*
from io_control import*
# from parallel_tasks import*
import time
import cProfile

# So, while the light fails 
# On a winter's afternoon, in a secluded chapel
# History is now and England.


#------------------------------------------------
# data import
#------------------------------------------------
races = pd.read_csv('./data_full/race_db.csv')
horse_race_entries = pd.read_csv('./data_full/horse_race_data_db.csv')
# horses = pd.read_csv('./data/horse_test.csv')

#------------------------------------------------
# organise dataframes
#------------------------------------------------
races.set_index('race_id', inplace= True)
horse_race_entries.set_index('race_id',inplace =True)

#------------------------------------------------
# filter CDF
#------------------------------------------------
# r = races.loc[races['class'] == 5]

print('available classes: ', races['class'].unique())
print('available distances: ', races['distance'].unique())
print('available fees: ','min ', races['fee'].min(), 'max ',races['fee'].max())
#-------------------------------------------------
# cdf mgmt
#------------------------------------------------
# if dists, classes, fee == None no cdf filtering

# dists = gen_cdf_distancelist('distances',races)
dists = None
classes = None
fee = None

# distribute filtering jobs to each rank
cdf_names = gen_cdf_names(race_class = classes,distance = dists, fee = fee)
cdf_array = gen_cdf_array(race_class = classes,distance = dists, fee = fee)

# print(cdf_names)
#------------------------------------------------
# get r, hr pairs
#------------------------------------------------
# r, hr = get_horse_in_races(r,horse_race_entries,start_time = '2022-02-27 18:47:00', end_time = '2022-02-27 18:53:00')

mode = 'dump' # or 'update'
results = './testing/'

# potential parallet execution
# my_rank = comm.Get_rank()
# total_procs = comm.Get_size()
# cdf_ranks = gen_cdf_ranks(cdf_names,total_procs)
# print(cdf_ranks)

for cdf in range(len(cdf_names)):
    #cdf_names and cdf_array are equal length lists 
    classes = cdf_array[cdf][0]
    dists = cdf_array[cdf][1]
    fee = cdf_array[cdf][2]

    r = cdf_filtering(races, distance = dists,race_class = classes,fee = fee)
 
#   reading in done rank by rank for startup
    if mode == 'dump':
        r, hr = get_horse_in_races(r,horse_race_entries,'all_gates')
        # ,start_time = '2022-12-21 23:22:55')
        #,start_time='2022-09-01 18:46:00',end_time='2022-12-25 18:47:00')
        summary = None
    elif mode == 'update':
        summary = read_summary(results+cdf_names[cdf]+'_summary')
        archive = read_archive(results+cdf_names[cdf]+'_archive')
        lastrace = read_lastrace(results+cdf_names[cdf]+'_lastrace')
        r, hr = get_horse_in_races(r,horse_race_entries,start_time=lastrace)
#------------------------------------------------
# sim engine
#------------------------------------------------
    start = time.time()# may have to be done n master rank
#   main loop distributed rank by rank
    print(r)
    print(hr)
    summary,archive,last_race = sim_engine(r,hr,summary=summary)

    if last_race is not None:
        summary2csv(summary,name=results+cdf_names[cdf]+'_summary')
        archive2csv(archive,mode,name=results+cdf_names[cdf]+'_archive')
        last_race2csv(last_race,results+cdf_names[cdf]+'_lastrace')

    print('last race ', last_race)
    end = time.time()

print('total time elapsed: ', end - start)