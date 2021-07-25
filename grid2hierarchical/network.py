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
            mac_node=MacNode()
            mac_node.cell_id=cell_id

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
            mac_node.boundary=geometry.Polygon(bounds)
            mac_node.geometry=mac_node.boundary.centroid
            mac_node.x_coord=round((left_bottom_x+right_bottom_x)/2,Coordinate_Precision)
            mac_node.y_coord=round((left_bottom_y+left_top_y)/2,Coordinate_Precision)
            net.mac_node_dict[mac_node.cell_id]=mac_node
            cell_id+=1

def _create_cells_by_s_grids(net,s_grids):
    cell_width = s_grids[0]
    cell_height = s_grids[1]
    cell_id = 0
    left_bottom_x_=net.min_x_coord

    while left_bottom_x_<=net.max_x_coord:
        left_bottom_y_ = net.min_y_coord
        while left_bottom_y_<=net.max_y_coord:
            mac_node = MacNode()
            mac_node.cell_id = cell_id

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
            mac_node.boundary = geometry.Polygon(bounds)
            mac_node.geometry = mac_node.boundary.centroid
            mac_node.x_coord = round((left_bottom_x + right_bottom_x) / 2, Coordinate_Precision)
            mac_node.y_coord = round((left_bottom_y + left_top_y) / 2, Coordinate_Precision)
            net.mac_node_dict[mac_node.cell_id] = mac_node
            cell_id += 1
            left_bottom_y_=left_bottom_y_+cell_height
        left_bottom_x_=left_bottom_x_+cell_width

def _simplify_mic_nodes(net):
    #establish the mapping between macro nodes and micro nodes
    mic_node_dict = copy.deepcopy(net.mic_node_dict)
    mac_node_dict=copy.deepcopy(net.mac_node_dict)
    net.mac_node_dict={}
    cell_id = 0
    for _,mac_node in mac_node_dict.items():
        x_min, y_min, x_max, y_max = mac_node.boundary.bounds
        mic_node_dict_={}
        for _,mic_node in mic_node_dict.items():
            if x_min <= mic_node.x_coord <= x_max and y_min <= mic_node.y_coord <= y_max:
                # if mic_node.geometry.within(mac_node.boundary):
                mac_node.element.append(mic_node.node_id)
                mac_node.num_element += 1
                if mic_node.activity_type:
                    mac_node.activity_type.append(mic_node.activity_type)
                if mic_node.ctrl_type:
                    mac_node.ctrl_type.append(mic_node.ctrl_type)
                if mic_node.node_type:
                    mac_node.node_type.append(mic_node.node_type)
                if mic_node.poi_id:
                    mac_node.poi_id.append(mic_node.poi_id)
            else:
                mic_node_dict_[mic_node.node_id]=mic_node

        if mac_node.num_element > 0:
            mac_node.cell_id = cell_id
            for mic_node_id in mac_node.element:
                net.mic_node_dict[mic_node_id].cell_id = cell_id
            net.mac_node_dict[cell_id] = mac_node
            cell_id += 1

        mic_node_dict = mic_node_dict_

    # delete the empty cells
    # mac_node_dict=copy.deepcopy(net.mac_node_dict)
    # net.mac_node_dict={}
    # cell_id=0
    # for _,mac_node in mac_node_dict.items():
    #     if mac_node.num_element>0:
    #         mac_node.cell_id=cell_id
    #         for mic_node_id in mac_node.element:
    #             net.mic_node_dict[mic_node_id].cell_id=cell_id
    #         net.mac_node_dict[cell_id]=mac_node
    #         cell_id+=1
    print("%s valid mac_cells were generated"%len(net.mac_node_dict))

def _simplify_mic_links(net):
    # establish the mapping between macro links and micro links
    link_id=0
    all_mac_link={}
    for mic_link in net.mic_link_list:
        from_node=net.mic_node_dict[mic_link.from_node_id]
        to_node=net.mic_node_dict[mic_link.to_node_id]
        from_cell=net.mac_node_dict[from_node.cell_id]
        to_cell=net.mac_node_dict[to_node.cell_id]
        if from_cell.cell_id!=to_cell.cell_id:
            if (from_cell.cell_id,to_cell.cell_id) not in all_mac_link:
                mac_link=MacLink()
                mac_link.link_id=link_id
                mac_link.from_cell_id=from_cell.cell_id
                mac_link.to_cell_id=to_cell.cell_id
                mac_link.geometry=geometry.LineString([(from_cell.x_coord,from_cell.y_coord),
                                                   (to_cell.x_coord,to_cell.y_coord)])
                all_mac_link[from_cell.cell_id,to_cell.cell_id]=link_id
                mic_link.mac_link_id=link_id
                link_id += 1
            else:
                link_id_=all_mac_link[from_cell.cell_id,to_cell.cell_id]
                mac_link=net.mac_link_dict[link_id_]
            if mic_link.length:
                mac_link.length_list.append(mic_link.length)
            if mic_link.lanes:
                mac_link.lanes_list.append(mic_link.lanes)
            if mic_link.free_speed:
                mac_link.free_speed_list.append(mic_link.free_speed)
            if mic_link.capacity:
                mac_link.capacity_list.append(mic_link.capacity)
            if mic_link.allowed_uses and mic_link.allowed_uses not in mac_link.allowed_uses:
                mac_link.allowed_uses.append(mic_link.allowed_uses)
            mac_link.number_of_miclink+=1

            net.mac_link_dict[mac_link.link_id] = mac_link

    print("%s valid mac_links were generated" % len(net.mac_link_dict))


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
        _simplify_mic_nodes(net)
        _simplify_mic_links(net)
    elif s_grids:
        _create_cells_by_s_grids(net,s_grids)
        _simplify_mic_nodes(net)
        _simplify_mic_links(net)
    elif level:
        if level<1:
            level=1
        elif level>len(Default_Simplification_Level):
            level=len(Default_Simplification_Level)
        s_grids=(Default_Simplification_Level[level-1],Default_Simplification_Level[level-1])
        _create_cells_by_s_grids(net, s_grids)
        _simplify_mic_nodes(net)
        _simplify_mic_links(net)
