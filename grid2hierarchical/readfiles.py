import csv
import os
import sys
from .classes import *
from .setting import *
from itertools import islice
from shapely.wkt import loads
from shapely.geometry import Point
def read_gmns_network_from_csv(input_folder):
    network=Network()
    if input_folder:
        node_file = os.path.join(input_folder, 'node.csv')
        link_file = os.path.join(input_folder, 'link.csv')
    else:
        node_file = 'node.csv'
        link_file = 'link.csv'
    try:
        with open(node_file,'r') as f:
            node_reader=csv.DictReader(f)
            x_coord_list=[]
            y_coord_list=[]
            for row in islice(node_reader, 0, None):
                key=row.keys()
                node=MicNode()
                node.node_id = int(row['node_id']) if 'node_id' in key else None
                node.name = row['name'] if 'name' in key else ''
                node.osm_node_id = row['osm_node_id'] if 'osm_node_id' in key else ''
                node.osm_highway = row['osm_highway'] if 'osm_highway' in key else ''
                node.zone_id = row['zone_id'] if 'zone_id' in key else ''
                node.ctrl_type = row['ctrl_type'] if 'ctrl_type' in key else ''
                node.node_type = row['node_type'] if 'node_type' in key else ''
                node.activity_type = row['activity_type'] if 'activity_type' in key else ''
                node.is_boundary = row['is_boundary'] if 'is_boundary' in key else ''
                node.x_coord = float(row['x_coord']) if 'x_coord' in key else ''
                node.y_coord = float(row['y_coord']) if 'y_coord' in key else ''
                node.main_node_id = row['main_node_id'] if 'main_node_id' in key else ''
                node.poi_id = row['poi_id'] if 'poi_id' in key else ''
                node.notes = row['notes'] if 'notes' in key else ''
                if node.x_coord and node.y_coord:
                    node.geometry=Point(node.x_coord,node.y_coord)
                    if node.node_id is not None:
                        network.mic_node_dict[node.node_id]=node
                        x_coord_list.append(node.x_coord)
                        y_coord_list.append(node.y_coord)
            network.min_x_coord=min(x_coord_list)-(abs(min(x_coord_list))*Coordinate_Extend_Scale)
            network.max_x_coord=max(x_coord_list)+(abs(max(x_coord_list))*Coordinate_Extend_Scale)
            network.min_y_coord=min(y_coord_list)-(abs(min(y_coord_list))*Coordinate_Extend_Scale)
            network.max_y_coord=max(y_coord_list)+(abs(max(y_coord_list))*Coordinate_Extend_Scale)
            # network.min_x_coord,network.max_x_coord=min(x_coord_list),max(x_coord_list)
            # network.min_y_coord,network.max_y_coord=min(y_coord_list),max(y_coord_list)
    except Exception as e:
        print(e)
        print(row)
        sys.exit(0)
    try:
        with open(link_file, 'r') as f:
            link_reader = csv.DictReader(f)
            for row in islice(link_reader, 0, None):
                key=row.keys()
                link=MicLink()
                link.name =row['name'] if 'name' in key else ''
                link.link_id = row['link_id'] if 'link_id' in key else ''
                link.osm_way_id = row['osm_way_id'] if 'osm_way_id' in key else ''
                link.from_node_id = int(row['from_node_id']) if 'from_node_id' in key else ''
                link.to_node_id = int(row['to_node_id']) if 'to_node_id' in key else ''
                link.dir_flag = row['dir_flag'] if 'dir_flag' in key else ''
                try:
                    link.length = float(row['length'])
                except:
                    link.length=''
                try:
                    link.lanes = float(row['lanes'])
                except:
                    link.lanes=''
                try:
                    link.free_speed = float(row['free_speed'])
                except:
                    link.free_speed=''
                try:
                    link.capacity = float(row['capacity'])
                except:
                    link.capacity=''
                link.link_type_name = row['link_type_name'] if 'link_type_name' in key else ''
                link.link_type = row['link_type'] if 'link_type' in key else ''
                link.geometry = loads(row['geometry']) if 'geometry' in key else ''
                link.allowed_uses = row['allowed_uses'].split(';') if 'allowed_uses' in key else ''
                link.from_biway = row['from_biway'] if 'from_biway' in key else ''
                link.is_link = row['is_link'] if 'is_link' in key else ''
                try:
                    link.VDF_FFTT1 = float(row['VDF_FFTT1'])
                except:
                    link.VDF_FFTT1=''
                try:
                    link.VDF_cap1 = float(row['VDF_cap1'])
                except:
                    link.VDF_cap1=''
                if link.from_node_id is not None and link.to_node_id is not None:
                    network.mic_link_list.append(link)
                else:
                    print("warning: link id=%s is ignored" % link.link_id)

    except Exception as e:
        print(e)
        print(row)
        sys.exit(0)
    print("%s mic_nodes were read"%len(network.mic_node_dict))
    print("%s mic_links were read"%len(network.mic_link_list))
    return network