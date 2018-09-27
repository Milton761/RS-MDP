import time
from ssp import *
from math import *
from copy import deepcopy


def pi_e(ssp, lambdaf, p0, error=0.000001):

    def sign(x): return (1, -1)[x < 0]

    P = p0

    t0 = time.clock()


    flag = True
    counter = 0

    while flag:
        print(counter)
        counter += 1
        
        V = policyEvaluation(ssp, P, lambdaf)

        P1 = {}

        for s in ssp._S:
            # print("--------------------------")
            #print("state: ", s)
            tmpV = []
            tmpP = []

            for a in ssp.App(s):
                # cprint("Action",a)
                acc = 0
                for s1 in ssp._S:
                    if not s1 in ssp._G:
                        acc = exp(lambdaf*ssp.C(s, a)) * ssp.P(s, a, s1)*V[s1] + acc
                        

                acc = exp(lambdaf*ssp.C(s, a)) * ssp.P(s, a, ssp._G[0])*sign(lambdaf) + acc
            
                tmpV.append(acc)
                tmpP.append(a)
        
            if len(tmpV) == 0:
                P1[s] = 'abs'
            else:
                minV = float('inf')
                for i in range(len(tmpV)):
                    if tmpV[i] < minV:
                        P1[s] = tmpP[i]
                        minV = tmpV[i]

        if P1==P:
            flag = False
            P = P1
        else:
            P = deepcopy(P1)


    R = {}
    R['policy'] = P
    return R

def policyEvaluation(ssp, policy, factor, error = 0.000001):
    
    def sign(x): return (1, -1)[x < 0]
    P = policy
    V = {}

    for s in ssp._S:
        V[s] = 2

    flag = True
    counter = 0
    for i in range(50):
        
        # print(counter)
        counter += 1
        for s in ssp._S:
            acc = 0
            V1 = deepcopy(V)

            for s1 in ssp._S:
                if not s1 in ssp._G:
                    acc = exp(factor*ssp.C(s, P[s])) * ssp.P(s, P[s], s1)*V[s1] + acc
                    #print("to -> " + s1," ",str(V1[s1]) + " " + str(acc))
                    # print(acc)
                acc = exp(factor*ssp.C(s, P[s])) * ssp.P(s, P[s], ssp._G[0])*sign(factor) + acc
            

     
    return V
                
            


def vi_e(ssp, lambdaf, error=0.000001, verbose=0, time_limit=60):

    def sign(x): return (1, -1)[x < 0]

    V = {}
    P = {}

    t0 = time.clock()

    for s in ssp._S:
        V[s] = 2

    flag = True

    counter = 0

    # for i in range(200):
    while flag:

        counter = counter + 1
        #print("New Iteration")
        V1 = deepcopy(V)
        locale = 0
        
        for s in ssp._S:
            # print("--------------------------")
            #print("state: ", s)

            v = V[s]
            tmpVal = []
            tmpAct = []

            for a in ssp.App(s):
                # cprint("Action",a)
                acc = 0
                for s1 in ssp._S:
                    if not s1 in ssp._G:
                        acc = exp(lambdaf*ssp.C(s, a)) *  ssp.P(s, a, s1)*V1[s1] + acc
                    

                acc = exp(lambdaf*ssp.C(s, a)) * ssp.P(s, a, ssp._G[0])*sign(lambdaf) + acc
                
                tmpVal.append(acc)
                tmpAct.append(a)

            if len(tmpVal) == 0:
                V[s] = 0
                P[s] = 'abs'
            else:
                minV = float('inf')
            
                for i in range(len(tmpVal)):
                    if tmpVal[i] < minV:
                        P[s] = tmpAct[i]
                        V[s] = tmpVal[i]
                        minV = tmpVal[i]
                locale = max(locale,abs(v-V[s]))

        if time.clock()-t0 >= time_limit:
            break
            
       
        if locale < 0.001:
            flag = False
        #print("N Iterations : ", counter)

    total_time = time.clock() - t0

    if total_time >= time_limit:
        total_time = -1

    R = {'value_function': V, 'policy': P, 'time': total_time}

    return R


# [V, P]=vi_e(ssp, 0.1, 0)

# for s in V:
#     print(s, V[s])

# print("---Policy---")
# for s in P:
#     print(s, P[s])
