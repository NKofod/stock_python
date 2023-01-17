import numpy as np 
import scipy.special as special 
import time 
from statistics import mean 


def election_area(): 
    prob_party = np.random.randint(0,100,13)
    prob_party = special.softmax(prob_party)*100
    prob_switch = np.random.randint(0,100,(13,13))
    tmp_mat = prob_party @ prob_switch
    tmp_mat = tmp_mat / sum(tmp_mat)
    return tmp_mat

tmp_time = []

for i in range(10000): 
    if i % 100 == 0 and tmp_time != []:
        print(mean(tmp_time))
    start_time = time.time()
    for j in range(1347): 
        election_area()
    end_time = time.time()

    tmp_time.append(end_time - start_time)

print(mean(tmp_time))