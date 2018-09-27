from ssp import *
import os


def prNav(i,x):

	maxP = 0.8
	minP = 0.2	
	step = (maxP-minP)/(x-1)

	return minP + i*step


def st(i,j):
	return str(i)+"_"+str(j)


def genDr():


	A=[0,1,2,3,4]

	S=[]

	for i in range(11):
		S.append(str(i))

	S.append("PASS")
	S.append("INIT")

	ssp = SSP()


	for state in S:
		ssp.S.append(state)

	ssp._s0 = "INIT"
	ssp.G.append("PASS")

	for a in A:
		ssp.A.append(str(a))

	detAct = "detAct"
	ssp.A.append(detAct)
	for s in range(11):

		state = "INIT"
		state1 = str(s)
		ssp.P(state,detAct,state1,1)
		ssp.C(state,detAct,0)
		ssp.App(state, detAct)

	
	for s in range(11):
		for a in A:
			action = str(a)
			for state1 in S:

				state = str(s)
				p=0
				if state1=="PASS":
					p = (0.08*float(s))+(0.04*float(a))
					ssp.P(state, action, state1, p) 
					ssp.C(state, action, 2+a)
					ssp.App(state, action)
				else:
					if state1 == str(min(s+a,10)):

						p = 1 - (0.08*float(s))+(0.04*float(a))
						ssp.P(state, action, state1, p) 
						ssp.C(state, action, 2+a)
						ssp.App(state, action)
				
				

	return ssp
		
def genNav2(x,y):
	A = ['U','D','R','L','abs']

	ssp = SSP()


	for j in range(y):
		for i in range(x):
			state = st(i,j)
			ssp.S.append(state)

	# ssp.S.append("DE")

	ssp._s0 = st(0,0)
	ssp.G.append(st(0,y-1))

	#add actions:
	for a in A:
		ssp.A.append(a)



	# goal abs state
	state = st(0,y-1)
		
	# action absorbing action
	
	ssp.P(state, A[4], state, 1) 
	ssp.C(state, A[4], 0)
	ssp.App(state, A[4])

	#[TOP] - define probability transiction function
	j = y-1
	for i in range(1,x):
		state = st(i,j)
		
		#action UP 	  NORTH
		if j < y-1:
			state1 = st(i,j+1)
			ssp.P(state, A[0], state1, 1) 
			ssp.C(state, A[0], 1)
			ssp.App(state, A[0])

		#action DOWN  SOUTH
		if j > 0:
			state1 = st(i,j-1)
			ssp.P(state, A[1], state1, 1)
			ssp.C(state, A[1], 1)
			ssp.App(state, A[1])

		#action RIGHT EAST
		if i < x-1:
			state1 = st(i+1,j)
			ssp.P(state, A[2], state1, 1)
			ssp.C(state, A[2], 1)
			ssp.App(state, A[2])

		#action LEFT  WEST
		if i > 0:
			state1 = st(i-1,j)
			ssp.P(state, A[3], state1, 1)
			ssp.C(state, A[3], 1)
			ssp.App(state, A[3])


	#[BOT] - define probability transiction function
	j = 0
	for i in range(x):
		state = st(i,j)

		#action UP 	  NORTH
		if j < y-1:
			state1 = st(i,j+1)
			ssp.P(state, A[0], state1, 1) 
			ssp.C(state, A[0], 1)
			ssp.App(state, A[0])

		#action DOWN  SOUTH
		if j > 0:
			state1 = st(i,j-1)
			ssp.P(state, A[1], state1, 1)
			ssp.C(state, A[1], 1)
			ssp.App(state, A[1])

		#action RIGHT EAST
		if i < x-1:
			state1 = st(i+1,j)
			ssp.P(state, A[2], state1, 1)
			ssp.C(state, A[2], 1)
			ssp.App(state, A[2])

		#action LEFT  WEST
		if i > 0:
			state1 = st(i-1,j)
			ssp.P(state, A[3], state1, 1)
			ssp.C(state, A[3], 1)
			ssp.App(state, A[3])

	#[MID] - define probability transiction function
	for j in range(1,y-1):
		for i in range(x):

			state = st(i,j)
			stateDE = st(0,0)

			#action UP 	  NORTH
			if j < y-1:
				state1 = st(i,j+1)
				ssp.P(state, A[0], state1, prNav(i,x)) 
				ssp.P(state, A[0], stateDE, 1-prNav(i,x)) 

				ssp.C(state, A[0], 1)
				ssp.App(state, A[0])

			#action DOWN  SOUTH
			if j > 0:
				state1 = st(i,j-1)
				ssp.P(state, A[1], state1, prNav(i,x)) 
				ssp.P(state, A[1], stateDE,1- prNav(i,x)) 
				ssp.C(state, A[1], 1)
				ssp.App(state, A[1])

			#action RIGHT EAST
			if i < x-1:
				state1 = st(i+1,j)
				ssp.P(state, A[2], state1, prNav(i,x)) 
				ssp.P(state, A[2], stateDE, 1-prNav(i,x)) 
				ssp.C(state, A[2], 1)
				ssp.App(state, A[2])

			#action LEFT  WEST
			if i > 0:
				state1 = st(i-1,j)
				ssp.P(state, A[3], state1, prNav(i,x)) 
				ssp.P(state, A[3], stateDE, 1-prNav(i,x)) 
				ssp.C(state, A[3], 1)
				ssp.App(state, A[3])




	return ssp


