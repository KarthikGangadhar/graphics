# Gangadhara, Karthik.
# kxg7851
# 2018-09-06

import sys
import math

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.m_Patches =  []
    self.m_a = ()
    self.m_s = ()
    self.m_r00 = 0
    self.m_r01 = 0
    self.m_r02 = 0
    self.m_r10 = 0
    self.m_r11 = 0
    self.m_r20 = 0    
    self.m_r20 = 0
    self.m_r21 = 0
    self.m_r22 = 0
    self.m_r12 = 0
    self.m_ex = 0
    self.m_ey = 0
    self.m_ez = 0

    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
    with open( inputFile, 'r' ) as fp :
      lines = fp.read().replace('\r', '' ).split( '\n' )

    for ( index, line ) in enumerate( lines, start = 1 ) :
      line = line.strip()
      
      if (line and line[0] != "#") :
        lineData = line.split()
        if(lineData[0] == "f"):
          try:
            faces = [(int(x)-1) for x in lineData if x != "f"]
            if len(faces) ==  3:
              self.m_Faces.append((tuple(faces)))
            else:
              print('line '+ str(index) +' is a malformed face spec.')          
          except:
            print('line '+ str(index) +' is a malformed face spec.')
        elif(lineData[0] == "p"):
          try:
            patches = [(int(x)-1) for x in lineData if x != "p"]
            if len(patches) >=  1:
              self.m_Patches.append((tuple(patches)))
            else:
              print('line '+ str(index) +' is a malformed patch spec.')          
          except:
            print('line '+ str(index) +' is a malformed patch spec.')
        elif(lineData[0] == "v"):
          try:
            vertex = [(float(x)) for x in lineData if x != "v"]
            if len(vertex) == 3:
              self.m_Vertices.append((tuple(vertex)))
            else:
              print('line '+ str(index) +' is a malformed vertex spec.')  
          except:
            print('line '+ str(index) +' is a malformed vertex spec.')
        elif(lineData[0] == "w"):
          try:
            window = [(float(x)) for x in lineData if x != "w"]
            if len(self.m_Window) >= 1 and len(window) == 4:
              print('line '+ str(index) +' is a duplicate window spec.')
              self.m_Window = tuple(window)
            elif len(window) == 4:
              self.m_Window = tuple(window)
            else:
              print('line '+ str(index) +' is a malformed window spec.')            
          except:
            print('line '+ str(index) +' is a malformed window spec.')            
        elif(lineData[0] == "s"):
          try:
            viewport = [(float(x)) for x in lineData if x != "s"]
            if len(self.m_Viewport) >= 1 and len(viewport) == 4:
              print('line '+ str(index) +' is a duplicate viewport spec.')
              self.m_Viewport = tuple(viewport)
            elif len(viewport) == 4:
              self.m_Viewport = tuple(viewport)
            else:
              print('line '+ str(index) +' is a malformed viewport spec.')
          except:
            print('line '+ str(index) +' is a malformed viewport spec.')            

  def getBoundingBox( self ) :
    vertices = self.getVertices()
    x_ordinates = [vertex[0] for vertex in vertices]
    y_ordinates = [vertex[1] for vertex in vertices]
    z_ordinates = [vertex[2] for vertex in vertices]
    (xmin, xmax) = (min(x_ordinates), max(x_ordinates))
    (ymin, ymax) =(min(y_ordinates), max(y_ordinates))
    (zmin, zmax) = (min(z_ordinates),max(z_ordinates))
    return ( xmin, xmax, ymin, ymax, zmin, zmax )

  def specifyTransform( self, ax, ay, sx, sy, distance = None) :
    self.m_a = (ax,ay)
    self.m_s = (sx,sy)
    self.pers_distance = distance 

  def getTransformedVertex( self, vNum , perspective = False, doEuler = False) :
    Vertices = self.getVertices()
    vertex = Vertices[vNum]
    x_vertex = vertex[0]
    y_vertex = vertex[1]
    z_vertex = vertex[2]

    if perspective:
      x_vertex = vertex[0] / (1 - (vertex[2]/self.pers_distance)) if vertex[2] != self.pers_distance else 0
      y_vertex = vertex[1] / (1 - (vertex[2]/self.pers_distance)) if vertex[2] != self.pers_distance else 0

    if doEuler:
      xp = (self.m_r00 * x_vertex) + self.m_r01 * y_vertex + self.m_r02 * z_vertex + self.m_ex
      yp = (self.m_r10 * x_vertex) + self.m_r11 * y_vertex + self.m_r12 * z_vertex + self.m_ey
      zp = (self.m_r20 * x_vertex) + self.m_r21 * y_vertex + self.m_r22 * z_vertex + self.m_ez
      (x_vertex,y_vertex,z_vertex) = (xp,yp,zp)

    x = (self.m_s[0] * x_vertex) + self.m_a[0]
    y = (self.m_s[1] * y_vertex) + self.m_a[1]
    return (x, y, 0.0)

  def transformXYZ(self, point, perspective = False, doEuler = False):
    x_vertex = point[0]
    y_vertex = point[1]
    z_vertex = point[2]

    if perspective:
      x_vertex = point[0] / (1 - (point[2]/self.pers_distance)) if point[2] != self.pers_distance else 0
      y_vertex = point[1] / (1 - (point[2]/self.pers_distance)) if point[2] != self.pers_distance else 0

    if doEuler:
      xp = (self.m_r00 * x_vertex) + self.m_r01 * y_vertex + self.m_r02 * z_vertex + self.m_ex
      yp = (self.m_r10 * x_vertex) + self.m_r11 * y_vertex + self.m_r12 * z_vertex + self.m_ey
      zp = (self.m_r20 * x_vertex) + self.m_r21 * y_vertex + self.m_r22 * z_vertex + self.m_ez
      (x_vertex,y_vertex,z_vertex) = (xp,yp,zp)

    x = (self.m_s[0] * x_vertex) + self.m_a[0]
    y = (self.m_s[1] * y_vertex) + self.m_a[1]
    return (x, y, 0.0)

  def getCenter(self ):
    ( xmin, xmax, ymin, ymax, zmin, zmax ) = self.getBoundingBox()
    return ((xmin + xmax)/2, ((ymin + ymax)/2),((zmin + zmax)/2)) 


  def specifyEulerAngles(self, roll = 0.0, pitch = 0.0, yaw =0.0):
    roll = math.radians(roll)
    pitch = math.radians(pitch)
    yaw = math.radians(yaw)

    self.m_r00 = math.cos(yaw) * math.cos(pitch)
    self.m_r01 = -1 * math.cos(pitch) * math.sin(yaw)
    self.m_r02 = math.sin(pitch)
    self.m_r10 = math.cos(roll) * math.sin(yaw) + math.cos(yaw) * math.sin(roll) * math.sin(pitch)
    self.m_r11 = math.cos(roll) * math.cos(yaw) - math.sin(roll) * math.sin(yaw) * math.sin(pitch)
    self.m_r12 = -1 * math.cos(pitch) * math.sin(roll)
    self.m_r20 = -1 * math.cos(roll) * math.cos(yaw) * math.sin(pitch) + math.sin(roll) * math.sin(yaw)
    self.m_r21 = math.cos(roll) * math.sin(yaw) * math.sin(pitch) + math.cos(yaw) * math.sin(roll)
    self.m_r22 = math.cos(roll) * math.cos(pitch)

    (tx,ty,tz) = self.getCenter()
  
    self.m_ex = (-1 * (self.m_r00 * tx)) -  ( self.m_r01 * ty) - (self.m_r02 * tz) + tx
    self.m_ey = (-1 * (self.m_r10 * tx)) -  ( self.m_r11 * ty) - (self.m_r12 * tz) + ty
    self.m_ez = (-1 * (self.m_r20 * tx)) -  ( self.m_r21 * ty) - (self.m_r22 * tz) + tz
  
  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window
  def getPatches( self )  : return self.m_Patches

