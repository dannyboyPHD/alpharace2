import pandas as pd
import numpy as np
import math


def calc_elos(h_ids,hr_block,hr_off,sum_off,summary_work,r_id,n):

    
    k = 32/(n-1)

    for player in range(n):
        playerEloChange = 0

        currPlace = int(hr_block[player,hr_off['place']])

        currElo = summary_work[h_ids[player],sum_off['currELO']]
        
        for opponent in range(n):
            if player == opponent:
                continue

            oppPlace = int(hr_block[opponent,hr_off['place']])
            oppElo = summary_work[h_ids[opponent],sum_off['currELO']]

            if currPlace < oppPlace:
                S = 1.0
            elif currPlace == oppPlace:
                S = 0.5
            else:
                S = 0.0

            EA = 1 / (1.0 + math.pow(10.0, (oppElo- currElo) / 400.0))
                
                #calculate ELO change vs this one opponent, add it to our change bucket
                #I currently round at this point, this keeps rounding changes symetrical between EA and EB, but changes K more than it should
                # print(K,S,EA)
            playerEloChange += round(k * (S - EA))

        summary_work[h_ids[player],sum_off['last_race']] = r_id
        summary_work[h_ids[player],sum_off['currELO']] = currElo + playerEloChange
        summary_work[h_ids[player],sum_off['N']] += 1

    return summary_work
    

def calc_horse_speed(h_ids,hr_block,hr_off,sum_off,summary_work,distance,n): 
    
    for player in range(n):
        time = hr_block[player,hr_off['horse_time']] 
        curr_speed = (distance/time)*3.6 # KPH

        prev_mean_speed = summary_work[h_ids[player],sum_off['mean_speed']]
        N = summary_work[h_ids[player],sum_off['N']]
        mean_speed = (prev_mean_speed*(N -1) + curr_speed)/N

        #mean speed
        summary_work[h_ids[player],sum_off['mean_speed']] = mean_speed
        
        #max speed
        if curr_speed > summary_work[h_ids[player],sum_off['max_speed']]:
            summary_work[h_ids[player],sum_off['max_speed']] = curr_speed

        hr_block[player,hr_off['horse_speed']] = curr_speed
    return summary_work, hr_block                        
    

def update_ratios(h_ids,hr_block,hr_off,sum_off,summary_work,n):
    for player in range(n):
        place = int(hr_block[player,hr_off['place']])
        N = summary_work[h_ids[player],sum_off['N']]
        
        if place ==1:
            wr =  summary_work[h_ids[player],sum_off['WR']]
            wr = (wr*(N-1)+1)/N

            summary_work[h_ids[player],sum_off['WR']] = wr
        else:
            wr =  summary_work[h_ids[player],sum_off['WR']]
            wr = (wr*(N-1))/N

            summary_work[h_ids[player],sum_off['WR']] = wr

        if(place ==1)or(place == 2) or (place == 3):
            pr = summary_work[h_ids[player],sum_off['PR']]
            pr = (pr*(N-1)+1)/N

            summary_work[h_ids[player],sum_off['PR']] = pr
        else:
            pr = summary_work[h_ids[player],sum_off['PR']]
            pr = (pr*(N-1))/N

            summary_work[h_ids[player],sum_off['PR']] = pr

        #DHR
        if (place == 1) and ( int(hr_block[player,hr_off['fire']]) != 1):
            dhr = summary_work[h_ids[player],sum_off['DHR']]
            dhr = (dhr*(N-1)+1)/N

            summary_work[h_ids[player],sum_off['DHR']] = dhr
        else:
            dhr = summary_work[h_ids[player],sum_off['DHR']]
            dhr = (dhr*(N-1))/N

            summary_work[h_ids[player],sum_off['DHR']] = dhr

        #HM ratio
        if (place == 4) and (int(hr_block[player,hr_off['fire']])==1):
            hm = summary_work[h_ids[player],sum_off['HM']]
            hm = (hm*(N-1)+1)/N

            summary_work[h_ids[player],sum_off['HM']] = hm
        else:
            hm = summary_work[h_ids[player],sum_off['HM']]
            hm = (hm*(N-1))/N

            summary_work[h_ids[player],sum_off['HM']] = hm

        # histogram update
        place_tag = "no_"+str(place)
        summary_work[h_ids[player],sum_off[place_tag]] += 1
    

    return summary_work

    


def update_profitability(h_ids,hr_block,hr_off,sum_off,summary_work,f,p,n):
    places = ['first','second','third','fourth','fifth','sixth'\
        ,'seventh','eighth','ninth','tenth','eleventh','twelfth']
    # print(places)
    for player in range(n):
        summary_work[h_ids[player],sum_off['costs']] += f

        place = int(hr_block[player,hr_off['place']])
        # print(place)
        # print(places[place-1])

        summary_work[h_ids[player],sum_off['revenue']] += p[places[place-1]]

        rev = summary_work[h_ids[player],sum_off['revenue']]
        costs = summary_work[h_ids[player],sum_off['costs']]
        summary_work[h_ids[player],sum_off['profit']] = rev - costs
        if costs == 0:
            summary_work[h_ids[player],sum_off['roi']] = 0
        else:
            summary_work[h_ids[player],sum_off['roi']] = (rev - costs)/costs

    return summary_work



        




