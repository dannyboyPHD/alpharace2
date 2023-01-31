import pandas as pd
import numpy as np
from calculations import*
import time
import json

def race_id2integer(r,hr,summary=None):
    r_dict = {}
    rev_r_dict = {}

    r_ids = r.index
    total_races = len(r_ids)

    for i in range(total_races):
        r_dict[r_ids[i]] = i

    if summary is not None:
        last_races = summary['last_race'].unique()
        for i in range(len(last_races)):
            # print('previous races: ',last_races[i])
            # print(total_races + i)
            r_dict[last_races[i]] = total_races + i

    rev_r_dict = {value:key for (key,value) in r_dict.items()}

    return r_dict, rev_r_dict


def horse_id2integer(summary):
    # needs summary functionality
    h_dict = {}
    rev_h_dict = {}
    # print(hr)
    h_ids = summary['horse_id'].unique()
    total_horses = len(h_ids)

    for i in range(total_horses):
        h_dict[h_ids[i]] = i
    rev_h_dict = {value:key for (key,value) in h_dict.items()}
    return h_dict, rev_h_dict
            

def create_work_array(r,hr,r_dict,h_dict):
    # archive style numpy array ready to be interated for elo calc and 
    # win rates ect.
    hr = hr.reset_index()
    columns = ['race_id',\
            'horse_id',\
            'fire',\
            'place',\
            'horse_time',\
            'gate',\
            'horse_speed',\
            'preELO',\
            'WR_t',\
            'PR_t',\
            'DHR_t',\
            'HM_t',\
            'no_races',\
            'no_1',\
            'no_2',\
            'no_3',\
            'no_4',\
            'no_5',\
            'no_6',\
            'no_7',\
            'no_8',\
            'no_9',\
            'no_10',\
            'no_11',\
            'no_12',\
            'max_speed_t',\
            'mean_speed_t',\
            'revenue_t',\
            'costs_t',\
            'profit_t',\
            'roi_t']
    off = [i for i in range(len(columns))]
    hr_offs = dict(zip(columns,off))

    hr_work = pd.DataFrame(columns = columns)
    start_times = pd.DataFrame(columns = ['start_time'])
    start_times['start_time'] = hr['start_time']
    # code in known values
    hr_work['race_id'] = hr['race_id']
    hr_work['horse_id'] = hr['horse_id']
    hr_work['fire'] = hr['fire']
    hr_work['place'] = hr['place']
    hr_work['horse_time'] = hr['horse_time']
    hr_work['gate'] = hr['gate']
    # apply dicts
    hr_work['horse_id'] = hr_work['horse_id'].map(h_dict)
    hr_work['race_id'] = hr_work['race_id'].map(r_dict)
    # print(hr_work)
    hr_work  = hr_work.to_numpy()
    # print(hr_work)

    return hr_work, start_times,hr_offs

def create_race_lookup(r,race_dict):
    pass

def create_summary(hr,r_dict,summary=None):
    column_headings = ['horse_id',\
            'last_race',\
            'currELO',\
            'WR',\
            'PR',\
            'DHR',\
            'HM',\
            'N',\
            'no_1',\
            'no_2',\
            'no_3',\
            'no_4',\
            'no_5',\
            'no_6',\
            'no_7',\
            'no_8',\
            'no_9',\
            'no_10',\
            'no_11',\
            'no_12',\
            'max_speed',\
            'mean_speed',\
            'revenue',\
            'costs',\
            'profit',\
            'roi']

    off = [i for i in range(len(column_headings))]
    summary_offsets = dict(zip(column_headings,off))

    if summary is not None:
        
        inhr_h_ids = hr['horse_id'].unique()
        curr_h_ids = summary['horse_id']

        new_h_ids = set(inhr_h_ids) - set(curr_h_ids)
        
        add_tab = pd.DataFrame(columns = column_headings)
        
        add_tab['horse_id'] = list(new_h_ids)
        add_tab[:] = 0.0
        add_tab['horse_id'] = list(new_h_ids)
        add_tab['currELO'] = 1000

        summary = summary.append(add_tab, ignore_index = True)

        # print(len(curr_h_ids))
        # print(len(new_h_ids))
        # print(len(inhr_h_ids))
        print('all horses now present: ', len(curr_h_ids)+len(new_h_ids))

    else:
        h_ids = hr['horse_id'].unique()
        total_horses = len(h_ids)
        
        summary = pd.DataFrame(columns = column_headings)
     
        summary['horse_id'] = h_ids
        summary[:] = 0.0
        summary['horse_id'] = h_ids
        summary['currELO'] = 1000
    #mapping to integer labels
    summary['last_race'] = summary['last_race'].map(r_dict)
    return summary.to_numpy(),summary, summary_offsets