def genNav(x,y):

	A = ['U','D','R','L','abs']

	ssp = SSP()


	for j in range(y):
		for i in range(x):
			state = st(i,j)
			ssp.S.append(state)

	ssp.S.append("DE")

	ssp._s0 = st(0,0)
	ssp.G.append(st(0,y-1))

	#add actions:
	for a in A:
		ssp.A.append(a)



	#goal abs state
	#state = st(0,y-1)
		
	#action absorbing action
	
	#ssp.P(state, A[4], state, 1) 
	#ssp.C(state, A[4], 1)
	#ssp.App(state, A[4])

	#[TOP] - define probability transiction function
	j = y-1
	for i in range(1,x):
		state = st(i,j)
		
		#action UP 	  NORTH
		if j < y-1:
			state1 = st(i,j+1)
			ssp.P(state, A[0], state1, 1) 
			ssp.C(state, A[0], 1)
			ssp.App(state, A[0])

		#action DOWN  SOUTH
		if j > 0:
			state1 = st(i,j-1)
			ssp.P(state, A[1], state1, 1)
			ssp.C(state, A[1], 1)
			ssp.App(state, A[1])

		#action RIGHT EAST
		if i < x-1:
			state1 = st(i+1,j)
			ssp.P(state, A[2], state1, 1)
			ssp.C(state, A[2], 1)
			ssp.App(state, A[2])

		#action LEFT  WEST
		if i > 0:
			state1 = st(i-1,j)
			ssp.P(state, A[3], state1, 1)
			ssp.C(state, A[3], 1)
			ssp.App(state, A[3])


	#[BOT] - define probability transiction function
	j = 0
	for i in range(x):
		state = st(i,j)

		#action UP 	  NORTH
		if j < y-1:
			state1 = st(i,j+1)
			ssp.P(state, A[0], state1, 1) 
			ssp.C(state, A[0], 1)
			ssp.App(state, A[0])

		#action DOWN  SOUTH
		if j > 0:
			state1 = st(i,j-1)
			ssp.P(state, A[1], state1, 1)
			ssp.C(state, A[1], 1)
			ssp.App(state, A[1])

		#action RIGHT EAST
		if i < x-1:
			state1 = st(i+1,j)
			ssp.P(state, A[2], state1, 1)
			ssp.C(state, A[2], 1)
			ssp.App(state, A[2])

		#action LEFT  WEST
		if i > 0:
			state1 = st(i-1,j)
			ssp.P(state, A[3], state1, 1)
			ssp.C(state, A[3], 1)
			ssp.App(state, A[3])

	#[MID] - define probability transiction function
	for j in range(1,y-1):
		for i in range(x):

			state = st(i,j)
			stateDE = "DE"

			#action UP 	  NORTH
			if j < y-1:
				state1 = st(i,j+1)
				ssp.P(state, A[0], state1, prNav(i,x)) 
				ssp.P(state, A[0], stateDE, 1-prNav(i,x)) 

				ssp.C(state, A[0], 1)
				ssp.App(state, A[0])

			#action DOWN  SOUTH
			if j > 0:
				state1 = st(i,j-1)
				ssp.P(state, A[1], state1, prNav(i,x)) 
				ssp.P(state, A[1], stateDE,1- prNav(i,x)) 
				ssp.C(state, A[1], 1)
				ssp.App(state, A[1])

			#action RIGHT EAST
			if i < x-1:
				state1 = st(i+1,j)
				ssp.P(state, A[2], state1, prNav(i,x)) 
				ssp.P(state, A[2], stateDE, 1-prNav(i,x)) 
				ssp.C(state, A[2], 1)
				ssp.App(state, A[2])

			#action LEFT  WEST
			if i > 0:
				state1 = st(i-1,j)
				ssp.P(state, A[3], state1, prNav(i,x)) 
				ssp.P(state, A[3], stateDE, 1-prNav(i,x)) 
				ssp.C(state, A[3], 1)
				ssp.App(state, A[3])




	return ssp






