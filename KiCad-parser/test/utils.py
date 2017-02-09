import os
class Resource(object):
	def getPath(*paths):
		return os.path.normpath(
			os.path.join(
				os.path.dirname(os.path.abspath(__file__)),
				'resources',
				*paths
			)
		)
