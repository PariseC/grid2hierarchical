import copy
import threading
from .classes import *
from .setting import *
from shapely import geometry

def _create_cells_by_n_grids(net,n_grids):
    n_rows = n_grids[0]
    n_cols = n_grids[1]
    cell_id=0
    for row in range(n_rows):
        for col in range(n_cols):
            grid_node=GridNode()
            grid_node.cell_id=cell_id

            left_top_y=round(net.min_y_coord+(row+1)/n_rows*(net.max_y_coord-net.min_y_coord),Coordinate_Precision)
            left_top_x=round(net.min_x_coord+col/n_cols*(net.max_x_coord-net.min_x_coord),Coordinate_Precision)

            right_top_y=round(net.min_y_coord+(row+1)/n_rows*(net.max_y_coord-net.min_y_coord),Coordinate_Precision)
            right_top_x=round(net.min_x_coord+(col+1)/n_cols*(net.max_x_coord-net.min_x_coord),Coordinate_Precision)

            right_bottom_y=round(net.min_y_coord+row/n_rows*(net.max_y_coord-net.min_y_coord),Coordinate_Precision)
            right_bottom_x=round(net.min_x_coord+(col+1)/n_cols*(net.max_x_coord-net.min_x_coord),Coordinate_Precision)

            left_bottom_y=round(net.min_y_coord+row/n_rows*(net.max_y_coord-net.min_y_coord),Coordinate_Precision)
            left_bottom_x=round(net.min_x_coord+col/n_cols*(net.max_x_coord-net.min_x_coord),Coordinate_Precision)

            bounds=[(left_top_x,left_top_y),(right_top_x,right_top_y),
                    (right_bottom_x,right_bottom_y),(left_bottom_x,left_bottom_y),(left_top_x,left_top_y)]
            grid_node.geometry=geometry.Polygon(bounds)
            grid_node.x_coord=round((left_bottom_x+right_bottom_x)/2,Coordinate_Precision)
            grid_node.y_coord=round((left_bottom_y+left_top_y)/2,Coordinate_Precision)
            net.grid_node_dict[grid_node.cell_id]=grid_node
            cell_id+=1

def _create_cells_by_s_grids(net,s_grids):
    cell_width = s_grids[0]
    cell_height = s_grids[1]
    cell_id = 0
    left_bottom_x_=net.min_x_coord

    while left_bottom_x_<=net.max_x_coord:
        left_bottom_y_ = net.min_y_coord
        while left_bottom_y_<=net.max_y_coord:
            grid_node = GridNode()
            grid_node.cell_id = cell_id

            left_top_y = round(left_bottom_y_+cell_height,Coordinate_Precision)
            left_top_x = round(left_bottom_x_,Coordinate_Precision)

            right_top_y = round(left_bottom_y_+cell_width,Coordinate_Precision)
            right_top_x = round(left_bottom_x_+cell_height, Coordinate_Precision)

            right_bottom_y = round(left_bottom_y_,Coordinate_Precision)
            right_bottom_x = round(left_bottom_x_+cell_width,Coordinate_Precision)

            left_bottom_y = round(left_bottom_y_,Coordinate_Precision)
            left_bottom_x = round(left_bottom_x_,Coordinate_Precision)

            bounds = [(left_top_x, left_top_y), (right_top_x, right_top_y),
                      (right_bottom_x, right_bottom_y), (left_bottom_x, left_bottom_y), (left_top_x, left_top_y)]
            grid_node.geometry = geometry.Polygon(bounds)
            grid_node.x_coord = round((left_bottom_x + right_bottom_x) / 2, Coordinate_Precision)
            grid_node.y_coord = round((left_bottom_y + left_top_y) / 2, Coordinate_Precision)
            net.grid_node_dict[grid_node.cell_id] = grid_node
            cell_id += 1
            left_bottom_y_=left_bottom_y_+cell_height
        left_bottom_x_=left_bottom_x_+cell_width

