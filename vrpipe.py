import sys
import cmath
from vrapid import VRObj

class Pipe(VRObj):
	def __init__(self, name='Pipe', length=0.0, dia=0.0):
		self.name = name
		self.length = length
		self.radius = dia / 2.0
		
		mesh = 60
		
		rad = 2.0 * cmath.pi / mesh
		
		inlet_shape = []
		outlet_shape = []
			
		for p in range(mesh):
			x = self.radius * cmath.cos( rad * p )
			y = self.radius * cmath.sin( rad * p )
			inlet_shape.append( [ x, y, 0])
			outlet_shape.append([ x, y, 0])
	
		VRObj.__init__(self, name=self.name, geometry=[ [inlet_shape, [0.0, 0.0, 0.0], [1.0+0.0*1j, 1.0+0.0*1j, 1.0+0.0*1j]], [outlet_shape, [0.0, 0.0, self.length],[1.0+0.0*1j, 1.0+0.0*1j, 1.0+0.0*1j]]])

class Reducer(VRObj):
	def __init__(self, name='reducer', length=0.0, dia1=0.0, dia2=0.0 ):
		self.name = name
		self.length = length
		self.radius1 = dia1 / 2.0
		self.radius2 = dia2 / 2.0
		
		mesh = 60
		
		rad = 2.0 * cmath.pi / mesh
		
		inlet_shape = []
		outlet_shape = []
			
		for p in range(mesh):
			x_in = self.radius1 * cmath.cos( rad * p )
			y_in = self.radius1 * cmath.sin( rad * p )
			x_out= self.radius2 * cmath.cos( rad * p )
			y_out= self.radius2 * cmath.sin( rad * p )
			inlet_shape.append( [ x_in , y_in , 0])
			outlet_shape.append([ x_out, y_out, 0])
		
		VRObj.__init__(self, name=self.name, geometry=[ [inlet_shape, [0.0, 0.0, 0.0], [1.0+0.0*1j, 1.0+0.0*1j, 1.0+0.0*1j]], [outlet_shape, [0.0, 0.0, self.length], [1.0+0.0*1j, 1.0+0.0*1j, 1.0+0.0*1j]]])
		

class Elbow(VRObj):
	def __init__(self, name='elbow', dia=0.0, angle=(cmath.pi/2), arm=0.0, direction=(cmath.pi/2)):
		self.name = name
		self.radius = dia / 2.0
		self.angle  = angle
		self.arm    = arm
		self.direction = direction
		
		mesh = 60
		bendings = 60
		
		rad1 = 2.0 * cmath.pi / mesh
		rad2 = self.angle / bendings
		
		geo = []
		shape = []
		
		for p in range( mesh + 1 ):
			c_shp = cmath.rect( self.radius , rad1 * p )
			shape.append( [ c_shp.real , c_shp.imag , 0])
		
		for t in range( bendings + 1 ):
			w = rad2 * t
			c_Tr = cmath.rect( self.arm , w )
			geo.append( [ shape, [ c_Tr.real - self.arm, 0.0, c_Tr.imag ], [1.0+0.0*1j, cmath.rect(1.0, w) ,1.0+0.0*1j] ] )
			
		VRObj.__init__(self, name=self.name, geometry=geo)
		self.rotate((1.0+0.0*1j, 1.0+0.0*1j, cmath.rect(1.0, direction - cmath.pi)))


if __name__ == '__main__' :
	
#	p1 = Pipe(name='testPipe', length=500, dia=200.0)
#	r1 = Reducer(name='testReducer', length=300.0, dia1=200.0, dia2=150.0)
	e1 = Elbow(name='testElbow_D0', dia=150.0, angle=cmath.pi/2, arm=200.0, direction=cmath.pi * 0.0)
	e2 = Elbow(name='testElbow_D45', dia=150.0, angle=cmath.pi/2, arm=200.0, direction=cmath.pi / 4)
	e3 = Elbow(name='testElbow_D90', dia=150.0, angle=cmath.pi/2, arm=200.0, direction=cmath.pi / 2)
#	p2 = Pipe(name='testPipe2', length=800, dia=150.0)
	
	#r1.move((0.0, 0.0, 500.0))
#	r1.move(p1.endTraj())
	#e1.move((0.0, 0.0, 800.0))
#	e1.move(r1.endTraj())
	
	#p2.rotate((1+0j, cmath.rect(1.0, cmath.pi/2), 1+0j))
#	p2.rotate(e1.endRot())
	#p2.move((-200.0, 0.0, 1000.0))
#	p2.move(e1.endTraj())
	
#	p1.createWaveFormObj()
#	r1.createWaveFormObj()
	e1.createWaveFormObj()
	e2.createWaveFormObj()
	e3.createWaveFormObj()
#	p2.createWaveFormObj()
