from collections import defaultdict
import json
import random

class SSP:

	#SSP is a Tuple M = <S, s0, G, A, P, C>



	def __init__(self):

		self.name = 'ssp'
		self._S = []
		self._s0 = ""
		self._G = []
		self._A = []

		self._P = {}
		self._C = {}
		self._App = defaultdict(list)

		self.s_a_pr = defaultdict(list)
		self.s_a_st = defaultdict(list)

	def App(self, state, action = None):

		if action is None:
			return self._App[state]
		else:
			if action not in self._App[state]: 
				self._App[state].append(action)

	def P(self, s, action, s1, probability = None):

		if probability is None:
			return self._P.get((s,action,s1),0)
		else:
			self._P[s, action, s1] = round(probability,2)
			self.s_a_st[s,action].append(s1)
			self.s_a_pr[s,action].append(round(probability,2))
			

	def C(self, s, a, cost = None):
		if cost is None:
			return self._C.get((s,a),0)
		else:
			self._C[s,a] = cost



	@property
	def S(self):
		return self._S

	@property
	def s0(self):
		return self._s0

	@property
	def G(self):
		return self._G

	@property
	def A(self):
		return self._A

	def printFullSSP(self):

		print(len(self._App))

		for s in self._S:
			print("=======================================================")
			print("State : " + s)
			print("Acts  : " + str( self._App[s]))


			print("CPT   : ")
			for a in self._App[s]:
				for s1 in self._S:
					if self.P(s,a,s1)>0:
						print("\t"+str(s)+" - "+a+ " - " +str(s1)+" Pr: "+str(self.P(s,a,s1)) + " C:"+ str(self.C(s,a)) )

		
		for s_a in self.s_a_st:
			print('State-Action : {0}'.format(s_a))
			p = self.s_a_st[s_a]
			s = self.s_a_pr[s_a]
			print('\t{0}'.format(s))
			print('\t{0}'.format(p))
			print('-----------------------------')


	def __str__(self):


		limit = "==========================="
		varS = "Stat : " + str(self._S)
		actA = "Acts : " + str(self._A)
		init = "Init : " + self._s0
		goal = "Goal : " + str(self._G)

		return limit + "\n" + varS + "\n" + actA + "\n" + init + "\n" + goal + "\n" + limit
	

	def writeFile(self, filename):
		with open(filename, 'w') as out:

			out.write("#STATES\n")
			out.write(str(len(self._S)))
			out.write("\n#LIST-STATES\n")
			for s in self._S:
				out.write(s+" ")

			out.write("\n#ACTIONS\n")
			out.write(str(len(self._S)))
			out.write("\n#LIST-ACTIONS\n")
			for a in self._A:
				out.write(a+" ")

			out.write("\n#INIT STATE\n")
			out.write(self._s0)

			out.write("\n#GOAL STATES\n")
			out.write(str(len(self._G)))
			for g in self._G:
				out.write(g+" ")

			out.write("\n#PROBABILITY TRANSITION FUNCTION\n")
			out.write(str(len(self._P))+"\n")
			for key in self._P:
				out.write(key[0]+" "+key[1]+" "+key[2]+" "+str(self._P[key])+"\n")

			out.write("#COST FUNCTION\n")
			out.write(str(len(self._C))+"\n")
			for key in self._C:
				out.write(key[0]+" "+key[1]+" "+ str(self._C[key])+"\n")

			out.write("#APP FUNCTION\n")
			out.write(str(len(self._App))+"\n")
			for key in self._App:
				out.write(str(len(self._App[key]))+"\n")
				for elem in self._App[key]:
					out.write(key+" "+elem+"\n")
			
			#json.dump(self,"JSON.json")
		
	def loadFile(self, filename):
		

		return 0

	def writeJSON(self, filename):
		filename = open(filename,'w')
		filename.write(jsonpickle.encode(self))
		filename.close()



	def readJSON(self, filename):
		filename = open(filename,'r')
		obj = filename.read()
		newObj = jsonpickle.decode(obj)
		self._S =  newObj._S
		self._A =  newObj._A
		
		self._s0 = newObj._s0
		self._G = newObj._G

		
		self._App = newObj._App
		

		for key in newObj._C:
			self._C[eval(key)] = newObj._C[key]
			
		for key in newObj._P:
			self._P[eval(key)] = newObj._P[key]
			

		# for tuple in self._C:
		# 	print(type(tuple), tuple, self._C[tuple])
		

	def toDot(self, filename):
		with open(filename, 'w') as out:
			var = "digraph {"
			out.write(var+'\n')

			var = "node [ fontname = Helvetica fontsize = 10 shape=circle style=filled]"
			out.write('\t' + var + '\n')
			var = "edge [ fontname = Helvetica fontsize = 10 ]"
			out.write('\t' + var + '\n')



			for s in self._S:
				label 	  = "label = \""+s+"\""
				color     = ", color = \"#E0E0E0\""
				fillcolor = ", fillcolor = \"#E0E0E0\""
				var = s + "["+label+color+fillcolor+"]"
				out.write('\t' + var + '\n')



				for a in self.App(s):


					color     = " color = \"#E0E0E0\""
					shape     = ",shape = point"
					var       = s+a + " ["+color+shape+"]"
					out.write('\t' + var + '\n')


					
					color 	  = "color = \"#E0E0E0\""
					shape     = ", arrowhead = none"
					var 	  = s + " -> " + s+a + " ["+color+shape+"]"
					out.write('\t' + var + '\n')


					for s1 in self._S:

						if self.P(s,a,s1) > 0:
							#label = "label = <"+ str(self.P(s,a,s1)) +"<SUB>"+ a +"</SUB>>"



							label = "label = <X<SUB>"+ s+","+a +"</SUB>>"
							color = ",color = \"#E0E0E0\""
							var = s+a + " -> " + s1 + "["+label+color+"]"
							out.write('\t' + var + '\n')

			var = "}"
			out.write(var+'\n')

	def simulate(self, s, a):

		S = self.s_a_st[s,a]
		P = self.s_a_pr[s,a]

		R = random.choices(S,P,k=1)
		
		return R[0]

	def evalPolicy(self, policy = {}, samples = 1000):
		
		s0 = self._s0
		sg = self._G[0]

		current_state = s0
		cost = 0

		for i in range(samples):
			while current_state!= sg:


				next_state = self.simulate(current_state, policy[current_state])
				cost+= self.C(current_state, policy[current_state])
				current_state = next_state
			current_state = self._s0

		return cost/samples