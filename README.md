# Grid2Hierarchical: An open-source academic research tool for building macro GMNS networks from micro GMNS networks for transportation system modeling and optimization

## Requirements
- shapely

## Simple Example
>The recommended way to install use the package is colning the source code from [github](https://github.com/PariseC/grid2hierarchical).
```python
>>>import grid2hierarchical as g2h

"""Step 1: Read GMNS network"""
net=g2h.read_gmns_network_from_csv('./data')

"""Step 2: Build macro GMNS network"""
# set the number of grids to build a macro GMNS network
g2h.partition_grid(net,n_grids=(100,100))
# or set the size of grids to build a macro GMNS network
# g2h.partition_grid(net,s_grids=(0.005,0.005))

"""Step 3: Save network files"""
g2h.save_network(net,output_folder='./macro_network_by_n_grids')
```
## Sample Networks

### Suzhou, China
micro gmns network 1:
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Suzhou-n_grids/gmns%20network%201.png?raw=true" width="800" height="600" alt="all modes network"/><br/>
micro gmns network 2:
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Suzhou-n_grids/gmns%20network%202.png?raw=true" width="800" height="600" alt="auto mode network"/><br/>
micro gmns network 3:
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Suzhou-n_grids/gmns%20network%203.png?raw=true" width="800" height="600" alt="auto mode network"/><br/>
macro gmns network 1：
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Suzhou-n_grids/gmns%20network%204.png?raw=true" width="800" height="600" alt="auto mode network"/><br/>
macro gmns network 2:
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Suzhou-n_grids/gmns%20network%205.png?raw=true" width="800" height="600" alt="auto mode network"/><br/>
macro gmns network 3:
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Suzhou-n_grids/gmns%20network%206.png?raw=true" width="800" height="600" alt="auto mode network"/><br/>

### Tempe, US
micro gmns network 1:
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Tempe-n_grids/gmns%20network%201.png?raw=true" width="800" height="600" alt="all modes network"/><br/>
micro gmns network 2:
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Tempe-n_grids/gmns%20network%202.png?raw=true" width="800" height="600" alt="auto mode network"/><br/>
micro gmns network 3:
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Tempe-n_grids/gmns%20network%203.png?raw=true" width="800" height="600" alt="auto mode network"/><br/>
macro gmns network 1：
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Tempe-n_grids/gmns%20network%204.png?raw=true" width="800" height="600" alt="auto mode network"/><br/>
macro gmns network 2：
<img src="https://github.com/PariseC/grid2hierarchical/blob/main/examples/Tempe-n_grids/gmns%20network%205.png?raw=true" width="800" height="600" alt="auto mode network"/><br/>


