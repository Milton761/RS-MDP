from ssp import *
from pulp import *
from math import *
import time
import pulp


from numpy import linalg as LA
import numpy as np
from vi import *


def printValues(problem):
	#print variables values of one problem
	print("=============values==============")
	for v in problem.variables():
			print(v.name, "=", v.varValue)

def printPolicy(policy):
	#print policy
	print("=============policy==============")
	for key, v in policy.items():
		print(key, " ", v)
 

def lp_ssp(ssp):

	#declare variables

	Vars = {}
	s_a = {}

	for s in ssp.S:
		
		var_name = None
		#in vars

		var_name = "IN_"+s
		Vars[var_name] = LpVariable(var_name,0)

		#out vars
		var_name = "OUT_"+s
		Vars[var_name] = LpVariable(var_name,0)

		#occupation measure vars
		for a in ssp.App(s):
			var_name = s + a
			Vars[var_name] = LpVariable(var_name,0)
			s_a[var_name] = [s,a]



	problem = SSP = LpProblem("LP - SSP", LpMinimize)

	#Set objective
	r_side = None
	for s in ssp.S:
		for a in ssp.App(s):
			var_name = s + a
			r_side += Vars[var_name]*ssp.C(s,a)
	problem += r_side

	#Add Constraints

	#C1 - Done

	#C2
	for s in ssp.S:
		r_side = None
		for s1 in ssp.S:
			for a in ssp.App(s1):
				if ssp.P(s1,a,s) > 0:
					#add in var
					r_side += Vars[s1+a]*ssp.P(s1, a, s) 

		if r_side != None:
			problem += Vars["IN_"+s] == r_side


	#C3
	for s in ssp.S:
		if not s in ssp.G:
			r_side = None
			for a in ssp.App(s):
				r_side += Vars[s+a]
			if r_side != None:

				#print("[C3]: OUT_"+s, "=", str(r_side))
				problem += Vars["OUT_"+s] == r_side

	#C4
	for s in ssp.S:
		if not (s==ssp.s0 or s in ssp.G):
			problem += Vars["OUT_"+s] - Vars["IN_"+s] == 0

	#C5

	problem += Vars["OUT_"+ssp.s0] - Vars["IN_"+ssp.s0] == 1

	#C6
	r_side = None
	for s in ssp.G:

		r_side += Vars["IN_"+s]	
	problem += r_side == 1


	print("=============================")
	print("           LP SSP            ")
	print("=============================")

	policy = {}

	GUROBI().solve(problem)

	for v in problem.variables():
		#print(v.name, "=", v.varValue)
		if v.name in s_a:
			if v.varValue > 0:
				policy[s_a[v.name][0]] = s_a[v.name][1]

	    
	print("Objective =", value(problem.objective))

	R = {}

	R['policy'] = policy
	R['problem'] = problem

	return R



def lp_ssp_D(ssp, discount=0.001):
	#declare variables

	Vars = {}
	s_a = {}

	for s in ssp.S:
		
		var_name = None
		#in vars

		var_name = "IN_"+s
		Vars[var_name] = LpVariable(var_name,0)

		#out vars
		var_name = "OUT_"+s
		Vars[var_name] = LpVariable(var_name,0)

		#occupation measure vars
		for a in ssp.App(s):
			var_name = s + a
			Vars[var_name] = LpVariable(var_name,0)
			s_a[var_name] = [s,a]



	problem = SSP = LpProblem("LP - SSP", LpMinimize)

	#Set objective
	r_side = None
	for s in ssp.S:
		for a in ssp.App(s):
			var_name = s + a
			r_side += Vars[var_name]*ssp.C(s,a)
	problem += r_side

	#Add Constraints

	#C1 - Done

	#C2
	for s in ssp.S:
		r_side = None
		for s1 in ssp.S:
			for a in ssp.App(s1):
				if ssp.P(s1,a,s) > 0:
					#add in var
					r_side += Vars[s1+a]*ssp.P(s1, a, s)*discount

		if r_side != None:
			problem += Vars["IN_"+s] == r_side


	#C3
	for s in ssp.S:
		if not s in ssp.G:
			r_side = None
			for a in ssp.App(s):
				r_side += Vars[s+a]
			if r_side != None:

				#print("[C3]: OUT_"+s, "=", str(r_side))
				problem += Vars["OUT_"+s] == r_side

	#C4
	for s in ssp.S:
		if not (s==ssp.s0 or s in ssp.G):
			problem += Vars["OUT_"+s] - Vars["IN_"+s] == 0

	#C5

	problem += Vars["OUT_"+ssp.s0] - Vars["IN_"+ssp.s0] == 1

	#C6
	r_side = None
	for s in ssp.G:

		r_side += Vars["IN_"+s]	
	problem += r_side == 1


	print("=============================")
	print("           LP SSP            ")
	print("=============================")

	policy = {}

	GUROBI().solve(problem)

	for v in problem.variables():
		#print(v.name, "=", v.varValue)
		if v.name in s_a:
			if v.varValue > 0:
				policy[s_a[v.name][0]] = s_a[v.name][1]

	    
	print("Objective =", value(problem.objective))

	

	return [problem, policy]