def plotNav(ssp, x, y, filename, policy = {}):


	#print(policy)

	symbol = {} 
	symbol['L'] = "&#x2190;"
	symbol['U'] = "&#x2191;"
	symbol['R'] = "&#x2192;"
	symbol['D'] = "&#x2193;"
	symbol['water'] = ""
	symbol['goal'] = "&#x2690;"
	symbol['abs'] = "&#x21ba;"


	with open(filename+".dot", 'w') as out:

		var = "digraph {"
		out.write(var+'\n')

		var = "\tnode [shape=plaintext]"
		out.write(var+'\n')

		var = "\ta[label=<<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\">"
		out.write(var+'\n')

		for j in range(y):

			var = "\t<TR>"
			out.write(var+'\n')

			for i in range(x):

				s_a = str(i)+"_"+str(y-j-1)
				
				if s_a in policy:
					

					color = " BGCOLOR=\"darkslategray1\""

					if i==0 and j==y-1:
						color = " BGCOLOR=\"deepskyblue\""

					sign = symbol[policy[s_a]]
					var = "\t\t<TD width=\"35\" height=\"35\" fixedsize=\"true\""+color+">"+sign+"</TD>"
				else:

					color = " BGCOLOR=\"gray\""
					sign = symbol['water']

					if j == 0 and i == 0:
						color = " BGCOLOR=\"chartreuse2\""
						sign = symbol['goal']

					var = "\t\t<TD width=\"35\" height=\"35\" fixedsize=\"true\""+color+">"+sign+"</TD>"

				out.write(var+'\n')

			var = "\t</TR>"
			out.write(var+'\n')

		var = "\t</TABLE>>];"
		out.write(var+'\n')
		var = "}"
		out.write(var+'\n')
		out.close()

		os.system("convert "+ filename+".dot " + filename+".png")



def genRiv2(x,y):
	
	A = ['U','D','R','L']

	ssp = SSP()

	for j in range(y):
		for i in range(x):
			state = str(i)+"_"+str(j)
			ssp.S.append(state)


		

	#ssp.S.append("DE")

	ssp._s0 = str(0)+"_"+str(0)
	ssp.G.append(str(x-1)+"_"+str(0))

	#add actions
	for a in A:
		ssp.A.append(a)

	ssp.A.append('abs')

	#[1] - define probability transiction function
	for j in range(1,y):
		for i in range(x):
	
			state = str(i)+"_"+str(j)
			if i==0 or i==x-1 or j==y-1:

				#action UP 	  NORTH
				if j < y-1:
					state1 = str(i)+"_"+str(j+1)
					ssp.P(state, A[0], state1, 0.9) 
					ssp.P(state, A[0], state, 0.1) 
					ssp.C(state, A[0], 1)
					ssp.App(state, A[0])

				#action DOWN  SOUTH
				if j > 0:
					state1 = str(i)+"_"+str(j-1)
					ssp.P(state, A[1], state1, 0.9)
					ssp.P(state, A[1], state, 0.1)
					ssp.C(state, A[1], 1)
					ssp.App(state, A[1])

				#action RIGHT EAST
				if i < x-1:
					state1 = str(i+1)+"_"+str(j)
					ssp.P(state, A[2], state1, 0.9)
					ssp.P(state, A[2], state, 0.1)
					ssp.C(state, A[2], 1)
					ssp.App(state, A[2])

				#action LEFT  WEST
				if i > 0:
					state1 = str(i-1)+"_"+str(j)
					ssp.P(state, A[3], state1, 0.9)
					ssp.P(state, A[3], state, 0.1)
					ssp.C(state, A[3], 1)
					ssp.App(state, A[3])


	state = str(0)+"_"+str(0)


	#action UP 	  NORTH

	state1 = str(0)+"_"+str(1)
	ssp.P(state, A[0], state1, 0.9) 
	ssp.P(state, A[0], state, 0.1) 
	ssp.C(state, A[0], 1)
	ssp.App(state, A[0])

	#action RIGHT EAST
	#state1 = "DE"
	#ssp.P(state, A[2], state1, 1)
	#ssp.C(state, A[2], 1)
	#ssp.App(state, A[2])



	rangeP = []
	maxP = 0.8
	minP = 0.2
	step = (maxP-minP)/(x-3)

	for i in range(x-2):
		rangeP.append(0.2)
	# print("HEREEEEEEEEEEEEEEE=============")
	# print(rangeP)


	for j in range(2,y-1):
		for i in range(1,x-1):

			state = str(i)+"_"+str(j)

			#action UP 	  NORTH
			if j < y-1:
				state1 = str(i)+"_"+str(j+1)
				state2 = str(i)+"_"+str(j-1)
				ssp.P(state, A[0], state1, 1-rangeP[i-1]) 
				ssp.P(state, A[0], state2, rangeP[i-1]) 

				ssp.C(state, A[0], 1)
				ssp.App(state, A[0])

			#action DOWN  SOUTH
			if j > 0:
				state1 = str(i)+"_"+str(j-1)
				ssp.P(state, A[1], state1, 1)
				
				ssp.C(state, A[1], 1)
				ssp.App(state, A[1])

			#action RIGHT EAST
			if i < x-1:
				state1 = str(i+1)+"_"+str(j)
				state2 = str(i)+"_"+str(j-1)
				ssp.P(state, A[2], state1, 1-rangeP[i-1])
				ssp.P(state, A[2], state2, rangeP[i-1]) 

				ssp.C(state, A[2], 1)
				ssp.App(state, A[2])

			#action LEFT  WEST
			if i > 0:
				state1 = str(i-1)+"_"+str(j)
				state2 = str(i)+"_"+str(j-1)
				ssp.P(state, A[3], state1, 1-rangeP[i-1])
				ssp.P(state, A[3], state2, rangeP[i-1]) 

				ssp.C(state, A[3], 1)
				ssp.App(state, A[3])

	for i in range(1,x-1):
		j = 1
		state = str(i)+"_"+str(j)

		#action UP 	  NORTH
		if j < y-1:
			state1 = str(i)+"_"+str(j+1)
			state2 = str(i)+"_"+str(j-1)
			ssp.P(state, A[0], state1, 1-rangeP[i-1]) 
			ssp.P(state, A[0], state2, rangeP[i-1]) 

			ssp.C(state, A[0], 1)
			ssp.App(state, A[0])

		#action DOWN  SOUTH
		if j > 0:
			#state1 = "DE"
			state1 = str(i)+"_"+str(j-1)

			ssp.P(state, A[1], state1, 1)
			
			ssp.C(state, A[1], 1)
			ssp.App(state, A[1])

		#action RIGHT EAST
		if i < x-1:
			state1 = str(i+1)+"_"+str(j)
			state2 = str(i)+"_"+str(j-1)
			ssp.P(state, A[2], state1, 1-rangeP[i-1])
			ssp.P(state, A[2], state2, rangeP[i-1]) 

			ssp.C(state, A[2], 1)
			ssp.App(state, A[2])

		#action LEFT  WEST
		if i > 0:
			state1 = str(i-1)+"_"+str(j)
			state2 = str(i)+"_"+str(j-1)
			ssp.P(state, A[3], state1, 1-rangeP[i-1])
			ssp.P(state, A[3], state2, rangeP[i-1]) 

			ssp.C(state, A[3], 1)
			ssp.App(state, A[3])

	stateGoal = str(x-1)+"_"+str(0)

	ssp.P(stateGoal,'abs',stateGoal,1)
	ssp.C(stateGoal,'abs',0)
	ssp.App(stateGoal,'abs')


	for i in range(1,x-1):
		state = str(i)+"_"+str(0)
		init = str(i-1)+"_"+str(0)
		#ssp.P(state, A[0], init, 1)
		#ssp.P(state, A[1], init, 1)
		#ssp.P(state, A[2], init, 1)
		ssp.P(state, A[3], init, 1)

		#ssp.C(state, A[0], 1)
		#ssp.C(state, A[1], 1)
		#ssp.C(state, A[2], 1)
		ssp.C(state, A[3], 1)

		#ssp.App(state, A[0])
		#ssp.App(state, A[1])
		#ssp.App(state, A[2])
		ssp.App(state, A[3])


	return ssp




