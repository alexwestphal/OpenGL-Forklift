"""
The animation module for assignment2.

@author Alex Westphal 9819 6992
@version 12-Oct-2010
"""
from collections import deque
from random import randint
from math import sin,cos,radians

class ForkliftAnimationTools(object):
	
	def __init__(self,scene,scheduler):
		self.scene = scene
		self.scheduler = scheduler
		self.in_progress = False
		self.queue = deque([])

	def _next_action(self):
		if len(self.queue) > 0:
			self.queue.popleft()()

	def activate_crates(self):
		for col in (self.scene.stack1.crates + self.scene.stack2.crates):
			for crate in col:
				if crate and crate.canRotate:
					rots = [crate.set_x_rot, crate.set_y_rot, crate.set_z_rot]
					self.scheduler.add(rots[randint(0,2)], 1000000, 0, 36000000)

	def reset(self):
		self.queue = deque([])
		self.scheduler.clear()
		self.scene.forklift.reset()
		self.scene.init_stacks()
		self.activate_crates()
		self.in_progress = False

	def move_x(self, time, dist, complete=None):
		def move_forklift(to):
			self.scene.forklift.location[0] = to
			
		cur = self.scene.forklift.location[0]
		self.scheduler.add(move_forklift,time,cur,cur+dist, complete)

	def move_z(self, time, dist, complete=None):
		def move_forklift(to):
			self.scene.forklift.location[2] = to
			
		cur = self.scene.forklift.location[2]
		self.scheduler.add(move_forklift,time,cur,cur+dist, complete)

	def rot(self, time, theta, complete=None):
		def rotate_forklift(angle):
			self.scene.forklift.angle = angle
			
		cur = self.scene.forklift.angle
		self.scheduler.add(rotate_forklift,time,cur,cur+theta, complete)

	def move_lift(self, time, level, complete=None):
		def move_forklift_riser(height):
			self.scene.forklift.lift_height = height
			
		cur = self.scene.forklift.lift_height
		self.scheduler.add(move_forklift_riser,time,cur,level, complete)

	def tilt_lift(self, time, angle, complete=None):
		def tilt_forklift_riser(ang):
			self.scene.forklift.lift_angle = ang
			
		cur = self.scene.forklift.lift_angle
		self.scheduler.add(tilt_forklift_riser,time,cur,angle, complete)

	def load_from_stack(self, stack, col, level):
		self.scene.forklift.set_payload(stack.remove(col,level))

	def place_on_stack(self, stack, col, level):
		stack.insert(self.scene.forklift.remove_payload(),col,level)

	def seq_finished(self):
		self.queue.append(self.reset)

	def seq_move_x(self, time, dist):
		self.queue.append(lambda: self.move_x(time,dist,self._next_action))

	def seq_move_z(self, time, dist):
		self.queue.append(lambda: self.move_z(time,dist,self._next_action))

	def seq_rot(self, time, theta):
		self.queue.append(lambda: self.rot(time,theta,self._next_action))

	def seq_move_lift(self, time, level):
		self.queue.append(lambda: self.move_lift(time,level,self._next_action))

	def seq_tilt_lift(self, time, angle):
		self.queue.append(lambda: self.tilt_lift(time,angle,self._next_action))

	def seq_set_head_lights(self, on):
		def activate():
			self.scene.forklift.set_head_lights(on)
			self._next_action()
		self.queue.append(activate)

	def seq_set_tail_lights(self, on):
		def activate():
			self.scene.forklift.set_tail_lights(on)
			self._next_action()
		self.queue.append(activate)

	def seq_set_left_indicator(self, on):
		def activate():
			self.scene.forklift.set_left_indicator(on)
			self._next_action()
		self.queue.append(activate)

	def seq_set_right_indicator(self, on):
		def activate():
			self.scene.forklift.set_right_indicator(on)
			self._next_action()
		self.queue.append(activate)

	def seq_load_from_stack(self, stack, col, level):
		def activate():
			self.load_from_stack(stack, col, level)
			self._next_action()
		self.queue.append(activate)

	def seq_place_on_stack(self, stack, col, level):
		def activate():
			self.place_on_stack(stack, col, level)
			self._next_action()
		self.queue.append(activate)

	def seq_wait(self, time):
		self.queue.append(lambda: self.scheduler.add(lambda: None,time,0,0))

	def seq_start(self):
		self._next_action()