def search_lambda2(ssp, init = 0.000001, verbose=0):
	
	flag = True

	#search upper bound
	f = init

	top = 0
	bot = 0

	while flag:
		
		f = f*2
		R = lp_ssp_e(ssp, f)

		if verbose:
			print(f)

		if R['time']>0:
			bot = f
		else:
			top = f
			flag = False
	
	R = search_lambda(ssp, bot, top , verbose)
	return R		
		

def search_lambda(ssp, factor = 0.000001, top = 1, verbose = 0):
	
	flag = True

	previus_factor = factor



	bot = factor
	

	if verbose :
		print('bot: {0:.5f}, top: {1:.5f}'.format(bot, top))
	R = {}
	t1 = time.clock()
	while (top - bot) > 0.00000001:
		

		f = (top + bot)/2
		# print('{0:.5f}'.format(f))
		if verbose:
			print('bot: {0:.5f}, top: {1:.5f}'.format(bot, top))

		R = lp_ssp_e(ssp, f)

		if R['time'] > 0:
			bot = f
		else:
			top = f 

	total_time = time.clock()-t1
	problem = R['problem']
	# printValues(R['problem'])
	n_vars = len(problem.variables())


	R = {}
	R['factor'] = bot
	R['time'] = total_time
	R['n_variables'] = n_vars
	R['problem'] = problem
	

	return R
	
def lp_ssp_e(ssp, factor = 1, verbose = 0, max_time = float('inf')):

	sign = lambda x: (1, -1)[x < 0]
	#declare variables

	t0 = time.clock()

	Vars = {}

	s_a = {}

	for s in ssp.S:
		
		if s not in ssp._G:
			
			var_name = None
			#in vars

			var_name = "IN_"+s
			Vars[var_name] = LpVariable(var_name,0)

			#out vars
			var_name = "OUT_"+s
			Vars[var_name] = LpVariable(var_name,0)

			#occupation measure vars
			for a in ssp.App(s):
				
				var_name = s + a
				Vars[var_name] = LpVariable(var_name,0)
				s_a[var_name] = [s,a]



	problem = SSP = LpProblem("LP - SSP exponential ", LpMinimize)

	#Set objective
	r_side = 0
	for s in ssp.S:
		if s not in ssp._G:
			for a in ssp.App(s):
				var_name = s + a
				r_side += Vars[var_name]*exp(factor*ssp.C(s,a))*ssp.P(s,a,ssp._G[0])*sign(factor)

			#r_side += Vars[var_name]*exp(factor*ssp.C(s,a))
	problem += r_side
	#Add Constraints

	#C1 - Done

	#C2 - modified 
	for s in ssp.S:
		
		r_side = None
		for s1 in ssp.S:
			if s1 not in ssp.G:
				for a in ssp.App(s1):
					if ssp.P(s1,a,s):
						#add in var
						r_side +=  Vars[s1+a]*ssp.P(s1, a, s)*exp(factor*ssp.C(s1,a))

		if r_side != None:

			if not s in ssp._G:
				problem += Vars["IN_"+s] == r_side


	#C3
	for s in ssp.S:
		if not s in ssp.G:
			r_side = None
			for a in ssp.App(s):
				r_side += Vars[s+a]
			if r_side != None:
				#print("[C3]: OUT_"+s, "=", str(r_side))
				problem += Vars["OUT_"+s] == r_side

	#C4
	for s in ssp.S:
		if not (s==ssp.s0 or s in ssp.G):
			problem += Vars["OUT_"+s] - Vars["IN_"+s] == 1

	#C5

	problem += Vars["OUT_"+ssp.s0] - Vars["IN_"+ssp.s0] == 1

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

	# gurobiSolver = GUROBI(msg = verbose,timeLimit=max_time)
	# gurobiSolver.solve(problem)
	gurobiSolver = GUROBI(msg = verbose,timeLimit=max_time)
	try:
		
		t0 = time.clock()
		gurobiSolver.actualSolve(problem)
		time_solver = time.clock()-t0

		for v in problem.variables():
			if v.name in s_a:
				if v.varValue > 0:
					policy[s_a[v.name][0]] = s_a[v.name][1]

	except Exception as e:

		if verbose:
			print('Error! Code: {c}, Message, {m}'.format(c = type(e).__name__, m = str(e)))
		
		time_solver = -1

	    
	#print("Objective =", value(problem.objective))

	if problem.status==-1:
		time_solver = -1

	R = {'problem': problem, 'policy': policy,
            'time_modeling': modeling_time, 'time': time_solver}

	return R