def genRiv(x,y):


	A = ['U','D','R','L']

	ssp = SSP()

	for j in range(y):
		for i in range(x):
			state = str(i)+"_"+str(j)
			ssp.S.append(state)


		

	#ssp.S.append("DE")

	ssp._s0 = str(0)+"_"+str(0)
	ssp.G.append(str(x-1)+"_"+str(0))

	#add actions
	for a in A:
		ssp.A.append(a)

	ssp.A.append('abs')

	#[1] - define probability transiction function
	for j in range(1,y):
		for i in range(x):

			state = str(i)+"_"+str(j)


			#action UP 	  NORTH
			if j < y-1:
				state1 = str(i)+"_"+str(j+1)
				ssp.P(state, A[0], state1, 1) 
				ssp.C(state, A[0], 1)
				ssp.App(state, A[0])

			#action DOWN  SOUTH
			if j > 0:
				state1 = str(i)+"_"+str(j-1)
				ssp.P(state, A[1], state1, 1)
				ssp.C(state, A[1], 1)
				ssp.App(state, A[1])

			#action RIGHT EAST
			if i < x-1:
				state1 = str(i+1)+"_"+str(j)
				ssp.P(state, A[2], state1, 1)
				ssp.C(state, A[2], 1)
				ssp.App(state, A[2])

			#action LEFT  WEST
			if i > 0:
				state1 = str(i-1)+"_"+str(j)
				ssp.P(state, A[3], state1, 1)
				ssp.C(state, A[3], 1)
				ssp.App(state, A[3])


	state = str(0)+"_"+str(0)


	#action UP 	  NORTH

	state1 = str(0)+"_"+str(1)
	ssp.P(state, A[0], state1, 1) 
	ssp.C(state, A[0], 1)
	ssp.App(state, A[0])

	#action RIGHT EAST
	#state1 = "DE"
	#ssp.P(state, A[2], state1, 1)
	#ssp.C(state, A[2], 1)
	#ssp.App(state, A[2])



	rangeP = []
	maxP = 0.8
	minP = 0.2
	step = (maxP-minP)/(x-3)

	for i in range(x-2):
		rangeP.append(minP+i*step)
	# print("HEREEEEEEEEEEEEEEE=============")
	# print(rangeP)


	for j in range(2,y-1):
		for i in range(1,x-1):

			state = str(i)+"_"+str(j)

			#action UP 	  NORTH
			if j < y-1:
				state1 = str(i)+"_"+str(j+1)
				state2 = str(i)+"_"+str(j-1)
				ssp.P(state, A[0], state1, 1-rangeP[i-1]) 
				ssp.P(state, A[0], state2, rangeP[i-1]) 

				ssp.C(state, A[0], 1)
				ssp.App(state, A[0])

			#action DOWN  SOUTH
			if j > 0:
				state1 = str(i)+"_"+str(j-1)
				ssp.P(state, A[1], state1, 1)
				
				ssp.C(state, A[1], 1)
				ssp.App(state, A[1])

			#action RIGHT EAST
			if i < x-1:
				state1 = str(i+1)+"_"+str(j)
				state2 = str(i)+"_"+str(j-1)
				ssp.P(state, A[2], state1, 1-rangeP[i-1])
				ssp.P(state, A[2], state2, rangeP[i-1]) 

				ssp.C(state, A[2], 1)
				ssp.App(state, A[2])

			#action LEFT  WEST
			if i > 0:
				state1 = str(i-1)+"_"+str(j)
				state2 = str(i)+"_"+str(j-1)
				ssp.P(state, A[3], state1, 1-rangeP[i-1])
				ssp.P(state, A[3], state2, rangeP[i-1]) 

				ssp.C(state, A[3], 1)
				ssp.App(state, A[3])

	for i in range(1,x-1):
		j = 1
		state = str(i)+"_"+str(j)

		#action UP 	  NORTH
		if j < y-1:
			state1 = str(i)+"_"+str(j+1)
			state2 = str(i)+"_"+str(j-1)
			ssp.P(state, A[0], state1, 1-rangeP[i-1]) 
			ssp.P(state, A[0], state2, rangeP[i-1]) 

			ssp.C(state, A[0], 1)
			ssp.App(state, A[0])

		#action DOWN  SOUTH
		if j > 0:
			#state1 = "DE"
			state1 = str(i)+"_"+str(j-1)

			ssp.P(state, A[1], state1, 1)
			
			ssp.C(state, A[1], 1)
			ssp.App(state, A[1])

		#action RIGHT EAST
		if i < x-1:
			state1 = str(i+1)+"_"+str(j)
			state2 = str(i)+"_"+str(j-1)
			ssp.P(state, A[2], state1, 1-rangeP[i-1])
			ssp.P(state, A[2], state2, rangeP[i-1]) 

			ssp.C(state, A[2], 1)
			ssp.App(state, A[2])

		#action LEFT  WEST
		if i > 0:
			state1 = str(i-1)+"_"+str(j)
			state2 = str(i)+"_"+str(j-1)
			ssp.P(state, A[3], state1, 1-rangeP[i-1])
			ssp.P(state, A[3], state2, rangeP[i-1]) 

			ssp.C(state, A[3], 1)
			ssp.App(state, A[3])

	stateGoal = str(x-1)+"_"+str(0)

	ssp.P(stateGoal,'abs',stateGoal,1)
	ssp.C(stateGoal,'abs',0)
	ssp.App(stateGoal,'abs')


	for i in range(1,x-1):
		state = str(i)+"_"+str(0)
		init = str(i-1)+"_"+str(0)
		#ssp.P(state, A[0], init, 1)
		#ssp.P(state, A[1], init, 1)
		#ssp.P(state, A[2], init, 1)
		ssp.P(state, A[3], init, 1)

		#ssp.C(state, A[0], 1)
		#ssp.C(state, A[1], 1)
		#ssp.C(state, A[2], 1)
		ssp.C(state, A[3], 1)

		#ssp.App(state, A[0])
		#ssp.App(state, A[1])
		#ssp.App(state, A[2])
		ssp.App(state, A[3])


	return ssp



