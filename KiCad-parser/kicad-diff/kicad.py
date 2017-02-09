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
		self.ref = re.findall(r'\(code (.*?)\)', string)[0]
		self.value = re.findall(r'name "(.*?)"', string)[0]

		# Fill notes
		nodes = re.findall(r'\(({0} (.*?))\)\)'.format(Node.tag), self.raw)
		for nodeStr in nodes:
			node = Node()
			node.deserialize(nodeStr[0])
			self.nodes.append(node)

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