def load_prerace_values(h_ids,hr_block,hr_off,sum_off, summary_work,n):
    for i in range(n):
        hr_block[i,hr_off['horse_speed']] = 0 # unitialised, dealt with in ratio
        hr_block[i,hr_off['preELO']] = summary_work[h_ids[i],sum_off['currELO']]
        hr_block[i,hr_off['WR_t']] = summary_work[h_ids[i],sum_off['WR']]
        hr_block[i,hr_off['PR_t']] = summary_work[h_ids[i],sum_off['PR']]
        hr_block[i,hr_off['DHR_t']] = summary_work[h_ids[i],sum_off['DHR']]
        hr_block[i,hr_off['HM_t']] = summary_work[h_ids[i],sum_off['HM']]
        hr_block[i,hr_off['no_races']] = summary_work[h_ids[i],sum_off['N']]
        hr_block[i,hr_off['no_1']] = summary_work[h_ids[i],sum_off['no_1']]
        hr_block[i,hr_off['no_2']] = summary_work[h_ids[i],sum_off['no_2']]
        hr_block[i,hr_off['no_3']] = summary_work[h_ids[i],sum_off['no_3']]
        hr_block[i,hr_off['no_4']] = summary_work[h_ids[i],sum_off['no_4']]
        hr_block[i,hr_off['no_5']] = summary_work[h_ids[i],sum_off['no_5']]
        hr_block[i,hr_off['no_6']] = summary_work[h_ids[i],sum_off['no_6']]
        hr_block[i,hr_off['no_7']] = summary_work[h_ids[i], sum_off['no_7']]
        hr_block[i,hr_off['no_8']] = summary_work[h_ids[i], sum_off['no_8']]
        hr_block[i,hr_off['no_9']] = summary_work[h_ids[i], sum_off['no_9']]
        hr_block[i,hr_off['no_10']] = summary_work[h_ids[i], sum_off['no_10']]
        hr_block[i,hr_off['no_11']] = summary_work[h_ids[i], sum_off['no_11']]
        hr_block[i,hr_off['no_12']] = summary_work[h_ids[i], sum_off['no_12']]
        hr_block[i,hr_off['max_speed_t']] = summary_work[h_ids[i], sum_off['max_speed']]
        hr_block[i,hr_off['mean_speed_t']] = summary_work[h_ids[i], sum_off['mean_speed']]
        hr_block[i,hr_off['revenue_t']] = summary_work[h_ids[i], sum_off['revenue']]
        hr_block[i,hr_off['costs_t']] = summary_work[h_ids[i], sum_off['costs']]
        hr_block[i,hr_off['profit_t']] = summary_work[h_ids[i], sum_off['profit']]
        hr_block[i,hr_off['roi_t']] = summary_work[h_ids[i], sum_off['roi']]

    return hr_block

def gen_race_lookup(r):
    # new format
    if 'num_horses' in r.columns:
        r_tmp = r[['distance','fee','prize_pool_first','prize_pool_second',\
            'prize_pool_third','prize_pools','start_time','num_horses']]
    # legacy format
    else:
        r_tmp = r[['distance','fee','prize_pool_first','prize_pool_second',\
            'prize_pool_third','start_time']]
        r_tmp.insert(6,'num_horses',12)

    off = [i for i in range(len(r_tmp.columns))]
    race_offsets = dict(zip(r_tmp.columns,off))

    last_race = r_tmp['start_time'].max()
    
    r = r_tmp.to_numpy()
    return r, race_offsets,last_race

    

def update_summary():
    pass


                             

def sim_engine(r,hr,summary=None):
    race_dict = {}
    rev_race_dict = {}

    horse_dict = {}
    rev_horse_dict = {}

    race_dict,rev_race_dict = race_id2integer(r,hr,summary=summary)

    # print('check race_dict ', race_dict['FpjUUWKI'])

    summary_work,summary,summary_offsets = create_summary(hr,race_dict,summary=summary)

    horse_dict, rev_horse_dict = horse_id2integer(summary)    

    hr_work, start_times,hr_offsets = create_work_array(r,hr,race_dict,horse_dict)

    race_lookup,race_off,last_race = gen_race_lookup(r)

    # print(hr_work)

    # print(race_lookup[:,race_off['distance']])
    # create summary from fresh hr_work, as well as w/ existing summary


    n_races = len(race_lookup)
    print('number of races', n_races)
    start = time.time()
    # indexing and slicing variables
    a = 0 
    b = 0

    # prize pool mode
    if 'prize_pools' in r.columns:
        prize = 'modern'
    else:
        prize = 'legacy'


    for r in range(n_races):
        #flexible 6 or 12 horse races
        num_h = race_lookup[r,race_off['num_horses']]
        a = b
        b = a + num_h

        h_ids = hr_work[a:b,hr_offsets['horse_id']]

        # load current stats from summary inot hr_work array
        hr_work[a:b,:] = \
            load_prerace_values(h_ids, hr_work[a:b,:],\
                hr_offsets,summary_offsets,summary_work,num_h)

        # calc new elos
        summary_work = calc_elos(h_ids,hr_work[a:b,:],\
            hr_offsets,summary_offsets,summary_work,r,num_h)
            # N += 1 inside calc_elos
            # affects order inwhich calc fcn can be called

        d = race_lookup[r,race_off['distance']]

        summary_work,hr_work[a:b,:] =\
            calc_horse_speed(h_ids,hr_work[a:b,:],\
            hr_offsets,summary_offsets,summary_work,d,num_h)

        summary_work = update_ratios(h_ids,hr_work[a:b,:],\
            hr_offsets,summary_offsets,summary_work,num_h)

        if prize == 'modern':
            p = race_lookup[r,race_off['prize_pools']]
            p = json.loads(p)
            fee = race_lookup[r,race_off['fee']]
            # print(p['total'])
            update_profitability(h_ids,hr_work[a:b,:]\
            ,hr_offsets,summary_offsets,\
            summary_work,fee,p,num_h)



    # timings and remapping
    end = time.time()
    print('time elapsed: ', end - start)
    if n_races != 0:
        print('time per race: ', (end-start)/n_races)

        s = pd.DataFrame(summary_work, columns = summary.columns )
        s['last_race'] = s['last_race'].map(rev_race_dict)
        archive = pd.DataFrame(hr_work,columns = hr_offsets.keys())
        archive['race_id'] = archive['race_id'].map(rev_race_dict)
        archive['horse_id'] = archive['horse_id'].map(rev_horse_dict)
    else:
        print('no races in update')
        s = None
        archive = None
        last_race = None
    return s, archive,last_race
        
    
    