def plotRiv(ssp, x, y, filename, policy = {}):


	#print(policy)

	symbol = {} 
	symbol['L'] = "&#8592;"
	symbol['U'] = "&#8593;"
	symbol['R'] = "&#8594;"
	symbol['D'] = "&#8595;"
	symbol['water'] = "&#x2248;"
	symbol['goal'] = "&#71;"
	symbol['None'] = "&#10540;"
	symbol['abs'] = "&#x21ba;"


	with open(filename+".dot", 'w') as out:

		var = "digraph {"
		out.write(var+'\n')

		var = "\tnode [shape=plaintext]"
		out.write(var+'\n')

		var = "\ta[label=<<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\">"
		out.write(var+'\n')

		for j in range(y):

			var = "\t<TR>"
			out.write(var+'\n')

			for i in range(x):

				s_a = str(i)+"_"+str(y-j-1)
				
				if s_a in policy:
					
					color = " BGCOLOR=\"darkgoldenrod1\""
					sign = symbol[policy[s_a]]
					var = "\t\t<TD width=\"35\" height=\"35\" fixedsize=\"true\""+color+">"+sign+"</TD>"
				else:



					color = " BGCOLOR=\"dodgerblue\""
					sign = symbol['water']

					if j == y-1 and i == x-1:
						color = " BGCOLOR=\"chartreuse3\""
						sign = symbol['goal']

					var = "\t\t<TD width=\"35\" height=\"35\" fixedsize=\"true\""+color+">"+sign+"</TD>"

				out.write(var+'\n')

			var = "\t</TR>"
			out.write(var+'\n')

		var = "\t</TABLE>>];"
		out.write(var+'\n')
		var = "}"
		out.write(var+'\n')
		out.close()

		os.system("convert "+ filename+".dot " + filename+".png")