class AnimationComponents(ForkliftAnimationTools):
	
	def fetch_x_p(self, stack, col, level, depth):
		self.seq_set_head_lights(True)
		self.seq_move_x(depth,depth)
		if level: self.seq_move_lift(level,level)
		self.seq_move_x(1,1)
		self.seq_load_from_stack(stack, col,level)
		self.seq_tilt_lift(1,5)
		self.seq_set_head_lights(False)
		self.seq_set_tail_lights(True)
		self.seq_move_x(2,-2)
		if level: self.seq_move_lift(level,0)
		self.seq_move_x(depth-1,1-depth)
		self.seq_set_tail_lights(False)

	def fetch_x_n(self, stack, col, level, depth):
		self.seq_set_head_lights(True)
		self.seq_move_x(depth,-depth)
		if level: self.seq_move_lift(level,level)
		self.seq_move_x(1,-1)
		self.seq_load_from_stack(stack, col,level)
		self.seq_tilt_lift(1,5)
		self.seq_set_head_lights(False)
		self.seq_set_tail_lights(True)
		self.seq_move_x(2,2)
		if level: self.seq_move_lift(level,0)
		self.seq_move_x(depth-1,depth-1)
		self.seq_set_tail_lights(False)

	def put_x_p(self, stack, col, level, depth):
		self.seq_set_head_lights(True)
		self.seq_move_x(depth-1,depth-1)
		if level: self.seq_move_lift(level,level)
		self.seq_move_x(2,2)
		self.seq_tilt_lift(1,0)
		self.seq_place_on_stack(stack, col,level)
		self.seq_set_head_lights(False)
		self.seq_set_tail_lights(True)
		self.seq_move_x(1,-1)
		if level: self.seq_move_lift(level,0)
		self.seq_move_x(depth,-depth)
		self.seq_set_tail_lights(False)

	def put_x_n(self, stack, col, level, depth):
		self.seq_set_head_lights(True)
		self.seq_move_x(depth-1,1-depth)
		if level: self.seq_move_lift(level,level)
		self.seq_move_x(2,-2)
		self.seq_tilt_lift(1,0)
		self.seq_place_on_stack(stack, col,level)
		self.seq_set_head_lights(False)
		self.seq_set_tail_lights(True)
		self.seq_move_x(1,1)
		if level: self.seq_move_lift(level,0)
		self.seq_move_x(depth,depth)
		self.seq_set_tail_lights(False)

