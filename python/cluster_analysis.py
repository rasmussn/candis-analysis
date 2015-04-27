from pycandis import ReadCandis
import numpy as np

def indexOf(row, col, data):
   ir = row % data.shape[0]
   ic = col % data.shape[1]
   return ic + ir*data.shape[1]
# end indexOf

def row_column(index, data):
   ic = index%data.shape[1]
   ir = int((index - ic)/float(data.shape[1]))
   return (ir, ic)
# end row_column

def isPresent(index, completed):
   isPresent = True
   try:
      i = completed.index(index)
   except ValueError:
      isPresent = False
   return isPresent
#end isPresent

def cluster_list(row, col, data, threshold, completed):
   me = indexOf(row, col, data)

   ## check to see if me location needs to be processed
   #
   ir = row % data.shape[0]
   ic = col % data.shape[1]
   if isPresent(me, completed) | (data[ir,ic] < threshold):
      return completed

   completed += [me]

   ## search 3x3 neighborhood
   #
   for ic in range(3):
      for ir in range(3):
         completed = cluster_list(row-1+ir, col-1+ic, data, threshold, completed)

   return completed
# end max_cluster_size

def islands(data, threshold):
   """ Returns a list of islands (connected set of cells above threshold)"""
   finished = []
   islands  = []

   for col in range(data.shape[1]):
      for row in range(data.shape[0]):
         me = indexOf(row, col, data)
         if isPresent(me, finished) == False:
           island = cluster_list(row, col, data, threshold, [])
           if island != []:
              islands += [island,]
           # add cells in island to finished list
           for cell_index in island:
              if isPresent(cell_index, finished) == False:
                 finished += [cell_index,]
         else:
            finished += [me,]
   return islands
# end islands

def island_center(data, island):
   row_sum = 0
   col_sum = 0

   for cell_index in island:
      (row,col) = row_column(cell_index, data)
      row_sum += row
      col_sum += col

   return (row_sum/float(len(island)), col_sum/float(len(island)))
# end island_center

def island_peak_location(data, island):
   intensity = 0.0
   peak = 0.0
   loc = ()

   for cell_index in island:
      (row,col) = row_column(cell_index, data)
      intensity += data[row,col]
      if data[row,col] > peak:
         loc = (row,col)

   return loc
# end island_peak_location

def island_intensity(data, island):
   intensity = 0.0
   peak = 0.0

   for cell_index in island:
      (row,col) = row_column(cell_index, data)
      intensity += data[row,col]
      if data[row,col] > peak: peak = data[row,col]

   return (intensity, peak)
# end island_center

def max_cluster_size(data, threshold):
   max = 0

   for col in range(data.shape[1]):
      for row in range(data.shape[0]):
         cluster = cluster_list(row, col, data, threshold, [])
         if max < len(cluster): max = len(cluster)
         
   return max
# end max_cluster_size

def cluster_histogram(data, threshold, blocking_factor):
   """Returns an 2D ndarray histogram of number of cells with data above threshold"""

   nrows = blocking_factor
   ncols = blocking_factor

   nRowCells = data.shape[0]/nrows
   nColCells = data.shape[1]/ncols

   buckets = np.zeros((nrows,ncols), dtype='int32')

   if (nrows*nRowCells != data.shape[0]):
      print('blocking factor doesn\'t lead to even number of cells'); exit
   if (ncols*nColCells != data.shape[1]):
      print('blocking factor doesn\'t lead to even number of cells'); exit

   for ic in range(data.shape[1]):
      col = ic/nColCells
      for ir in range(data.shape[0]):
         row = ir/nRowCells
         if data[ir][ic] > threshold:
            buckets[row,col] += 1

   return buckets
# end cluster_histogram

def intensity(data):
   """Returns intensity (sum of data) and average intensity"""

   nrows = data.shape[0]
   ncols = data.shape[1]

   lum_sum = data.sum()
   lum_avg = lum_sum/(nrows*ncols)

   return (lum_sum, lum_avg)
# end intensity