def lp_ssp_e_l(ssp, factor = 1, verbose = 0, max_time = float('inf')):

	sign = lambda x: (1, -1)[x < 0]
	#declare variables

	t0 = time.clock()

	Vars = {}

	s_a = {}

	for s in ssp.S:
		
		if s not in ssp._G:
			
			var_name = None
			#in vars

			var_name = "IN_"+s
			Vars[var_name] = LpVariable(var_name,0)

			#out vars
			var_name = "OUT_"+s
			Vars[var_name] = LpVariable(var_name,0)

			#occupation measure vars
			for a in ssp.App(s):
				
				var_name = s + a
				Vars[var_name] = LpVariable(var_name,0)
				s_a[var_name] = [s,a]



	problem = SSP = LpProblem("LP - SSP exponential ", LpMinimize)
	Vars['lambda'] = LpVariable('lambda',0)


	#Set objective
	r_side = 0
	for s in ssp.S:
		if s not in ssp._G:
			for a in ssp.App(s):
				var_name = s + a
				r_side += Vars[var_name]*exp(Vars['lambda']*ssp.C(s,a))*ssp.P(s,a,ssp._G[0])*sign(Vars['lambda'])

			#r_side += Vars[var_name]*exp(factor*ssp.C(s,a))
	problem += r_side
	#problem += Vars['lambda']
	#Add Constraints

	#C1 - Done

	#C2 - modified 
	for s in ssp.S:
		
		r_side = None
		for s1 in ssp.S:
			if s1 not in ssp.G:
				for a in ssp.App(s1):
					if ssp.P(s1,a,s):
						r_side +=  Vars[s1+a]*ssp.P(s1, a, s)*exp(Vars['lambda'])
						#add in var*ssp.C(s1,a))

		if r_side != None:
			if not s in ssp._G:
				problem += Vars["IN_"+s] == r_side


	#C3
	for s in ssp.S:
		if not s in ssp.G:
			r_side = None
			for a in ssp.App(s):
				r_side += Vars[s+a]
			if r_side != None:
				#print("[C3]: OUT_"+s, "=", str(r_side))
				problem += Vars["OUT_"+s] == r_side

	#C4
	for s in ssp.S:
		if not (s==ssp.s0 or s in ssp.G):
			problem += Vars["OUT_"+s] - Vars["IN_"+s] == 0

	#C5

	problem += Vars["OUT_"+ssp.s0] - Vars["IN_"+ssp.s0] == 1

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
		gurobiSolver = GUROBI(msg = verbose,timeLimit=max_time)
		t0 = time.clock()
		gurobiSolver.solve(problem)
		time_solver = time.clock()-t0

		for v in problem.variables():
			if v.name in s_a:
				if v.varValue > 0:
					policy[s_a[v.name][0]] = s_a[v.name][1]

	except Exception:
		time_solver = -1

	    
	#print("Objective =", value(problem.objective))

	R = {'problem': problem, 'policy': policy,
            'time_modeling': modeling_time, 'time': time_solver}

	return R


