import sys
import math
import cmath

class VRObj():
	def __init__(self, name='no_name', geometry=[[ [ [0.0, 0.0, 0.0] ], [0.0, 0.0, 0.0], [1.0+0.0*1j, 1.0+0.0*1j, 1.0+0.0*1j] ]], closed=True):
		
		self.name = name
		
		self.vec = []
		self.node = []
		self.face = []

		self.shape = []
		self.trajectory = []
		self.rotation = []
		
		node_num = len(geometry[0][0])
		
		i = 1
		for g in geometry:
			
			shp = g[0]
			trj = g[1]
			rot = g[2]
			
			self.shape.append(shp)
			self.trajectory.append(trj)
			self.rotation.append(rot)
			
			self.node.append( range(i, i + node_num) + [ i ])
			i = i + node_num
			
			# Complex number for rotation(rad)
			c_rotX = rot[0]
			c_rotY = rot[1]
			c_rotZ = rot[2]
			
			v = []
			for x, y, z in shp:
				# Rotation around x axis
				Qx = c_rotX * ( y + z * 1j)
				y = Qx.real
				z = Qx.imag
				# Rotation around y axis
				Qy = c_rotY * ( x + z * 1j)
				x = Qy.real
				z = Qy.imag
				# Rotation around z axis
				Qz = c_rotZ * ( x + y * 1j)
				x = Qz.real
				y = Qz.imag
				# Move
				v.append( [ x + trj[0], y + trj[1], z + trj[2]] )
				
			self.vec.append(v)
		
		# face
		for j in range(len(self.node) - 1):
			face = []
			if ( closed == True ):
				for k in range(node_num):
					face.append( [ self.node[j][k], self.node[j+1][k], self.node[j+1][k+1], self.node[j][k+1] ])
					
				self.face.append(face)
			else:
				for k in range(node_num - 1):
					face.append( [ self.node[j][k], self.node[j+1][k], self.node[j+1][k+1], self.node[j][k+1] ])
					
				self.face.append(face)
				
	def move(self, ( dx, dy, dz ) = ( 0.0, 0.0, 0.0 ) ):
		
		for shp in self.vec:
			for sv in shp:
				( sv[0], sv[1], sv[2] ) = ( sv[0] + dx, sv[1] + dy, sv[2] + dz )
		
		for trj in self.trajectory:
			( trj[0], trj[1], trj[2] ) = ( trj[0] + dx , trj[1] + dy, trj[2] +dz )
	
	def rotate(self, ( c_rotX, c_rotY, c_rotZ ) = ( 1.0 + 0.0*1j ,1.0 + 0.0*1j, 1.0 + 0.0*1j )):
		
		for shp in self.vec:
			for v in shp:
				# Rotation around x axis
				Qx = c_rotX * ( v[1] + v[2] * 1j)
				v[1] = Qx.real
				v[2] = Qx.imag
				# Rotation around y axis
				Qy = c_rotY * ( v[0] + v[2] * 1j)
				v[0] = Qy.real
				v[2] = Qy.imag
				# Rotation around z axis
				Qz = c_rotZ * ( v[0] + v[1] * 1j)
				v[0] = Qz.real
				v[1] = Qz.imag
				
		for trj in self.trajectory:
			# Rotation around x axis
			Tx = c_rotX * ( trj[1] + trj[2] * 1j )
			trj[1] = Tx.real
			trj[2] = Tx.imag
			# Rotation around y axis
			Ty = c_rotY * ( trj[0] + trj[2] * 1j )
			trj[0] = Ty.real
			trj[2] = Ty.imag
			# Rotation around z axis
			Tz = c_rotZ * ( trj[0] + trj[1] * 1j)
			trj[0] = Tz.real
			trj[1] = Tz.imag
			
		for rot in self.rotation:
			( rot[0], rot[1], rot[2] ) = ( rot[0] * c_rotX, rot[1] * c_rotY, rot[2] * c_rotZ )
		
		
	def startTraj(self):
		return self.trajectory[0]
		
	def endTraj(self):
		return self.trajectory[-1]
		
	def getTraj(self, idx=0):
		return self.trajectory[idx]
		
	def startRot(self):
		return self.rotation[0]
		
	def endRot(self):
		return self.rotation[-1]
		
	def getRot(self, idx=0):
		return self.rotation[idx]
		
	def createWaveFormObj(self):
		
		fobj = open(self.name + '.obj', 'w')
		
		print >> fobj, 'g ' + self.name
		
		for v_arry in self.vec:
			for v in v_arry:
				print >> fobj, 'v ' + str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2])
		
		for f_arry in self.face:
			for f in f_arry:
				print >> fobj, 'f ' + str(f[0]) + ' ' + str(f[1]) + ' ' + str(f[2]) + ' ' + str(f[3])
		
		fobj.close()
		
if __name__ == '__main__' :
	
	mesh = 36
	
	rad = 2.0 * cmath.pi / mesh
	
	inlet_shape = []
	outlet_shape = []
		
	for p in range(mesh):
		x = 100 * cmath.cos( rad * p )
		y = 100 * cmath.sin( rad * p )
		inlet_shape.append( [ x, y, 0])

	sample_geo = []
	
	for i in range(181):
		sample_geo.append( [ inlet_shape, (0.0, 0.0, 0.0), ( cmath.rect(1.0, 0.0), cmath.rect(1.0, (cmath.pi/180) * i ), cmath.rect(1.0, 0.0)) ] )
	
	sphere = VRObj(name='sphere', geometry=sample_geo)
	
	sphere.createWaveFormObj()

	deg = 360 / mesh
	
	sample_geo =[]
	waveShape = []
	
	for p in range(mesh):
		x = deg * p
		y = 10.0 * cmath.cos( 4 * math.radians(x) )
		waveShape.append( [ x, y, 0])
	
	sample_geo.append( [ waveShape, (0.0, 0.0, 0.0),  ( cmath.rect(1.0, 0.0), cmath.rect(1.0, 0.0), cmath.rect(1.0, 0.0)) ])
	sample_geo.append( [ waveShape, (0.0, 0.0, 50.0), ( cmath.rect(1.0, 0.0), cmath.rect(1.0, 0.0), cmath.rect(1.0, 0.0)) ])

	curtain = VRObj(name='curtain', geometry=sample_geo, closed=False)
	
	curtain.createWaveFormObj()
