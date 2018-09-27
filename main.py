from ssp import *
from vi import *
from lpSolver import *
from genProblem import *

from lpSolverG import *


def expTir():
	# TireWorld Domain
	print('#{0:10} {1:10} {2:10} {3:10} {4:10} {5:10} {5:10} {6:10}'.format('instante','states','time1','f1','time2','f2','time3','f3'))

	for tam in range(2,22,2):
		R = genTire(tam)
		ssp = R['ssp']
		s_states = len(ssp._S)
		instance = str(tam)
		
		R1 = search_lambda2(ssp)

		factor = 0.1
		error = 0.001
		R2 = riskAdverse(ssp, error + 0.000001, error, factor, initPolicy(ssp))

		R3 = riskAdverse2(ssp, error + 0.000001, error, factor, initPolicy(ssp))

		print('{0:3} {1:5} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f} {6:10.3f} {7:10.3f}'.format(instance,s_states,R1['time'],R1['factor'],R2['time'],R2['factor'],R3['time'],R3['factor']))


# Navigation Domain
def expNav():
	
	print('#{0:10} {1:10} {2:10} {3:10} {4:10} {5:10} {6:10} {7:10}'.format('instante','states','time1','f1','time2','f2','time2','f2'))

	x = 4
	for j in range(6,22,2):
		y = j

		ssp = genNav2(x,y)
		s_states = len(ssp._S)
		instance = str(x) +" X "+str(y)
		# print(s_states)
		
		# print(R1['time'],R1['factor'])
		R1 = search_lambda2(ssp)
		factor = -0.1
		error = 0.001
		R2 = riskAdverse(ssp, error + 0.000001, error, factor, initPolicy(ssp))
		R3 = riskAdverse2(ssp, error + 0.000001, error, factor, initPolicy(ssp))
		print('{0:3} {1:5} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f} {6:10.3f} {7:10.3f}'.format(instance,s_states,R1['time'],R1['factor'],R2['time'],R2['factor'],R3['time'],R3['factor']))


# River Domain
def expRiv():
	
	print('#{0:10} {1:10} {2:10} {3:10} {4:10} {5:10} {6:10} {7:10}'.format('instante','states','time1','f1','time2','f2','time2','f2'))

	x = 5
	for j in range(6,22,2):
		y = j
		ssp = genRiv2(x,y)

		s_states = len(ssp._S)
		instance = str(x) +" X "+str(j)
		
		# print(s_states)
		R1 = search_lambda2(ssp)
		factor = -0.1
		error = 0.001
		R2 = riskAdverse(ssp, error + 0.000001, error, factor, initPolicy(ssp))
		R3 = riskAdverse2(ssp, error + 0.000001, error, factor, initPolicy(ssp))
		print('{0:3} {1:5} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f} {6:10.3f} {7:10.3f}'.format(instance,s_states,R1['time'],R1['factor'],R2['time'],R2['factor'],R3['time'],R3['factor']))


def test():

	tam = 1
	R = genTire(tam)
	ssp = R['ssp']

	md = R['metadata'] 
	am = R['actMap']

	error = 0.00001
	beta  = error + 0.00000001
	factor = 0.1
	R = riskAdverse(ssp, beta, error, factor, initPolicy(ssp))
	print(ssp.name,' ', R['factor'])

	R1 = search_lambda2(ssp)
	print('SEARCH LAMBDA', R1['factor'])

	#0.6 0.7 0.8
	R = lp_ssp_e(ssp, 0.7)
	plotTire(ssp, tam, "example-tire", R['policy'], md, am);

test()