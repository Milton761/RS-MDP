
# Copyright 2018, Gurobi Optimization, LLC

# This example formulates and solves the following simple MIP model:
#  maximize
#        x +   y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#  x, y, z binary


from gurobipy import *
from ssp import *
from math import *
import time

# pylint: disable=E0602

# try:
    
#     # Create a new model
#     m = Model("mip1")

#     # Create variables
#     x = m.addVar(vtype = GRB.BINARY, name="x")
#     y = m.addVar(vtype = GRB.BINARY, name="y")
#     z = m.addVar(vtype = GRB.BINARY, name="z")

#     # Set objective
#     m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

#     # Add constraint: x + 2 y + 3 z <= 4
#     m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

#     # Add constraint: x + y >= 1
#     m.addConstr(x + y >= 1, "c1")

#     m.optimize()

#     for v in m.getVars():
#         print('%s %g' % (v.varName, v.x))

#     print('Obj: %g' % m.objVal)
 
# except GurobiError as e:
#     print('Error code ' + str(e.errno) + ": " + str(e))

# except AttributeError:
#     print('Encountered an attribute error')


def lp_ssp_GRB(ssp, verbose = 0):
    
    
    m = Model('LP - SSP')

    Vars = {}
    s_a = {}

    for s in ssp.S:
        var_name = None
        # in vars
        var_name = 'IN_' + s
        Vars[var_name] = m.addVar(vtype=GRB.SEMICONT, name = var_name)

        #out vars
        var_name = 'OUT_'+s
        Vars[var_name] = m.addVar(vtype=GRB.SEMICONT, name = var_name)

        #occupation measure vars
        for a in ssp.App(s):
            var_name = s + a
            Vars[var_name] = m.addVar(vtype=GRB.SEMICONT, name = var_name)
            s_a[var_name] = [s,a]

    #set objective
    r_side = 0
    for s in ssp.S:
        for a in ssp.App(s):
            var_name = s + a
            r_side += Vars[var_name]*ssp.C(s,a)
	
    m.setObjective(r_side, GRB.MINIMIZE)

    #Add constraints
    # C1

    for var in Vars:
        m.addConstr(Vars[var] >= 0)

    #C2
    for s in ssp.S:
        r_side = 0
        flag = False
        for s1 in ssp.S:
            for a in ssp.App(s1):
                if ssp.P(s1,a,s) > 0:
                    #add in var
                    flag = True
                    r_side += Vars[s1+a]*ssp.P(s1, a, s) 

        if flag:
            m.addConstr(Vars['IN_'+s] == r_side)
            
    #C3
    for s in ssp.S:
        if not s in ssp.G:
            flag = False
            r_side = 0
            for a in ssp.App(s):
                r_side += Vars[s+a]
                flag = True
            if flag:
                m.addConstr(Vars["OUT_"+s] == r_side)

    #C4
    for s in ssp.S:
        if not (s==ssp.s0 or s in ssp.G):
            m.addConstr(Vars["OUT_"+s] - Vars["IN_"+s] == 0)

    #C5
    m.addConstr(Vars["OUT_"+ssp.s0] - Vars["IN_"+ssp.s0] == 1)

    #C6
    r_side = 0
    for s in ssp.G:
        r_side += Vars["IN_"+s]	
    m.addConstr(r_side == 1)

    if verbose:
        print('================== lp ssp ===============')

    policy = {}

    m.optimize()

    # for c in m.getConstrs():
    #     print(c.value)

    for v in m.getVars():

        if verbose:
            print('{0:8} = {1:5.3f}'.format(v.varName, v.x))
        # print('%s %g' % (v.varName, v.x))

        if v.varName in s_a:
            if v.x > 0:
                policy[s_a[v.varName][0]] = s_a[v.varName][1]
    if verbose:
        print('Obj: %g' % m.objVal)

    R = {}

    R['policy'] = policy
    R['problem'] = m

    return R



def lp_ssp_e_GRB(ssp, factor = 1, verbose = 0, max_time = float('inf')):

    sign = lambda x: (1, -1)[x < 0]
    #declare variables

    m = Model('LP - RS SSP')

    t0 = time.clock()

    Vars = {}

    s_a = {}

    for s in ssp.S:
        
        if s not in ssp._G:
            
            var_name = None
            #in vars

            var_name = "IN_"+s
            Vars[var_name] = m.addVar(vtype=GRB.CONTINUOUS, name = var_name)

            #out vars
            var_name = "OUT_"+s
            Vars[var_name] = m.addVar(vtype=GRB.CONTINUOUS, name = var_name)

            #occupation measure vars
            for a in ssp.App(s):
                
                var_name = s + a
                Vars[var_name] = m.addVar(vtype=GRB.CONTINUOUS, name = var_name)
                s_a[var_name] = [s,a]


    #Set objective
    r_side = 0
    for s in ssp.S:
        if s not in ssp._G:
            for a in ssp.App(s):
                var_name = s + a
                r_side += Vars[var_name]*exp(factor*ssp.C(s,a))*ssp.P(s,a,ssp._G[0])*sign(factor)

            #r_side += Vars[var_name]*exp(factor*ssp.C(s,a))
    m.setObjective(r_side, GRB.MINIMIZE)
    #Add Constraints
    

    # m.setParam(GRB.Param.MIPGapAbs,GRB.INFINITY)

    #C1 - Done
    for var in Vars:
        m.addConstr(Vars[var] >= 0)

    

    #C2 - modified 
    for s in ssp.S:
        
        r_side = 0
        flag = False
        for s1 in ssp.S:
            if s1 not in ssp.G:
                for a in ssp.App(s1):
                    if ssp.P(s1,a,s):
                        #add in var
                        flag = True
                        r_side +=  Vars[s1+a]*ssp.P(s1, a, s)*exp(factor*ssp.C(s1,a))

        if flag:

            if not s in ssp._G:
                m.addConstr(Vars['IN_'+s] == r_side)


    #C3
    for s in ssp.S:
        if not s in ssp.G:
            r_side = 0
            flag = False
            for a in ssp.App(s):
                flag = True
                r_side += Vars[s+a]
            if flag:
                m.addConstr(Vars["OUT_"+s] == r_side)

    #C4
    for s in ssp.S:
        if not (s==ssp.s0 or s in ssp.G):
            m.addConstr(Vars["OUT_"+s] - Vars["IN_"+s] == 1)

    #C5

    m.addConstr(Vars["OUT_"+ssp.s0] - Vars["IN_"+ssp.s0] == 1)

    #C6
    # r_side = None
    # gl = -sign(factor)
    # for s in ssp.G:

    # 	r_side += Vars["IN_"+s]	
    # problem += r_side == 1

    modeling_time = time.clock() - t0


    # print("=============================")
    # print("         LP SSP_E            ")
    # print("=============================")

    policy = {}

    time_solver = 0

    
    try:
            
        t0 = time.clock()
        m.optimize()
        time_solver = time.clock()-t0

        for v in m.getVars():
	
            if verbose:
                print('{0:8} = {1:5.3f}'.format(v.varName, v.x))
            # print('%s %g' % (v.varName, v.x))

            if v.varName in s_a:
                if v.x > 0:
                    policy[s_a[v.varName][0]] = s_a[v.varName][1]

    except Exception as e:

        if verbose:
            print('Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e)))
        
        time_solver = -1

        
    #print("Objective =", value(problem.objective))

    # if problem.status==-1:
    #     time_solver = -1

    R = {'problem': m, 'policy': policy,
            'time_modeling': modeling_time, 'time': time_solver}

    return R