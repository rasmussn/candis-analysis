from evtk.hl  import imageToVTK
from evtk.vtk import VtkFile, VtkImageData
from pycandis import ReadCandis
import numpy as np

class CandisConvert(object):
   """ A class to convert candis files"""

   def __init__(self, prefix):
      """Constructor: Set the candis prefix, i.e., 'a006'"""
      self.prefix = prefix
   # end __init__

   def ipad(self, i):
      s = str(i)
      if i < 10:
         return '00' + s
      elif i < 100:
         return '0' + s
      else:
         return s
   # end ipad

   def filename(self, i):
      """Returns a Candis filename based on the prefix and a given integer"""
      return self.prefix + "." + self.ipad(i)
   # end canfile

   def read(self, i):
      """Returns a Candis file object based on the prefix and a given integer"""
      return ReadCandis(self.filename(i))
   # end canfile

   def getTime(self, i):
      cfile = self.read(i)
      return cfile.getField('time').data

   def getFieldNames(self, canfile, dim):
      """Returns a list of the fields in the Candis object of rank dim"""
      l = []
      keys = canfile.vfields.keys()
      for key in keys:
         vfield = canfile.getField(key)
         if len(vfield.dims) == dim:
            l.append(key)
      return l
   # end canFieldsDim

   def getField(self, i, field):
      """Returns an ndarray for the given field at file index i"""
      cfile = self.read(i)
      vfield = cfile.getField('rainflux')
      return vfield.data
   # end getField

   def convertToVTK(self, i, key):
      cfile = self.read(i)
      vfield = cfile.getField(key)
      data = vfield.data
      if len(vfield.dims) == 2:
         data = data.reshape(data.shape + (1,))
      d = {}
      d[key] = data
      imageToVTK(key + "." + self.filename(i), cellData = d)
   # end convertToVTK

   def convertRainfluxToVTK(self, i, cfile):
      rainflux = cfile.getField('rainflux').data
      rainflux = rainflux.reshape(rainflux.shape + (1,))

      (nx,ny,nz) = rainflux.shape
      print nx, ny, nz
      ncells = nx*ny*nz
      start   = (  0,  0,  0)
      end     = ( nx, ny, nz)
      origin  = (0.0,0.0,0.0)
      spacing = (1.0,1.0,1.0)

      w = VtkFile("rainflux." + self.filename(i), VtkImageData)
      w.openGrid(start, end, origin, spacing)
      w.openPiece(start, end)
      w.openData("Cell", scalars = "rainflux")
      w.addData("rainflux", rainflux)
      w.closeData("Cell")
      w.closePiece()
      w.closeGrid()
      w.appendData(data = rainflux)
      w.save()

   # end convertRainfluxToVTK

   def convertVelocitiesToVTK(self, i, cfile):
      vx = cfile.getField('vx').data
      vy = cfile.getField('vy').data
      vz = cfile.getField('vz').data

      nx,ny,nz = vx.shape
      ncells = nx*ny*nz

      start   = (  0,  0,  0)
      end     = ( nx, ny, nz)
      origin  = (0.0,0.0,0.0)
      spacing = (1.0,1.0,1.0)

      w = VtkFile("v." + self.filename(i), VtkImageData)
      w.openGrid(start, end, origin, spacing)
      w.openPiece(start, end)
      w.openData("Cell", vectors = "velocity")
      w.addData("velocity", (vx,vy,vz))
      w.closeData("Cell")
      w.closePiece()
      w.closeGrid()
      w.appendData(data = (vx,vy,vz))
      w.save()

   # end convertVelocitiesToVTK

   def convertRainMixingToVTK(self, i, cfile):
      rr = cfile.getField('rr').data

      nx,ny,nz = rr.shape
      ncells = nx*ny*nz

      start   = (  0,  0,  0)
      end     = ( nx, ny, nz)
      origin  = (0.0,0.0,0.0)
      spacing = (1.0,1.0,1.0)

      w = VtkFile("rr." + self.filename(i), VtkImageData)
      w.openGrid(start, end, origin, spacing)
      w.openPiece(start, end)
      w.openData("Cell", scalars = "rr")
      w.addData("rr", rr)
      w.closeData("Cell")
      w.closePiece()
      w.closeGrid()
      w.appendData(data = rr)
      w.save()

   # end convertRainMixingToVTK

   def rainfluxDiffToVTK(self, i, altPrefix):
      """ Get Candis filenames based on the prefix and a given integer"""
      file1 = self.prefix + "/" + self.prefix + "." + self.ipad(i)
      file2 = altPrefix   + "/" + altPrefix   + "." + self.ipad(i)

      """Get Candis file objects based on the prefix and a given integer"""
      cfile1 = ReadCandis(file1)
      cfile2 = ReadCandis(file2)

      rainflux1 = cfile1.getField('rainflux').data
      rainflux2 = cfile2.getField('rainflux').data

      nx,ny = rainflux1.shape
      nz = 1
      ncells = nx*ny*nz
      start   = (  0,  0,  0)
      end     = ( nx, ny, nz)
      origin  = (0.0,0.0,0.0)
      spacing = (1.0,1.0,1.0)

      rainflux1 = rainflux1.reshape(rainflux1.shape + (1,))
      rainflux2 = rainflux2.reshape(rainflux2.shape + (1,))
      rain_diff = rainflux2 - rainflux1

      print "Maximum diff for", i, "is", rain_diff.max()

      w = VtkFile("rainflux_diff." + self.ipad(i), VtkImageData)
      w.openGrid(start, end, origin, spacing)
      w.openPiece(start, end)
      w.openData("Cell", scalars = "rainflux_diff")
      w.addData("rainflux_diff", rain_diff)
      w.closeData("Cell")
      w.closePiece()
      w.closeGrid()
      w.appendData(data = rain_diff)
      w.save()

   # end rainfluxDiffToVTK

# end class CandisConvert
