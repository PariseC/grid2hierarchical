
import grid2hierarchical as g2h


net=g2h.read_gmns_network_from_csv('../data/Suzhou')
g2h.partition_grid(net,n_grids=(100,100))
# g2h.partition_grid(net,s_grids=(0.005,0.005))
# g2h.partition_grid(net,level=3)
g2h.save_network(net,output_folder='./Suzhou-n_grids')