def st2(i,j):
	return str(i) + ',' + str(j)


def genTire(tam):

	# def genTireworld(tam):
		
	# 	tam = tam+1

	# 	for j in range(1,tam,1):
	# 		for i in range(1,tam,1):
	# 			print(j,i)
	# 		tam = tam-1
			
	# 	print("---------------")
	# 	#creating routes
	# 	sa = 1
	# 	sb = 1

	# 	def create_routes(sa,sb):
			
	# 		tama = sa+3
	# 		tamb = sb+3
	# 		for j in range(sa,tama,1):
	# 			for i in range(sb,tamb,1):
	# 				#action D
	# 				if j%2==1:
	# 					print(j,i," D ", j,i+1)

					
	# 			tama = tama-1
	# 			tamb = tamb-1

	# 	create_routes(sa,sb)
	ssp = SSP()
	ssp.name = 'tireworld['+str(tam)+']'

	group = {}



	def genBase(x,y):
		baseTam = 3
		tmp = []

		# gen base states
		for j in range(y, y+3, 1):
			for i in range(x, x+baseTam, 1):
				# print('({0},{1}) '.format(i,j),end='')
				tmp.append(st2(i,j))
			# print('\n')
			baseTam -= 1

		# add group to each state
		for i in range(len(tmp)):
			group[tmp[i]] = i

		return tmp

	# print(group)
	
	def getInitStates(tam):

		seedX = []
		seedY = []

		tam = tam+1
		tam2 = tam

		for j in range(1,tam):
			for i in range(1,tam2):
				# print('({0},{1}) '.format(i*2-1,j*2-1), end='')
				seedX.append(i*2-1)
				seedY.append(j*2-1)
			# print('\n')
			tam2 -= 1

		return [seedX,seedY]

	p1 = {}

	



	[X,Y] = getInitStates(tam)

	# for i in range(len(X)):
	# 	print('{0},{1}'.format(X[i],Y[i]))

	# gen all states:
	tmpS = []

	for i in range(len(X)):
		tmpS = genBase(X[i],Y[i])

		for s in tmpS:
			if s not in ssp._S:
				ssp._S.append(s)

	# print(ssp._S)
	# gen all connections	 

	# print('STATES:', ssp._S)

	A = ['R','D','L','abs']

	for a in A:
		ssp._A.append(a)

	s0 = st2(1,1)
	# print("tam", tam)
	tam = (tam*2)+2
	tam2 = tam

	prtn = 0.5
	prst = 0.8

	for j in range(1,tam):
		for i in range(1,tam2):
			# print('({0},{1}) '.format(i,j),end='')
			s = st2(i,j)

			if group[st2(i,j)] == 0:
				
				if i==1 and j!=1:

					p1[s] = 'unsafe'
					# right ->
					s1 = st2(i+1,j)
					a = A[0]
					ssp.P(s,a,s1,1-prtn)
					ssp.P(s,a,s0,prtn)
					ssp.C(s,a,1)
					ssp.App(s,a)
					# down v
					s1 = st2(i,j+1)
					a = A[1]
					ssp.P(s,a,s1,1-prtn)
					ssp.P(s,a,s0,prtn)
					ssp.C(s,a,1)
					ssp.App(s,a)
					# left |/
					s1 = st2(i-1,j+1)
					a = A[2]

					

					if s1 in ssp._S:
						
						ssp.P(s,a,s1,1)
						ssp.C(s,a,1)
						ssp.App(s,a)
				else :
					if j == 1:
						p1[s] = 'safe'
						# right ->
						s1 = st2(i+1,j)
						a = A[0]
						ssp.P(s,a,s1,prst)
						ssp.P(s,a,s1,1-prst)
						ssp.C(s,a,1)
						ssp.App(s,a)
						# down v
						s1 = st2(i,j+1)
						a = A[1]
						ssp.P(s,a,s1,prst)
						ssp.P(s,a,s1,1-prst)
						ssp.C(s,a,1)
						ssp.App(s,a)
						# left |/
						s1 = st2(i-1,j+1)
						if s1 in ssp._S:
							a = A[2]
							ssp.P(s,a,s1,prst)
							ssp.P(s,a,s1,1-prst)
							ssp.C(s,a,1)
							ssp.App(s,a)
					else:
						p1[s] = 'unsafe'
						# right ->
						# down v
						# left |/
						s1 = st2(i-1,j+1)
						if s1 in ssp._S:
							a = A[2]
							ssp.P(s,a,s1,1-prtn)
							ssp.P(s,a,s0,prtn)
							ssp.C(s,a,1)
							ssp.App(s,a)


			if group[st2(i,j)] == 1:
				
				p1[s] = 'safe'
				# right >

				s1 = st2(i+1,j)
				a = A[0]
				ssp.P(s,a,s1,prst)
				ssp.P(s,a,s1,1-prst)
				ssp.C(s, a, 1)
				ssp.App(s, a)

				# down \/
				# s1 = st2(i,j+1)

				# left |/
				s1 = st2(i-1,j+1)
				a = A[2]
				ssp.P(s,a,s1,prst)
				ssp.P(s,a,s1,1-prst)
				ssp.C(s, a, 1)
				ssp.App(s, a)

			if group[st2(i,j)] == 2:

				p1[s] = 'safe'
				# print('STATE :',  st2(i,j))
				# right >
				s1 = st2(i+1,j)
				a = A[0]
				
				if s1 in ssp._S:
					ssp.P(s,a,s1,prst)
					ssp.P(s,a,s1,1-prst)
					ssp.C(s, a, 1)
					ssp.App(s, a)


				# down \/
				s1 = st2(i,j+1)
				a = A[1]
				if s1 in ssp._S:
					ssp.P(s,a,s1,prst)
					ssp.P(s,a,s1,1-prst)
					ssp.C(s, a, 1)
					ssp.App(s, a)

				# left |/
				s1 = st2(i-1,j+1)
				a = A[2]
				ssp.P(s,a,s1,prst)
				ssp.P(s,a,s1,1-prst)
				ssp.C(s, a, 1)
				ssp.App(s, a)



			if group[st2(i,j)] == 3:

				p1[s] = 'unsafe'
				# right >
				s1 = st2(i,j)
				a = A[0]
				ssp.P(s, a, s1, 1-prtn)
				ssp.P(s, a, s0, prtn)
				ssp.C(s, a, 1)
				ssp.App(s, a)
				# down \/
				s1 = st2(i,j+1)
				a = A[1]
				ssp.P(s, a, s1, 1-prtn)
				ssp.P(s, a, s0, prtn)
				ssp.C(s, a, 1)
				ssp.App(s, a)
				# left |/
				# s1 = st2(i-1,j+1)
				# a = A[2]
				# if s1 in ssp._S:
				# 	ssp.P(s, a, s1, 1)
				# 	ssp.C(s, a, 1)
				# 	ssp.App(s, a)

			if group[st2(i,j)] == 4:

				p1[s] = 'safe'
				# right >
				# s1 = st2(i,j)
				# down \/
				# s1 = st2(i,j+1)
				# left |/
				s1 = st2(i-1,j+1)
				a = A[2]
				ssp.P(s,a,s1,prst)
				ssp.P(s,a,s1,1-prst)
				# ssp.P(s, a, s0, prtn)
				ssp.C(s, a, 1)
				ssp.App(s, a)

			if group[st2(i,j)] == 5:
				p1[s] = 'unsafe'
				
				# right >
				s1 = st2(i+1,j)
				a = A[0]
				if s1 in ssp._S:
					if i==1:
						p1[s] = 'unsafe'
						ssp.P(s, a, s1, 1-prtn)
						ssp.P(s, a, s0, prtn)
						ssp.C(s, a, 1)
						ssp.App(s, a)
					else:
						p1[s] = 'safe'
						ssp.P(s,a,s1,prst)
						ssp.P(s,a,s1,1-prst)
						ssp.C(s, a, 1)
						ssp.App(s, a)
				# down \/
				s1 = st2(i,j+1)
				a = A[1]
				if s1 in ssp._S:
					if i==1:
						p1[s] = 'unsafe'
						ssp.P(s, a, s1, 1-prtn)
						ssp.P(s, a, s0, prtn)
						ssp.C(s, a, 1)
						ssp.App(s, a)
					else:
						p1[s] = 'safe'
						ssp.P(s,a,s1,prst)
						ssp.P(s,a,s1,1-prst)
						ssp.C(s, a, 1)
						ssp.App(s, a)
				# left |/
				s1 = st2(i-1,j+1)
				a = A[2]
				if s1 in ssp._S:
					if i==1:
						p1[s] = 'unsafe'
						ssp.P(s, a, s1, 1-prtn)
						ssp.P(s, a, s0, prtn)
						ssp.C(s, a, 1)
						ssp.App(s, a)
					else:
						p1[s] = 'safe'
						ssp.P(s,a,s1,prtn)
						ssp.P(s,a,s1,1-prtn)
						ssp.C(s, a, 1)
						ssp.App(s, a)
		tam2 -= 1
		# print('')

	sg = st2(1,tam-1)
	ssp._G.append(sg)
	ssp.P(sg,'abs', sg, 1)
	ssp.C(sg,'abs', 0)
	ssp.App(sg,'abs')

	ssp._s0 = st2(1,1)
	

	R = {}
	R['ssp'] = ssp
	R['metadata'] = p1

	# print('METADATA', p1)

	actMap = {}

	# print("tam", tam)
	tam2 = tam
	for j in range(1,tam):
		for i in range(1,tam2):
			s = st2(i,j)
			if s in ssp._S:
				for a in ssp.App(s):
					x = (i-1)*2
					y = (j-1)*2
					if a == 'R':
						actMap[st2(x+1,y)] = 'R'
					if a == 'D':
						actMap[st2(x,y+1)] = 'D'
					if a == 'L':
						actMap[st2(x-1,y+1)] = 'L'


		tam2 -= 1

	R['actMap'] = actMap
	
	return R