class Animation(AnimationComponents):
	
	def __init__(self,scene,scheduler):
		ForkliftAnimationTools.__init__(self,scene,scheduler)
		self.activate_crates()
		self.riser_level = 0

	def run1(self):
		if self.in_progress: return
		self.reset()
		self.in_progress = True
		
		for i in range(4):
			for j in range(4):
				self.seq_set_left_indicator(True)
				self.seq_rot(2,90)
				self.seq_set_left_indicator(False)
				self.fetch_x_p(self.scene.stack2, i, 3-j, 2)
				self.seq_set_right_indicator(True)
				self.seq_rot(4,-180)
				self.seq_set_right_indicator(False)
				self.put_x_n(self.scene.stack4, i, j, 3)
				self.seq_set_left_indicator(True)
				self.seq_rot(2,90)
				self.seq_set_left_indicator(False)
			self.seq_set_head_lights(True)
			self.seq_move_z(1,1)
			self.seq_set_head_lights(False)
		
		self.seq_set_tail_lights(True)
		self.seq_move_z(4,-4)
		self.seq_set_tail_lights(False)
		
		for i in range(4):
			for j in range(4):
				self.seq_set_left_indicator(True)
				self.seq_rot(2,90)
				self.seq_set_left_indicator(False)
				self.fetch_x_p(self.scene.stack1, i, 3-j, 3)
				self.seq_set_right_indicator(True)
				self.seq_rot(4,-180)
				self.seq_set_right_indicator(False)
				self.put_x_n(self.scene.stack3, i, j, 2)
				self.seq_set_left_indicator(True)
				self.seq_rot(2,90)
				self.seq_set_left_indicator(False)
			self.seq_set_head_lights(True)
			self.seq_move_z(1,1)
			self.seq_set_head_lights(False)
		
		self.seq_set_tail_lights(True)
		self.seq_move_z(4,-4)
		self.seq_set_tail_lights(False)
		
		for i in range(4):
			for j in range(4):
				self.seq_set_right_indicator(True)
				self.seq_rot(2,-90)
				self.seq_set_right_indicator(False)
				self.fetch_x_n(self.scene.stack3, i, 3-j, 2)
				self.seq_set_left_indicator(True)
				self.seq_rot(4,180)
				self.seq_set_left_indicator(False)
				self.put_x_p(self.scene.stack1, i, j, 3)
				self.seq_set_right_indicator(True)
				self.seq_rot(2,-90)
				self.seq_set_right_indicator(False)
			self.seq_set_head_lights(True)
			self.seq_move_z(1,1)
			self.seq_set_head_lights(False)
		
		self.seq_set_tail_lights(True)
		self.seq_move_z(4,-4)
		self.seq_set_tail_lights(False)
		
		for i in range(4):
			for j in range(4):
				self.seq_set_right_indicator(True)
				self.seq_rot(2,-90)
				self.seq_set_right_indicator(False)
				self.fetch_x_n(self.scene.stack4, i, 3-j, 3)
				self.seq_set_left_indicator(True)
				self.seq_rot(4,180)
				self.seq_set_left_indicator(False)
				self.put_x_p(self.scene.stack2, i, j, 2)
				self.seq_set_right_indicator(True)
				self.seq_rot(2,-90)
				self.seq_set_right_indicator(False)
			self.seq_set_head_lights(True)
			self.seq_move_z(1,1)
			self.seq_set_head_lights(False)
		
		self.seq_set_tail_lights(True)
		self.seq_move_z(4,-4)
		self.seq_set_tail_lights(False)
		
		self.seq_set_head_lights(False)
		self.seq_finished()
		self.seq_start()

	def run2(self):
		if self.in_progress: return
		self.reset()
		self.in_progress = True
		self.seq_set_head_lights(True)
		self.seq_move_z(3,6)
		self.seq_set_head_lights(False)
		self.seq_set_left_indicator(True)
		self.seq_rot(2,90)
		self.seq_set_left_indicator(False)
		self.seq_set_head_lights(True)
		self.seq_move_x(4,8)
		self.seq_set_head_lights(False)
		self.seq_set_left_indicator(True)
		self.seq_rot(2,90)
		self.seq_set_left_indicator(False)
		self.seq_set_head_lights(True)
		self.seq_move_z(4,-8)
		self.seq_set_head_lights(False)
		self.seq_set_left_indicator(True)
		self.seq_rot(2,90)
		self.seq_set_left_indicator(False)
		self.seq_set_head_lights(True)
		self.seq_move_x(4,-8)
		self.seq_set_head_lights(False)
		self.seq_set_left_indicator(True)
		self.seq_rot(2,90)
		self.seq_set_left_indicator(False)
		self.seq_set_head_lights(True)
		self.seq_move_z(1,2)
		self.seq_set_head_lights(False)
		self.seq_finished()
		self.seq_start()

	def move_forward(self):
		if self.in_progress: return
		theta = radians(self.scene.forklift.angle)
		self.scene.forklift.set_head_lights(True)
		self.move_z(1,cos(theta))
		self.move_x(1,sin(theta), lambda: self.scene.forklift.set_head_lights(False))

	def move_backward(self):
		if self.in_progress: return
		theta = radians(self.scene.forklift.angle)
		self.scene.forklift.set_tail_lights(True)
		self.move_z(1,-cos(theta))
		self.move_x(1,-sin(theta), lambda: self.scene.forklift.set_tail_lights(False))

	def turn_left(self):
		if self.in_progress: return
		self.scene.forklift.set_left_indicator(True)
		self.rot(1,15, lambda:self.scene.forklift.set_left_indicator(False))
	
	def turn_right(self):
		if self.in_progress: return
		self.scene.forklift.set_right_indicator(True)
		self.rot(1,-15, lambda: self.scene.forklift.set_right_indicator(False))
		

	def lift_riser(self):
		if self.in_progress: return
		if self.riser_level == 3: return
		self.riser_level += 1
		self.move_lift(2, self.riser_level)

	def drop_riser(self):
		if self.in_progress: return
		if self.riser_level == 0: return
		self.riser_level -= 1
		self.move_lift(2, self.riser_level)





