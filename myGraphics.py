# Gangadhara, Karthik.
# kxg7851
# 2018-09-06

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
from CohenSutherland import clipLine 
from BézierPatch import resolve 
import numpy

class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def create_graphic_objects( self, model, canvas, doClip = False, doPerspective = False, doEuler = False, resolution = 4) :
    viewport = model.m_Viewport
    faces = model.m_Faces
    patches = model.m_Patches
    vertices = model.m_Vertices
    patchVertices = vertices
    width = int(canvas.cget( 'width' ))
    height = int(canvas.cget( 'height' ))
    port = (viewport[0] * width, viewport[1] * height, viewport[2] * width, viewport[3] * height)

    self.objects.append( canvas.create_rectangle(*port))
    if len(faces) > 0:
      for face in faces:
        face_vertices = tuple([model.getTransformedVertex(vNum, doPerspective, doEuler) for vNum in face])
        self.drawTriangle(canvas,*face_vertices,port,doClip)
    if len(patches) > 0:
      for patch in patches:
        result = resolve(resolution, patch, patchVertices, False)
        pointList = []
        for res in result:
          pointList.append(model.transformXYZ(res,doPerspective, doEuler))
        for row in range(resolution-1):
          rowStart = row * resolution
          for col in range(resolution-1):
            here = rowStart + col
            there = here + resolution
            triangleA = ( pointList[here], pointList[there], pointList[there+1] )
            triangleB = ( pointList[there+1], pointList[here+1], pointList[here] )
            self.drawTriangle(canvas,*triangleA,port,doClip)
            self.drawTriangle(canvas,*triangleB,port,doClip)

  def redisplay( self, canvas, event ) :
    pass

  def drawTriangle(self, canvas, v1, v2, v3, portal, doClip ) :
      if not doClip:
        self.objects.append( canvas.create_line(
          v1[0],v1[1],
          v2[0],v2[1],
          v3[0],v3[1],
          v1[0],v1[1]
        ))
      else:
        clip_result = clipLine(v1[0],v1[1],v2[0],v2[1], portal)
        if clip_result[0]:
          self.objects.append( canvas.create_line(clip_result[1],clip_result[2], clip_result[3],clip_result[4]))
        clip_result1 = clipLine(v2[0],v2[1],v3[0],v3[1], portal)
        if clip_result1[0]:
          self.objects.append( canvas.create_line(clip_result1[1],clip_result1[2], clip_result1[3],clip_result1[4]))
        clip_result2 = clipLine(v3[0],v3[1],v1[0],v1[1], portal)
        if clip_result2[0]:
          self.objects.append( canvas.create_line(clip_result2[1],clip_result2[2], clip_result2[3],clip_result2[4]))
