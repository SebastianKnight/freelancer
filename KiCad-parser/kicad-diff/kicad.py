import re

class Component(object):
	tag = 'comp'
	def __init__(self, ref=None, value=None):
		self.ref = ref
		self.value = value
		self.raw = None

	def deserialize(self, string):
		self.raw = string
		self.ref = re.findall(r'ref "(.*?)"', string)[0]
		self.value = re.findall(r'value "(.*?)"', string)[0]

	def __eq__(self, component):
		return self.ref == component.ref and self.value == component.value
	def __ne__(self, component):
		return not(self.__eq__(component))

	def __str__(self):
		return 'ref({}), value({})'.format( self.ref, self.value )

class Node(object):
	tag = 'node'
	def __init__(self, ref=None, pin=None):
		self.ref = ref
		self.pin = pin
		self.raw = None

	def deserialize(self, string):
		self.raw = string
		self.ref = re.findall(r'ref (.*?)\)', string)[0]
		self.pin = re.findall(r'pin (.*?)$', string)[0]

	def __eq__(self, node):
		return self.ref == node.ref and self.pin == node.pin

	def __ne__(self, node):
		return not(self.__eq__(node))

	def __str__(self):
		return 'ref({}), pin({})'.format( self.ref, self.pin )

class Net(object):
	tag = 'net'
	def __init__(self, code=None, name=None):
		self.code = code
		self.name = name
		self.raw = None
		self.nodes = []

	def deserialize(self, string):
		self.raw = string
		#Set nets props
		self.code = re.findall(r'\(code (.*?)\)', string)[0]
		self.name = re.findall(r'name "(.*?)"', string)[0]

		# Fill notes
		nodes = re.findall(r'\(({0} (.*?))\)\)'.format(Node.tag), self.raw)
		for nodeStr in nodes:
			node = Node()
			node.deserialize(nodeStr[0])
			self.nodes.append(node)

	def __eq__(self, net):
		if self.name == net.name and self.code == net.code:
			return True
		else:
			return False

	def __ne__(self, node):
		return not (self.__eq__(node))

	def __str__(self):
		return 'ref({}), name({})'.format( self.code, self.name )

class Project(object):

	def __init__(self, filePath):
		self.path = filePath
		self.raw = None

		self.components = []
		self.nets = []

		self._deserialize()

	def _deserialize(self):
		"""File elements in "" should not have speces! """
		with open(self.path) as file:
			# Create more general solution
			self.raw = file.read()
			raw = self.raw.replace('\n','')

		# Fill components
		comps = re.findall(r'\(({0} (.*?))\)\)'.format(Component.tag), raw)
		for compStr in comps:
			comp = Component()
			comp.deserialize(compStr[0])
			self.components.append(comp)

		# Fill nets
		nets = re.findall(r'\(({0} (.*?)\)\))\)'.format(Net.tag), raw)
		for netStr in nets:
			net = Net()
			net.deserialize(netStr[0])
			self.nets.append(net)

	def diffReport(self, project):
		Project._diff('componenst', self.components, project.components)
		Project._diff('nets', self.nets, project.nets)

	@staticmethod
	def _diff(name, firstList, secondList):
		# Check missing components
		missingList = []
		matchedComp = []
		for selfComp in firstList:
			missing = True
			for comp in secondList:
				if selfComp == comp:
					missing = False
					matchedComp.append(comp)
					# Because unique comps is here break
					break

			if missing:
				missingList.append(selfComp)

		# Check overflown components
		overflownList = []
		for comp in secondList:
			missing = True
			for matchComp in matchedComp:
				if matchComp == comp:
					missing = False
			if missing:
				overflownList.append(comp)

		if missingList != []:
			print('\nMissing {}: {}'.format(name, len(missingList)))
			for comp in missingList:
				print(' - {}'.format(comp))

		if overflownList != []:
			print('\nOverflown {}: {}'.format(name, len(overflownList)))
			for comp in overflownList:
				print(' + {}'.format(comp))