def lp_sspude_e(ssp, factor = 1, penalty=1000):
	#declare variables

	Vars = {}
	s_a = {}

	for s in ssp.S:
		
		var_name = None
		#in vars

		var_name = "IN_"+s
		Vars[var_name] = LpVariable(var_name,0)

		#out vars
		var_name = "OUT_"+s
		Vars[var_name] = LpVariable(var_name,0)

		#occupation measure vars
		for a in ssp.App(s):
			var_name = s + a
			Vars[var_name] = LpVariable(var_name,0)
			s_a[var_name] = [s,a]



	print("=============================")
	print("====LP - SSPUDE =============")
	print("=============================")

	d = penalty

	problem = SSP = LpProblem("SSPUDE - LP", LpMinimize)

	#LP formulation with Dead Ends#

	#dead ends vars
	for s in ssp.S:
		var_name = "DE_"+s
		Vars[var_name] = LpVariable(var_name,0)


	#set objective

	r_side = None
	for s in ssp.S:
		for a in ssp.App(s):
			var_name = s + a
			#r_side += Vars[var_name]*ssp.C(s,a)
			r_side += Vars[var_name]*exp(factor*ssp.C(s,a))*ssp.P(s,a,ssp._G[0])

	for s in ssp.S:
		r_side += Vars["DE_"+s]*d

	problem += r_side 


	#Add constraints

	#C1 - Done in declaration

	#C2
	for s in ssp.S:
		r_side = None
		for s1 in ssp.S:
			for a in ssp.App(s1):
				if ssp.P(s1,a,s) > 0:
					#add in var
					#r_side += Vars[s1+a]*ssp.P(s1, a, s) 
					r_side +=  Vars[s1+a]*ssp.P(s1, a, s)*exp(factor*ssp.C(s1,a))

		if r_side != None:
			problem += Vars["IN_"+s] == r_side

	#C3
	for s in ssp.S:
		if not (s==ssp.s0 or s in ssp.G):
			problem += Vars["OUT_"+s] - Vars["IN_"+s] == 0

	#C4
	problem += Vars["OUT_"+ssp.s0] - Vars["IN_"+ssp.s0] == 1

	#C7 - Done in declaration

	#C8

	for s in ssp.S:
		r_side = None
		if not (s in ssp.G):
			for a in ssp.App(s):
				r_side += Vars[s+a]
			r_side += Vars["DE_"+s]
			problem += Vars["OUT_"+s] == r_side


	#C9

	r_side = None
	for s in ssp.G:
		r_side += Vars["IN_"+s]

	for s in ssp.S:
		r_side += Vars["DE_"+s]

	problem += r_side == 1


	policy = {}

	GUROBI().solve(problem)

	for v in problem.variables():
		print(v.name, "=", v.varValue)
		if v.name in s_a:
			if v.varValue > 0:
				policy[s_a[v.name][0]] = s_a[v.name][1]

	    
	print("Objective =", value(problem.objective))

	print("=============policy==============")
	for key, v in policy.items():
		print(key, " ", v)


	return [problem, policy]


