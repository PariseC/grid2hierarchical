
class MicNode():
    def __init__(self):
        self.node_id=None
        self.name=None
        self.osm_node_id=None
        self.osm_highway=None
        self.zone_id=None
        self.ctrl_type=None
        self.node_type=None
        self.activity_type=None
        self.is_boundary=None
        self.x_coord=None
        self.y_coord=None
        self.main_node_id=None
        self.poi_id=None
        self.notes=None
        self.geometry=None
        self.cell_id=0

class MicLink():
    def __init__(self):
        self.name=None
        self.link_id=None
        self.osm_way_id=None
        self.from_node_id=None
        self.to_node_id=None
        self.dir_flag=None
        self.length=None
        self.lanes=None
        self.free_speed=None
        self.capacity=None
        self.link_type_name=None
        self.link_type=None
        self.geometry=None
        self.allowed_uses=None
        self.from_biway=None
        self.is_link=None
        self.VDF_FFTT1=None
        self.VDF_cap1=None
        self.mac_link_id=0

class MacNode():
    def __init__(self):
        self.name=''
        self.cell_id=0
        self.element=[]
        self.num_element=0
        self.activity_type=[]
        self.ctrl_type=[]
        self.node_type=[]
        self.poi_id=[]
        self.geometry=None
        self.x_coord=None
        self.y_coord=None
        self.boundary=None

class MacLink():
    def __init__(self):
        self.name=''
        self.link_id=0
        self.from_cell_id=0
        self.to_cell_id=0
        self.length_list=[]
        self.lanes_list=[]
        self.free_speed_list=[]
        self.capacity_list=[]
        self.geometry=None
        self.allowed_uses=[]
        self.number_of_miclink=0

class Network():
    def __init__(self):
        self.mic_node_dict={}
        self.mic_link_list=[]

        self.mac_node_dict={}
        self.mac_link_dict={}

        self.min_x_coord=-180
        self.min_y_coord=-90
        self.max_x_coord=180
        self.max_y_coord=90




