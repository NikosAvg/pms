import matplotlib.pyplot as plt
import numpy as np
import math
plt.style.use('fivethirtyeight')
import pandas as pd
plt.rcParams['figure.dpi'] = 150

file = open("./Package_1557150186325-NOA_816878_NOA.txt","r")
#data = pd.read_csv('signal_data.csv')

data = []
for f in file:
    data = f.split()
    
for i in range(len(data)):
    data[i] = int(data[i])
L = pd.Series(data)
#L = data.values
def VarianceFunction(positions):
    positions = pd.Series(positions)
    T = [i for i in range(2,22,2)]
    var0 = positions.var()
    result = [(positions.rolling(window=t).mean()).dropna().var()/var0 for t in T]
    return [result,T]

diff = []
for i in range(1,len(L)):
    value = L[i] - L[i-1]
    diff.append(value)

def SO(data,window,step):
    rc = []
    L = pd.Series(data)
    start = 0
    end = start + window
    while(end <= len(L)):
        test1 = L[start:end]
        varfunc1 = VarianceFunction(test1)
        CorCoef1 = np.corrcoef(np.log(varfunc1[0]), np.log(varfunc1[1]))[0,1]
        if(np.abs(CorCoef1) < 0.95):
            minval1 = np.min(test1)
            l = (np.max(test1) - np.min(test1))/np.min(test1) #growth parameter of the Verhulst model
            transf_data1 = [np.log(t+1-minval1) - l for t in test1]
            varfunc3 = VarianceFunction(transf_data1)
            CorCoef2 = np.corrcoef(np.log(varfunc3[0]), np.log(varfunc3[1]))[0,1]
            if( np.abs(CorCoef2) > 0.99):
                print(start)
                print(end)
                print("1 ,",CorCoef1)
                print("2 ,",CorCoef2)
                rc.append(test1)
                break
        start += step
        end += step
    return rc
s = SO(diff, window=100, step=1)
j = [[i.index.stop, i.values[-1]] for i in s]
plt.plot(L,'bo')
for i in j:
    plt.axvline(x = i[0], color='red', linewidth=0.5)
plt.show()
print(j)