def lp_sspude_D(ssp, discount = 1, penalty=1000):

	#declare variables

	Vars = {}
	s_a = {}

	for s in ssp.S:
		
		var_name = None
		#in vars

		var_name = "IN_"+s
		Vars[var_name] = LpVariable(var_name,0)

		#out vars
		var_name = "OUT_"+s
		Vars[var_name] = LpVariable(var_name,0)

		#occupation measure vars
		for a in ssp.App(s):
			var_name = s + a
			Vars[var_name] = LpVariable(var_name,0)
			s_a[var_name] = [s,a]



	print("=============================")
	print("====LP - SSPUDE =============")
	print("=============================")

	d = penalty

	problem = SSP = LpProblem("SSPUDE - LP", LpMinimize)

	#LP formulation with Dead Ends#

	#dead ends vars
	for s in ssp.S:
		var_name = "DE_"+s
		Vars[var_name] = LpVariable(var_name,0)


	#set objective

	r_side = None
	for s in ssp.S:
		for a in ssp.App(s):
			var_name = s + a
			r_side += Vars[var_name]*ssp.C(s,a)

	for s in ssp.S:
		r_side += Vars["DE_"+s]*d

	problem += r_side 


	#Add constraints

	#C1 - Done in declaration

	#C2
	for s in ssp.S:
		r_side = None
		for s1 in ssp.S:
			for a in ssp.App(s1):
				if ssp.P(s1,a,s) > 0:
					#add in var
					r_side += Vars[s1+a]*ssp.P(s1, a, s)*discount

		if r_side != None:
			problem += Vars["IN_"+s] == r_side

	#C3
	for s in ssp.S:
		if not (s==ssp.s0 or s in ssp.G):
			problem += Vars["OUT_"+s] - Vars["IN_"+s] == 0

	#C4
	problem += Vars["OUT_"+ssp.s0] - Vars["IN_"+ssp.s0] == 1

	#C7 - Done in declaration

	#C8

	for s in ssp.S:
		r_side = None
		if not (s in ssp.G):
			for a in ssp.App(s):
				r_side += Vars[s+a]
			r_side += Vars["DE_"+s]
			problem += Vars["OUT_"+s] == r_side


	#C9

	r_side = None
	for s in ssp.G:
		r_side += Vars["IN_"+s]

	for s in ssp.S:
		r_side += Vars["DE_"+s]

	problem += r_side == 1


	policy = {}

	GUROBI().solve(problem)

	for v in problem.variables():
		print(v.name, "=", v.varValue)
		if v.name in s_a:
			if v.varValue > 0:
				policy[s_a[v.name][0]] = s_a[v.name][1]

	    
	print("Objective =", value(problem.objective))

	print("=============policy==============")
	for key, v in policy.items():
		print(key, " ", v)


	return [problem, policy]


def initPolicy(ssp):
    currentP = {}
    for s in ssp._S:
        currentP[s] = ssp.App(s)[0]

    return currentP





def riskAdverse(ssp, beta, error, factor, p0):

	R = {}
	link = {}
	linkT = {}

	for i in range(len(ssp._S)):
		link[i] = ssp._S[i]
		linkT[ssp._S[i]] = i

	T = []

	tamM = len(ssp._S)

	for i in range(tamM):
		T.append([])
		for j in range(tamM):
			T[i].append(0)

	for j in range(tamM):
		for i in range(tamM):
			state1 = link[i]
			state2 = link[j]
			if state2 == ssp._G[0]:
				T[i][j] = 0
			else:
				T[i][j] = ssp.P(state1, p0[state1], state2)

	D = []

	for i in range(tamM):
		D.append([])
		for j in range(tamM):
			D[i].append(0)

	for j in range(tamM):
		for i in range(tamM):
			if i == j:
				state1 = link[i]
				D[i][j] = exp(factor*ssp.C(state1, p0[state1]))

	# T1 = np.array(T)
	# D1 = np.array(D)

	def specR(ssp, factor, policy):

		for j in range(tamM):
			for i in range(tamM):
				state1 = link[i]
				state2 = link[j]

				if state2 == ssp._G[0]:
					T[i][j] = 0
				else:
					T[i][j] = ssp.P(state1, policy[state1], state2)

		for j in range(tamM):
			for i in range(tamM):
				if i == j:
					state1 = link[i]
					D[i][j] = exp(factor*ssp.C(state1, policy[state1]))
					# print('FACTOR ',factor)
					# print('STATE', state1)
					# print('POLICY', policy[state1])
					# print('COST' ,ssp.C(state1,policy[state1]))

		# print(D)
		T1 = np.array(T)
		D1 = np.array(D)
		M = D1.dot(T1)

		
		w, v = LA.eig(M)
		for i in range(len(w)):
			w[i] = abs(w[i])
		initSR = max(w)

		return initSR.real

	# print("INIT FACTOR ", factor)
	flag = True


	R = vi_e(ssp, factor, p0)
	#R = vi_e(ssp,factor,p0)
	p1 = R['policy']

	p1[ssp._G[0]] = 'abs'

	counter = 0

	t0 = time.clock()
	tp = 0

	while p0 != p1:
		tp = time.clock()-t0

		counter = counter + 1
		p0 = deepcopy(p1)
		# print("deepcopy")

		try:
			initSR = specR(ssp, factor, p1)
		except:
			break
		# print("before inner while")
		# print("INIT SR", initSR)
		while initSR < (1-beta):
			# counter +=1
			factor = factor + (np.log(1-error) - np.log(initSR))
			# print("factor",factor)
			initSR = specR(ssp, factor, p1)

		# 	print("afterINITSR")
		# print("exit inner while")

		# R = vi_e(ssp,factor,p0)
		try:
			R = lp_ssp_e(ssp, factor)
		except:
			break

		p1 = R['policy']
		p1[ssp._G[0]] = 'abs'
		# plotRiv(ssp, x, y, "expRiv2", p1)

	time2 = time.clock()-t0

	R['factor'] = factor
	R['policy'] = p1
	R['time'] = time2
	R['tlast'] = tp
	R['counter'] = counter
	return R