# ssp = genTire(2)

# print(ssp)
# group = {}


def plotTire(ssp, tam, filename, policy = {}, metadata = {}, actMap = {}):

	symbol = {} 
	symbol['L'] = "&#11113;"
	# symbol['U'] = "&#x2191;"
	symbol['R'] = "&#11106;"
	symbol['D'] = " &#11107;"
	# symbol['water'] = ""
	# symbol['goal'] = "&#x2690;"
	symbol['abs'] = "&#x21ba;"
	symbol['place'] = "&#x2609;"
	symbol['void'] = ""
	symbol['safe'] = ""
	symbol['unsafe'] = ""


	p1 = {}

	tam = tam*2+2
	# print("TAM REAL", tam)
	for j in range(1,tam):
		for i in range(1,tam):
			if st2(i,j) in ssp._S :
				i1 = (i-1)*2
				j1 = (j-1)*2
				p1[st2(i1,j1)] = metadata[st2(i,j)]

			if st2(i,j) in policy:
				i1 = (i-1)*2
				j1 = (j-1)*2

				if policy[st2(i,j)] == 'R':
					p1[st2(i1+1,j1)] = 'R'
				if policy[st2(i,j)] == 'D':
					p1[st2(i1,j1+1)] = 'D'
				if policy[st2(i,j)] == 'L':
					p1[st2(i1-1,j1+1)] = 'L'




	tam = (tam-1)*2
	# print("TAM FULL", tam)

	counter = 0

	with open(filename+".dot", 'w') as out:

		var = "digraph {"
		out.write(var+'\n')

		var = "\tnode [shape=plaintext, fontsize=16, fontname=arial ]"
		out.write(var+'\n')

		var = "\ta[label=<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\" COLOR=\"#ffffff\">"
		out.write(var+'\n')
		cellsize = 30

		for j in range(tam-1):

			var = "\t<TR>"
			out.write(var+'\n')

			for i in range(tam-1):
				
				if st2(i,j) in p1:
					if p1[st2(i,j)] == 'safe':
						color = " BGCOLOR=\"#D1F2EB\""
						sign = symbol[p1[st2(i,j)]]
						sign = str(counter)
						colorSymbol = "<FONT COLOR=\"gray\">"
						if ssp._s0 == st2(i+1,j+1):
							sign = '&#128660;'
							colorSymbol = "<FONT COLOR=\"black\">"
						var = "\t\t<TD width=\""+str(cellsize)+"\" height=\""+str(cellsize)+"\" fixedsize=\"true\""+color+">"+colorSymbol+sign+"</FONT></TD>"
						counter +=1
					elif p1[st2(i,j)] == 'unsafe':
						color = " BGCOLOR=\"#FADBD8\""
						sign = symbol[p1[st2(i,j)]]
						sign = str(counter)
						colorSymbol = "<FONT COLOR=\"gray\">"
						if i == 0 and j == tam-2:
							sign = '&#9873;'
							colorSymbol = "<FONT COLOR=\"black\">"
						var = "\t\t<TD width=\""+str(cellsize)+"\" height=\""+str(cellsize)+"\" fixedsize=\"true\""+color+">"+colorSymbol+sign+"</FONT></TD>"
						counter +=1
					else:
						color = " BGCOLOR=\"white\""
						sign = symbol[p1[st2(i,j)]]
						var = "\t\t<TD width=\""+str(cellsize)+"\" height=\""+str(cellsize)+"\" fixedsize=\"true\""+color+">"+sign+"</TD>"
				else:
					if st2(i,j) in actMap:
						color = " BGCOLOR=\"white\""
						sign = symbol[actMap[st2(i,j)]]
						colorSymbol = "<FONT COLOR=\"gray\">"
						var = "\t\t<TD width=\""+str(cellsize)+"\" height=\""+str(cellsize)+"\" fixedsize=\"true\""+color+">"+colorSymbol+sign+"</FONT></TD>"
					else:
						color = " BGCOLOR=\"white\""
						sign = symbol['void']
						
						var = "\t\t<TD width=\""+str(cellsize)+"\" height=\""+str(cellsize)+"\" fixedsize=\"true\""+color+">"+sign+"</TD>"

				out.write(var+'\n')
			var = "\t</TR>"
			out.write(var+'\n')

		var = "\t</TABLE>>];"
		out.write(var+'\n')
		var = "}"
		out.write(var+'\n')
		out.close()

		os.system("convert "+ filename+".dot " + filename+".png")
