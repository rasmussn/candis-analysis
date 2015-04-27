import sys
sys.path = ['../candis-analysis',] + sys.path

import cluster_analysis as ca
import CandisConvert as cancon

num_bins = 16
basename = 'a014'
begin    = 3333
end      = 3334         # inclusive

threshold = .001

cc = cancon.CandisConvert(basename)

for file_index in range(begin,end+1):
   data = cc.getField(file_index, 'rainflux')
   data = abs(data)
   vxflux = cc.getField(file_index, 'vxflux')
   vyflux = cc.getField(file_index, 'vyflux')

   islands = ca.islands(data, threshold)
   print file_index, len(islands)
   for island in islands:
      (row_avg, col_avg) = ca.island_center(data, island)
      (row_peak, col_peak) = ca.island_peak_location(data, island)
      (intensity, peak) = ca.island_intensity(data, island)
      print '  {0:3d} {1:3d} {2:3d} {3:.2f} {4:.2f} {5:.4f} {6:.4f} {7:.4f} {8:.4f} {9:.4f}'.format(len(island), row_peak, col_peak, row_avg, col_avg, intensity, intensity/len(island), peak, vxflux[row_peak,col_peak], vyflux[row_peak,col_peak])