def _match_nodes(net):
    #establish the mapping between macro nodes and micro nodes
    node_dict = copy.deepcopy(net.node_dict)
    grid_node_dict=copy.deepcopy(net.grid_node_dict)
    net.grid_node_dict={}
    cell_id = 0
    for _,grid_node in grid_node_dict.items():
        x_min, y_min, x_max, y_max = grid_node.geometry.bounds
        node_dict_={}
        for _,node in node_dict.items():
            if x_min <= node.x_coord <= x_max and y_min <= node.y_coord <= y_max:
                # if mic_node.geometry.within(mac_node.boundary):
                grid_node.elements.append(node.node_id)
                grid_node.number_of_elements += 1
                if node.activity_type:
                    grid_node.activity_type.append(node.activity_type)
                if node.ctrl_type:
                    grid_node.ctrl_type.append(node.ctrl_type)
                if node.node_type:
                    grid_node.node_type.append(node.node_type)
                if node.poi_id:
                    grid_node.poi_id.append(node.poi_id)
            else:
                node_dict_[node.node_id]=node

        if grid_node.number_of_elements > 0:
            grid_node.cell_id = cell_id
            grid_node.node_id=cell_id
            for node_id in grid_node.elements:
                net.node_dict[node_id].cell_id = cell_id
            net.grid_node_dict[cell_id] = grid_node
            cell_id += 1

        node_dict = node_dict_

    print("%s valid grid_cells were generated"%len(net.grid_node_dict))

def _match_links(net):
    # establish the mapping between macro links and micro links
    link_id=0
    all_grid_link={}
    for link in net.link_list:
        from_node=net.node_dict[link.from_node_id]
        to_node=net.node_dict[link.to_node_id]
        from_cell=net.grid_node_dict[from_node.cell_id]
        to_cell=net.grid_node_dict[to_node.cell_id]
        link_type_name=link.link_type_name
        link_type=link.link_type
        from_cell.modes.append(link_type_name)
        to_cell.modes.append(link_type_name)
        if from_cell.cell_id!=to_cell.cell_id:
            if (from_cell.cell_id,to_cell.cell_id,link_type) not in all_grid_link:
                grid_link=GridLink()
                grid_link.link_id=link_id
                grid_link.from_node_id = from_cell.node_id
                grid_link.to_node_id = to_cell.node_id
                grid_link.from_cell_id=from_cell.cell_id
                grid_link.to_cell_id=to_cell.cell_id
                grid_link.link_type_name=link_type_name
                grid_link.link_type=link_type
                grid_link.geometry=geometry.LineString([(from_cell.x_coord,from_cell.y_coord),
                                                   (to_cell.x_coord,to_cell.y_coord)])
                all_grid_link[from_cell.cell_id,to_cell.cell_id,link_type]=link_id
                link.grid_link_id=link_id
                link_id += 1
            else:
                link_id_=all_grid_link[from_cell.cell_id,to_cell.cell_id,link_type]
                link.grid_link_id=link_id_
                grid_link=net.grid_link_dict[link_id_]
            if link.length:
                grid_link.length_list.append(link.length)
            if link.lanes:
                grid_link.lanes_list.append(link.lanes)
            if link.free_speed:
                grid_link.free_speed_list.append(link.free_speed)
            if link.capacity:
                grid_link.capacity_list.append(link.capacity)
            if link.allowed_uses:
                grid_link.allowed_uses.extend(link.allowed_uses)
            grid_link.number_of_links+=1

            net.grid_link_dict[grid_link.link_id] = grid_link

    print("%s valid grid_links were generated" % len(net.grid_link_dict))


def partition_grid(net,n_grids=None,s_grids=None,level=None):
    """
    Uers can choose one of the bellow three parameters to simplify GMNS network (n_grids or s_girds or level).
    :param net: GMNS Network. The network needs to be simplified
    :param n_grids: tuple(int,int). The number of grids to simplify GMNS network
    :param s_grids: tuple(float,float). The size of gris to simplify GMNS network
    :param level: int [1,6]. The level to quickly simplify network
    :return: network
    """
    if n_grids:
        _create_cells_by_n_grids(net,n_grids)
        _match_nodes(net)
        _match_links(net)
    elif s_grids:
        _create_cells_by_s_grids(net,s_grids)
        _match_nodes(net)
        _match_links(net)
    elif level:
        if level<1:
            level=1
        elif level>len(Default_Simplification_Level):
            level=len(Default_Simplification_Level)
        s_grids=(Default_Simplification_Level[level-1],Default_Simplification_Level[level-1])
        _create_cells_by_s_grids(net, s_grids)
        _match_nodes(net)
        _match_links(net)
