import numpy as np
import random
import matplotlib.pyplot as plt
# %matplotlib inline
import networkx as nx

# 生成小世界网络
def small_world(N, d, a):
    random.seed(1024)
    A = np.zeros((N, N))

    for i in range(N):                          
        t = 0
        while t < (d/2):
            A[i][i-(t+1)] = 1
            A[i-(t+1)][i] = 1
            t += 1

    for i in range(N):  
        t = 0
        while t < (N/2):
            if A[i][i-(t+1)] == 1:        
                if random.random() < a:         
                    A[i][i-(t+1)] = 0                   
                    A[i-(t+1)][i] = 0
                    target = random.randint(0,(N-1))
                    while A[i][target] == 1 or target == i: 
                        target = random.randint(0,(N-1))
                    A[i][target] = 1                    
                    A[target][i] = 1
            t += 1
    return A

# 随机零号病人
def patient_zero_rand(N,num):
    Infecters = random.sample(range(N),num)
    InfectStatus = np.zeros(N,int)            
    for i in Infecters:
        InfectStatus[i] = 1                   
    return InfectStatus

# 初始化零号病人
def patient_zero_given(N, id):
    InfectStatus = np.zeros(N,int)            
    InfectStatus[id] = 1                   
    return InfectStatus

# 感染过程
def infect(A, S, beta, gamma=0):        
    N = len(A)
    for i in range(N):
        if S[i] == 1 and random.random() <= gamma:
            S[i] = 2
 
    if sum(S==1) < N/2:                 
        for i in range(N):               
            if S[i] == 1:
                for j in range(N):
                    if A[i][j] == 1 and S[j] == 0 and random.random() <= beta:
                        S[j] = 1        
    else:
        for i in range(N):
            if S[i] == 0:
                for j in range(N):
                    if A[i][j] == 1 and S[j] == 1 and random.random() <= beta:
                        S[i] = 1
    return S

# 网络中的 SIR 过程
def SIR(A, N0, Beta, Gamma):
    # print("Beta: ", Beta)
    # print("Gamma: ", Gamma)
    N = len(A)
    S = patient_zero_given(N, N0)

    result = []
    time = 0
    while True:
        result.append((sum(S==0), sum(S==1), sum(S==2)))
        print(N0, time, (sum(S==0), sum(S==1), sum(S==2)))
        if sum(S==1) == N or sum(S==1) == 0:
            break
        
        S = infect(A, S, Beta, Gamma) 
        time += 1
    
    return np.array(result)

# C = small_world(1000,4,0.2)    
# result = SIR(C,2,0.3,0.1)