def riskAdverse2(ssp, beta, error, factor, p0):

	R = {}
	link = {}
	linkT = {}

	for i in range(len(ssp._S)):
		link[i] = ssp._S[i]
		linkT[ssp._S[i]] = i

	T = []

	tamM = len(ssp._S)

	for i in range(tamM):
		T.append([])
		for j in range(tamM):
			T[i].append(0)

	for j in range(tamM):
		for i in range(tamM):
			state1 = link[i]
			state2 = link[j]
			if state2 == ssp._G[0]:
				T[i][j] = 0
			else:
				T[i][j] = ssp.P(state1, p0[state1], state2)

	D = []

	for i in range(tamM):
		D.append([])
		for j in range(tamM):
			D[i].append(0)

	for j in range(tamM):
		for i in range(tamM):
			if i == j:
				state1 = link[i]
				D[i][j] = exp(factor*ssp.C(state1, p0[state1]))

	# T1 = np.array(T)
	# D1 = np.array(D)

	def specR(ssp, factor, policy):

		for j in range(tamM):
			for i in range(tamM):
				state1 = link[i]
				state2 = link[j]

				if state2 == ssp._G[0]:
					T[i][j] = 0
				else:
					T[i][j] = ssp.P(state1, policy[state1], state2)

		for j in range(tamM):
			for i in range(tamM):
				if i == j:
					state1 = link[i]
					D[i][j] = exp(factor*ssp.C(state1, policy[state1]))
					# print('FACTOR ',factor)
					# print('STATE', state1)
					# print('POLICY', policy[state1])
					# print('COST' ,ssp.C(state1,policy[state1]))

		# print(D)
		T1 = np.array(T)
		D1 = np.array(D)
		M = D1.dot(T1)

		
		w, v = LA.eig(M)
		for i in range(len(w)):
			w[i] = abs(w[i])
		initSR = max(w)

		return initSR.real

	# print("INIT FACTOR ", factor)
	flag = True


	R = vi_e(ssp, factor, p0)
	#R = vi_e(ssp,factor,p0)
	p1 = R['policy']

	p1[ssp._G[0]] = 'abs'

	counter = 0

	t0 = time.clock()
	tp = 0

	while p0 != p1:
		tp = time.clock()-t0

		counter = counter + 1
		p0 = deepcopy(p1)
		# print("deepcopy")

		try:
			initSR = specR(ssp, factor, p1)
		except:
			break
		# print("before inner while")
		# print("INIT SR", initSR)
		while initSR < (1-beta):
			# counter +=1
			factor = factor + (np.log(1-error) - np.log(initSR))
			# print("factor",factor)
			initSR = specR(ssp, factor, p1)

		# 	print("afterINITSR")
		# print("exit inner while")

		R = vi_e(ssp,factor,p0)
		# try:
		# 	R = lp_ssp_e(ssp, factor)
		# except:
		# 	break

		p1 = R['policy']
		p1[ssp._G[0]] = 'abs'
		# plotRiv(ssp, x, y, "expRiv2", p1)

	time2 = time.clock()-t0

	R['factor'] = factor
	R['policy'] = p1
	R['time'] = time2
	R['tlast'] = tp
	R['counter'] = counter
	return R
