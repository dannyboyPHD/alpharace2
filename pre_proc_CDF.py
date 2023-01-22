import pandas as pd
from itertools import product


def get_horse_in_races(r,hr,start_time = 0, end_time =0):
    
    if start_time != 0 and end_time != 0:
        r = r.loc[ (r['start_time']> start_time) & (r['start_time']<= end_time)]
        # strictly greater than means races at start_time excluded
        if 'num_horses' in r.columns:
            r = r.loc[r['num_horses']==12]

        
        r_ids = r.index
        hr = hr[hr.index.isin(r_ids)]
        
    elif start_time!=0 and end_time == 0:
        r = r.loc[ (r['start_time']> start_time)]
        # strictly greater than means races at start_time excluded
        
        if 'num_horses' in r.columns:
            r = r.loc[r['num_horses']==12]

        r_ids = r.index
        hr = hr[hr.index.isin(r_ids)]
    else:
        if 'num_horses' in r.columns:
            r = r.loc[r['num_horses']==12]

        r_ids = r.index.unique()
        hr = hr.loc[hr.index.isin(r_ids)]
    print(r)

    if 'num_horses' in r.columns:
        r = r.drop(columns = ['num_horses'])

    print('number of 12 place races: ', len(r))
    print('correspindng races in hr: ', len(hr)/12)

    # old_rids = set(r_ids) - set(hr.index.unique())

    # old_r = r.loc[old_rids]
    # print('missing races distances: ', old_r['distance'].unique())
    # print('missing races event_type: ', old_r['event_type'].unique())
    # print('earliest missing race: ', old_r[old_r['start_time']==old_r['start_time'].min()] )
    # print('latest missing race: ', old_r[old_r['start_time']==old_r['start_time'].max()] )
    # print('number of missing races: ', len(old_rids))
    # r_ids = hr.index.unique()

    # r = r.loc[r_ids]
    # print(len(r_ids),len(hr['horse_id']))
    # r_ids = r.index
    r = r.sort_values(by=['start_time'])
    print('number of races in this cdf: ', len(r_ids))
    print('earliest race in cdf: ', r[r['start_time']==r['start_time'].min()])
    print('latest race in cdf: ', r[r['start_time']==r['start_time'].max()])

    hr = pd.merge(hr,r['start_time'], left_index = True, right_index = True)
    hr = hr.sort_values(by = ['start_time', 'race_id'])
    #clean types
    hr['horse_id'] = hr['horse_id'].astype(int)
    hr['place'] = hr['place'].astype(int)
    hr['gate'] = hr['gate'].astype(int)

    return r,  hr


def cdf_filtering(races,race_class = None, distance = None,fee = None):
    if race_class is None and distance is None and fee is None:
        
        r = races
    else:
        if isinstance(race_class,list):
            pass
        elif race_class is None:
            pass
        else:
            race_class = [race_class]

        if isinstance(distance,list):
            pass
        elif distance is None:
            pass
        else:
            distance = [distance]
        if isinstance(fee,list):
            pass
        elif fee is None:
            pass
        else:
            fee = [fee]

 
    if distance is not None:
        r = races.loc[races['distance'].isin(distance)]
        
        if race_class is not None:
            r = r.loc[races['class'].isin(race_class)]
            if fee is not None:
                r = r.loc[races['fee'].isin(fee)]
        elif fee is not None:
            r = r.loc[races['fee'].isin(fee)]
            
    elif race_class is not None:
        r = races.loc[races['class'].isin(race_class)]
        if fee is not None:
                r = r.loc[races['fee']>fee]
    elif fee is not None:
        r = races.loc[races['fee']>fee]

    return r

def gen_cdf_names(race_class = None, distance = None,fee = None):
    if race_class is None and distance is None and fee is None:
        names = 'CallDallFall'
 
    if race_class is not None:
        classes = ['C'+str(c) for c in race_class]
        
    else:
        classes = ['Call']

    if distance is not None:
        dists = ['D'+str(d) for d in distance]
    else:
        dists = ['Dall']

    if fee is not None:
        if fee > 0.0:
            fee = ['Fpaid']
        else:
            fee = ['Ffree']
    else:
        fee = ['Fall']

    names = product(classes,dists)
    names = [''.join(list(n)) for n in names]

    names = product(names,fee)
    names = [''.join(list(n)) for n in names]
    return names

def gen_cdf_array(race_class = None, distance = None,fee = None):

    if race_class is None and distance is None and fee is None:
        classes = [None]
        dists = [None]
        fee = [None]
    else:
 
        if race_class is not None:
            classes = [c for c in race_class]
        
        else:
            classes = [None]

        if distance is not None:
            dists = [d for d in distance]
        else:
            dists = [None]

        if fee is not None:
            if fee > 0.0:
                fee = fee
            else:
                fee = -1
        else:
            fee = [None]

    cdf_inputs = list(product(classes,dists,fee))
    print(cdf_inputs)
    return cdf_inputs


def gen_cdf_distancelist(mode,races):
    if mode == 'distances':
        cdf = races['distance'].unique()
    elif mode == 'classes':
        cdf = races['class'].unique()
    elif mode == 'marathon':
        cdf = [2200,2400,2600]
    elif mode == 'mids':
        cdf = [1600,1800,2000]
    elif mode == 'sprint':
        cdf = [1000,1200,1400]
    elif mode == 'none':
        cdf = None
    
    return cdf
