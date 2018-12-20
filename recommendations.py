# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 11:20:08 2018

@author: Rakesh Maharjan
"""

# A dictionary of movie critics and their ratings of a small set of movies

critics = {'Lisa Rose' : {'Lady in the water' : 2.5, 'Snake on a plane' : 3.5,
                          'Just My Luck' : 3.0, 'Superman Returns' : 3.5,
                          'You, Me and Dupree' : 2.5, 'The Night Listener' : 3.0},
            'Gene Seymour' : {'Lady in the water' : 3.0, 'Snake on a plane' : 3.5,
                              'Just My Luck' : 1.5, 'Superman Returns' : 5.0,
                              'You, Me and Dupree' : 3.0, 'The Night Listener' : 3.5},
            'Michael Phillips' : {'Lady in the water' : 2.5, 'Snake on a plane' : 3.0,
                                  'Superman Returns' : 3.5,'The Night Listener' : 4.0},
            'Claudia Puig' : {'Lady in the water' : 2.5, 'Snake on a plane' : 3.5,
                              'Superman Returns' : 4.0,
                              'You, Me and Dupree' : 2.5, 'The Night Listener' : 4.5},
            'Mick LaSalle' : {'Lady in the water' : 3.0, 'Snake on a plane' : 4.0,
                              'Just My Luck' : 2.0, 'Superman Returns' : 3.0,
                              'You, Me and Dupree' : 2.0, 'The Night Listener' : 3.0},
            'Jack Matthews' : {'Lady in the water' : 3.0, 'Snake on a plane' : 4.0,
                              'Superman Returns' : 5.0,
                              'You, Me and Dupree' : 3.5},
            'Toby' : {'Snake on a plane' : 4.5,
                      'Superman Returns' : 5.0,
                      'You, Me and Dupree' : 1.0}}

from math import sqrt

# Returns a distance-based similarity score for person1 and Person2
def sim_distance(prefs, person1, person2):
    #Get the list of the shared items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
            
    # if they have no ratings in common return 0
    if len(si) == 0 : 
        return 0
    
    # Add up the squares of all the differences 
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                    for item in prefs[person1] if item in prefs[person2]])
    
    return 1/(1 + sum_of_squares)

# Returns the Pearson correlation coeffecient for p1 and p2

def sim_pearson(prefs, p1, p2):
    #Get the list of the mutually rated items
    
    si ={}
    
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    
    # Find the number of elements         
    n = len(si)
    
    # if there are no ratings in common 0
    if n == 0:
        return 0
    
    # Add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # sum up the squares
    sum1sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2sq = sum([pow(prefs[p2][it], 2) for it in si])

    # sum up the produts
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calculate Pearson Score
    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1sq - pow(sum1, 2)/n) * (sum2sq - pow(sum2, 2)/n))
    if den == 0:
        return 0
    
    r = num/den
    
    return r


# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional parms.

def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    
    # sort the list so the highest score appear at the top
    scores.sort()
    scores.reverse()
    return scores[0 : n]

# Gets recommendations for a person by using a weighted average 
# of every other user's rankings

def getRecommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare to myself
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        
        #ignore scores of zero or lower
        if sim <= 0:
            continue
    for item in prefs[other]:
        #only score movie I haven't seen yet
        if item not in prefs[person] or prefs[person][item] == 0:
            #similarity * score
            totals.setdefault(item, 0)
            totals[item] += prefs[other][item]*sim
            #sum of similarities
            simSums.setdefault(item,0)
            simSums[item] += sim
            
    # Create the normalized list
    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    
    #Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

getRecommendations(critics, 'Toby', similarity=sim_distance)
    
    
    
    

