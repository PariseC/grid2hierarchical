import csv
import os


def save_network(network, output_folder='csvfile', enconding=None):
    if output_folder:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        mic_node_filepath = os.path.join(output_folder, 'node.csv')
        mic_link_filepath = os.path.join(output_folder, 'link.csv')
        mac_node_filepath = os.path.join(output_folder, 'mac_node.csv')
        mac_link_filepath = os.path.join(output_folder, 'mac_link.csv')
    else:
        mic_node_filepath = 'node.csv'
        mic_link_filepath = 'link.csv'
        mac_node_filepath = 'mac_node.csv'
        mac_link_filepath = 'mac_link.csv'

    try:
        if enconding is None:
            outfile = open(mic_node_filepath, 'w', newline='', errors='ignore')
        else:
            outfile = open(mic_node_filepath, 'w', newline='', errors='ignore', encoding=enconding)

        write = csv.writer(outfile)
        write.writerow(['name', 'node_id', 'osm_node_id', 'osm_highway', 'zone_id', 'ctrl_type', 'node_type',
                        'activity_type','is_boundary','x_coord', 'y_coord', 'main_node_id','poi_id','notes',
                        'cell_id'])
        mic_nodes_sort=sorted(network.mic_node_dict.keys())
        for id in mic_nodes_sort:
            node=network.mic_node_dict[id]
            line = [node.name,node.node_id,node.osm_node_id,node.osm_highway,node.zone_id,node.ctrl_type,
                    node.node_type,node.activity_type,node.is_boundary,node.x_coord,node.y_coord,node.main_node_id,
                    node.poi_id,node.notes,node.cell_id]
            write.writerow(line)
        outfile.close()

    except PermissionError:
        print('node.csv may be locked by other programs. please release it then try again')

    try:
        if enconding is None:
            outfile = open(mic_link_filepath, 'w', newline='', errors='ignore')
        else:
            outfile = open(mic_link_filepath, 'w', newline='', errors='ignore', encoding=enconding)

        write = csv.writer(outfile)
        write.writerow(['name', 'link_id', 'osm_way_id', 'from_node_id', 'to_node_id','dir_flag','length',
                        'lanes','free_speed','capacity','link_type_name','link_type','geometry','allowed_uses',
                        'from_biway','is_link','VDF_FFTT1','VDF_cap1','macro_link_id'])
        for  link in network.mic_link_list:
            line = [link.name, link.link_id, link.osm_way_id, link.from_node_id, link.to_node_id,link.dir_flag,
                    link.length,link.lanes,link.free_speed,link.capacity,link.link_type_name,link.link_type,
                    link.geometry.wkt,link.allowed_uses,link.from_biway,link.is_link,link.VDF_FFTT1,link.VDF_cap1,
                    link.mac_link_id]
            write.writerow(line)
        outfile.close()
    except PermissionError:
        print('link.csv may be locked by other programs. please release it then try again')

    try:
        if enconding is None:
            outfile = open(mac_node_filepath, 'w', newline='', errors='ignore')
        else:
            outfile = open(mac_node_filepath, 'w', newline='', errors='ignore', encoding=enconding)

        write = csv.writer(outfile)
        write.writerow(['name', 'cell_id', 'elements', 'number_of_element','activity_type','ctrl_type', 'node_type',
                        'poi_id','x_coord','y_coord','boundary'])
        mac_nodes_sort=sorted(network.mac_node_dict.keys())
        for id in mac_nodes_sort:
            node=network.mac_node_dict[id]
            element=';'.join([str(id) for id in node.element]) if len(node.element)>0 else ''
            activity_type=';'.join(node.activity_type) if len(node.activity_type)>0 else ''
            ctrl_type=';'.join(node.ctrl_type) if len(node.ctrl_type)>0 else ''
            node_type=';'.join(node.node_type) if len(node.node_type)>0 else ''
            poi_id=';'.join(str(id) for id in node.poi_id) if len(node.poi_id)>0 else ''
            line=[node.name,node.cell_id,element,node.num_element,activity_type,ctrl_type,
                  node_type,poi_id,node.x_coord,node.y_coord,node.boundary.wkt]
            write.writerow(line)
        outfile.close()
    except PermissionError:
        print('mac_node.csv may be locked by other programs. please release it then try again')

    try:
        if enconding is None:
            outfile = open(mac_link_filepath, 'w', newline='', errors='ignore')
        else:
            outfile = open(mac_link_filepath, 'w', newline='', errors='ignore', encoding=enconding)

        write = csv.writer(outfile)
        write.writerow(['name', 'link_id', 'from_cell_id', 'to_cell_id', 'length','lanes', 'free_speed', 'capacity',
                        'geometry', 'allowed_uses', 'number_of_micro_link'])
        mac_links_sort=sorted(network.mac_link_dict.keys())
        for id in mac_links_sort:
            link=network.mac_link_dict[id]
            lanes=sum(link.lanes_list)/len(link.lanes_list) if len(link.lanes_list) else ''
            free_speed=sum(link.free_speed_list)/len(link.free_speed_list) if len(link.free_speed_list) else ''
            capacity=sum(link.capacity_list)/len(link.capacity_list) if len(link.capacity_list) else ''
            length=sum(link.length_list)/len(link.length_list) if len(link.length_list) else ''
            allowed_uses=set(link.allowed_uses)
            allowed_uses=';'.join(allowed_uses) if len(allowed_uses)>0 else ''

            line = [link.name, link.link_id, link.from_cell_id, link.to_cell_id,length, lanes, free_speed,capacity,
                    link.geometry.wkt,allowed_uses,link.number_of_miclink]
            write.writerow(line)
        outfile.close()
    except PermissionError:
        print('mac_link.csv may be locked by other programs. please release it then try again')