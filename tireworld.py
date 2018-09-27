from ssp import *
import os


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

	ssp = SSP()
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
						ssp.P(s,a,s1,prst)
						ssp.P(s,a,s1,1-prst)
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
