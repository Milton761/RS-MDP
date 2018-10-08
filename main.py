from ssp import *
from vi import *
from lpSolver import *
from genProblem import *

from lpSolverG import *


def expTir():
	# TireWorld Domain
	print('#{0:10} {1:10} {2:10} {3:10} {4:10} {5:10} {5:10} {6:10}'.format('instante','states','time1','f1','time2','f2','time3','f3'))

	for tam in range(2,52,2):
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
		error = 0.000001
		R2 = riskAdverse(ssp, error + 0.00000001, error, factor, initPolicy(ssp))
		R3 = riskAdverse2(ssp, error + 0.00000001, error, factor, initPolicy(ssp))
		print('{0:3} {1:5} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f} {6:10.3f} {7:10.3f}'.format(instance,s_states,R1['time'],R1['factor'],R2['time'],R2['factor'],R3['time'],R3['factor']))


def test():

	tam = 2
	R = genTire(tam)
	ssp = R['ssp']
	# ssp.printFullSSP()

	md = R['metadata'] 
	am = R['actMap']

	R = lp_ssp(ssp)
	# plotTire(ssp, tam, "example-tire1", R['policy'], md, am);

	# error = 0.0001
	# beta  = error+0.00000001
	# factor = 0.1
	# R = riskAdverse(ssp, beta, error, factor, initPolicy(ssp))
	# print(ssp.name,' ', R['factor'])

	# R1 = search_lambda2(ssp)
	# print('SEARCH LAMBDA', R1['factor'])

	#0.6 0.7 0.8
	# R = lp_ssp_e(ssp,R['factor'])
	print(R['policy'])
	print('cost : ', ssp.evalPolicy(R['policy']))
	# plotTire(ssp, tam, "example-tire", R['policy'], md, am);
	

# test()
# expTir()

def expTir_random():

	def getError(real, x):
		return 100-getPrecision(real,x)

	def getPrecision(real, x):
		return (x*100)/real

	for i in range(1,11,1):

		tam = 10

		opt = {}
		opt['pr_return'] = getRandomPr(0.5, 0.99)
		opt['pr_execute'] = getRandomPr(0.1,0.99)
		
		R = genTire(tam, opt)
		ssp = R['ssp']
		theoricalLambda = log(1/(1-opt['pr_execute']))
		# print(theoricalLambda)

		factor = -0.1
		error = 0.0001

		R2 = riskAdverse(ssp, error + 0.000001, error, factor, initPolicy(ssp))

		e = getError(theoricalLambda, R2['factor'])
		print('Optimal: {0:5.3f} , Calculated: {1:5.3f} in {2:5.3f} secs, with {3:5.3f}% error'.format(theoricalLambda, R2['factor'], R2['time'], e))

expTir_random()

