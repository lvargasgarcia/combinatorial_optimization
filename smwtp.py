#from Snob2 import SnElement, SnFunction, ClausenFFT
import itertools

# convertir pi en numero, ej: (5,4,2,3,1) -> 54321
def to_int(pi):
	sum = pi[0]
	for i in range(1,len(pi)):
		sum = sum * 10 + pi[i] if pi[i] != 10 else sum * 100 + 10
	return sum

class SMWTP:
	# times = []
	# weights = []
	# due = []
	# globalMin = None
	# globalMax = None
	def __init__(self, file):
		
		self.times = []
		self.weights = []
		self.due = []
		self.globalMin = None
		self.globalMax = None
		
		with open(file) as f:
			lines = f.readlines()
			n = int(lines[0])
			for line in lines[1:]:
				elements = line.split()
				self.times.append(float(elements[0]))
				self.weights.append(float(elements[1]))
				self.due.append(float(elements[2]))
			if n != len(self.times):
				print("Warning: elements count does not match")

	def evaluate(self, permutation):
		t = 0
		fit = 0
		for i in range(len(self.times)):
			job = permutation[i]-1
			t = t + self.times[job]
			if t > self.due[job]:
				fit = fit + self.weights[job] * (t - self.due[job])

		return fit
	
	def delta(self, pi, h, position, k):

		different_components = [i for i in range(position-1, position+k-1)]
		result = 0
		common_tardiness = sum([self.times[pi[i]-1] for i in range(position-1)])
		t_pi = common_tardiness
		t_hpi = common_tardiness
		
		for i in different_components:
			
			job_pi, job_hpi = pi[i]-1, pi[h[i]-1]-1
			t_pi += self.times[job_pi]
			t_hpi += self.times[job_hpi]

			if t_pi > self.due[job_pi]:
				result -= self.weights[job_pi] * (t_pi - self.due[job_pi])
			
			if t_hpi > self.due[job_hpi]:
				result += self.weights[job_hpi] * (t_hpi - self.due[job_hpi])
		
		return result

	def getN(self):
		return len(self.times)


	def getFunction(self):
		n = len(self.times)
		dict = {}
		for permutation in itertools.permutations(range(1,n+1)):
			val = self.evaluate(permutation)
			dict[tuple(permutation)]=val
			if self.globalMin == None or val < self.globalMin:
				self.globalMin=val
			if self.globalMax == None or val > self.globalMax:
				self.globalMax=val

		return dict

