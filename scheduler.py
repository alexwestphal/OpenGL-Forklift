"""
The scheduler module for assignment2.

@author Alex Westphal 9819 6992
@version 12-Oct-2010
"""
import time

class Scheduler(object):

	def __init__(self):
		self.items = []
		self.speed = 1.0

	def add(self, func, length, startVal, endVal, complete=None):
		startTime = time.time()
		endTime = startTime + (length*self.speed)
		item = SchedulerItem(func,startTime,endTime,startVal,endVal,complete)
		self.items.append(item)

	def run(self):
		self.items = filter(lambda item: item.run(), self.items)

	def increaseSpeed(self):
		self.speed /= 2

	def decreaseSpeed(self):
		self.speed *= 2

	def clear(self):
		self.items = []

class SchedulerItem(object):
	
	def __init__(self, func, startTime, endTime, startVal, endVal, complete):
		self.func = func
		self.Ts = startTime
		self.Te = endTime
		self.Tt = endTime-startTime
		self.Vs = startVal
		self.Ve = endVal
		self.Vt = endVal-startVal
		self.complete = complete
	
	def run(self):
		Tn = time.time()
		
		if Tn < self.Ts:
			return true
		elif (self.Te - Tn) <= 0:
			self.func(self.Ve)
			if self.complete: self.complete()
			return False
		else:
			self.func(((Tn-self.Ts)/self.Tt)*self.Vt + self.Vs)
			return True

		
