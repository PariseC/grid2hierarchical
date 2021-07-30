import csv
import os


def save_network(network, output_folder='./', enconding=None):
    output_folder=os.path.join(output_folder,'grid_network')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    node_filepath = os.path.join(output_folder, 'node.csv')
    link_filepath = os.path.join(output_folder, 'link.csv')
    grid_node_filepath = os.path.join(output_folder, 'grid_node.csv')
    grid_link_filepath = os.path.join(output_folder, 'grid_link.csv')


    try:
        if enconding is None:
            outfile = open(node_filepath, 'w', newline='', errors='ignore')
        else:
            outfile = open(node_filepath, 'w', newline='', errors='ignore', encoding=enconding)

        write = csv.writer(outfile)
        write.writerow(['name', 'node_id', 'osm_node_id', 'osm_highway', 'zone_id', 'ctrl_type', 'node_type',
                        'activity_type','is_boundary','x_coord', 'y_coord', 'main_node_id','poi_id','notes',
                        'cell_id'])
        nodes_sort=sorted(network.node_dict.keys())
        for id in nodes_sort:
            node=network.node_dict[id]
            line = [node.name,node.node_id,node.osm_node_id,node.osm_highway,node.zone_id,node.ctrl_type,
                    node.node_type,node.activity_type,node.is_boundary,node.x_coord,node.y_coord,node.main_node_id,
                    node.poi_id,node.notes,node.cell_id]
            write.writerow(line)
        outfile.close()

    except PermissionError:
        print('node.csv may be locked by other programs. please release it then try again')

    try:
        if enconding is None:
            outfile = open(link_filepath, 'w', newline='', errors='ignore')
        else:
            outfile = open(link_filepath, 'w', newline='', errors='ignore', encoding=enconding)

        write = csv.writer(outfile)
        write.writerow(['name', 'link_id', 'osm_way_id', 'from_node_id', 'to_node_id','dir_flag','length',
                        'lanes','free_speed','capacity','link_type_name','link_type','geometry','allowed_uses',
                        'from_biway','is_link','VDF_FFTT1','VDF_cap1','grid_link_id'])
        for  link in network.link_list:
            line = [link.name, link.link_id, link.osm_way_id, link.from_node_id, link.to_node_id,link.dir_flag,
                    link.length,link.lanes,link.free_speed,link.capacity,link.link_type_name,link.link_type,
                    link.geometry.wkt,link.allowed_uses,link.from_biway,link.is_link,link.VDF_FFTT1,link.VDF_cap1,
                    link.grid_link_id]
            write.writerow(line)
        outfile.close()
    except PermissionError:
        print('link.csv may be locked by other programs. please release it then try again')

    try:
        if enconding is None:
            outfile = open(grid_node_filepath, 'w', newline='', errors='ignore')
        else:
            outfile = open(grid_node_filepath, 'w', newline='', errors='ignore', encoding=enconding)

        write = csv.writer(outfile)
        write.writerow(['node_id','cell_id', 'elements', 'number_of_elements','activity_type','ctrl_type', 'node_type',
                        'poi_id','mode','x_coord','y_coord','geometry'])
        grid_nodes_sort=sorted(network.grid_node_dict.keys())
        for id in grid_nodes_sort:
            node=network.grid_node_dict[id]
            elements=';'.join([str(id) for id in node.elements]) if len(node.elements)>0 else ''
            activity_type=';'.join(node.activity_type) if len(node.activity_type)>0 else ''
            ctrl_type=';'.join(node.ctrl_type) if len(node.ctrl_type)>0 else ''
            node_type=';'.join(node.node_type) if len(node.node_type)>0 else ''
            poi_id=';'.join(str(id) for id in node.poi_id) if len(node.poi_id)>0 else ''
            modes=';'.join(set(node.modes))
            line=[node.node_id,node.cell_id,elements,node.number_of_elements,activity_type,ctrl_type,
                  node_type,poi_id,modes,node.x_coord,node.y_coord,node.geometry.wkt]
            write.writerow(line)
        outfile.close()
    except PermissionError:
        print('grid_node.csv may be locked by other programs. please release it then try again')

    try:
        if enconding is None:
            outfile = open(grid_link_filepath, 'w', newline='', errors='ignore')
        else:
            outfile = open(grid_link_filepath, 'w', newline='', errors='ignore', encoding=enconding)

        write = csv.writer(outfile)
        write.writerow(['link_id','from_node_id', 'to_node_id',  'from_cell_id', 'to_cell_id', 'length','lanes',
                        'link_type_name','link_type','free_speed', 'capacity','geometry', 'allowed_uses',
                        'number_of_links'])
        grid_links_sort=sorted(network.grid_link_dict.keys())
        for id in grid_links_sort:
            link=network.grid_link_dict[id]
            lanes=sum(link.lanes_list)/len(link.lanes_list) if len(link.lanes_list) else ''
            free_speed=sum(link.free_speed_list)/len(link.free_speed_list) if len(link.free_speed_list) else ''
            capacity=sum(link.capacity_list)/len(link.capacity_list) if len(link.capacity_list) else ''
            length=sum(link.length_list)/len(link.length_list) if len(link.length_list) else ''
            allowed_uses=set(link.allowed_uses)
            allowed_uses=';'.join(allowed_uses) if len(allowed_uses)>0 else ''

            line = [link.link_id,link.from_node_id, link.to_node_id, link.from_cell_id, link.to_cell_id,length, lanes,
                    link.link_type_name,link.link_type, free_speed,capacity,
                    link.geometry.wkt,allowed_uses,link.number_of_links]
            write.writerow(line)
        outfile.close()
    except PermissionError:
        print('grid_link.csv may be locked by other programs. please release it then try again')