#---------#---------#---------#---------#---------#--------#
def constructTransform( w, v, width, height ) :
  (fx,fy) = (-w[0], -w[1])
  (gx,gy) = (width*v[0], height*v[1])
  sx = (width * (v[2] - v[0]))/(w[2] - w[0])
  sy = (height * (v[3] - v[1]))/(w[3] - w[1])
  ax = fx * sx + gx
  ay = fy * sy + gy
  return ( ax, ay, sx, sy )

#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load and the canvas size.
  fName  = sys.argv[1]
  width  = int( sys.argv[2] )
  height = int( sys.argv[3] )

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( "%s: %d vert%s, %d face%s" % (
    fName,
    len( model.getVertices() ), 'ex' if len( model.getVertices() ) == 1 else 'ices',
    len( model.getFaces() ), '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( '     ', v )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( '     ', f )

  w = model.getWindow()
  v = model.getViewport()
  print( 'Window line:', w )
  print( 'Viewport line:', v )
  print( 'Canvas size:', width, height )
  print( 'Bounding box:', model.getBoundingBox() )

  ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )
  print( f'Transform is {ax} {ay} {sx} {sy}' )

  model.specifyTransform( ax, ay, sx, sy)

  print( 'First 3 transformed vertices:' )
  for vNum in range( 3 ) :
    print( '     ', model.getTransformedVertex( vNum ) )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
