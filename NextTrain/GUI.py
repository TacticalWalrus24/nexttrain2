from tkinter import *
import collections
import math
from decimal import *
from typing import *
from PIL import Image, ImageTk
import pymysql
connection = pymysql.connect(host="localhost", user="root", passwd="", database="nexttrain2")
cursor = connection.cursor()

def clean_database():
    command = "DELETE FROM `platforms` WHERE 1"
    cursor.commit(command)
    command = "DELETE FROM `rail` WHERE 1"
    cursor.commit(command)
    command = "DELETE FROM `rail_connections` WHERE 1"
    cursor.commit(command)
    command = "DELETE FROM `route` WHERE 1"
    cursor.commit(command)
    command = "DELETE FROM `route_station` WHERE 1"
    cursor.commit(command)
    command = "DELETE FROM `stations` WHERE 1"
    cursor.commit(command)

def dat_update_station(station):
    retrive = f"SELECT ID FROM stations"
    cursor.execute(retrive)
    stationID = [x[0] for x in cursor.fetchall()]
    match = False
    for sid in stationID:
        if station.ID == sid:
            write = f"UPDATE `stations` SET `Name`='{station.get_name()}',`Network`='{station.network}',`isStation`='{station.widget_class.is_station}' WHERE `ID` = '{station.ID}'"
            cursor.execute(write)
            match = True
            break
    if not match:
        write = f"INSERT INTO `stations` (`ID`, `Name`, `Network`, `isStation`) VALUES ('{station.ID}', '{station.get_name()}', '{station.network}', '{station.widget_class.is_station}')"
        cursor.execute(write)

def dat_update_rail(rail):
    retrive = f"SELECT ID FROM rail"
    cursor.execute(retrive)
    railID = [x[0] for x in cursor.fetchall()]
    match = False
    for rid in railID:
        if rail.ID == rid:
            write = f"UPDATE `rail` SET `length`='{rail.length}', `width`='{rail.width}'  WHERE `ID` = '{rail.ID}'"
            cursor.execute(write)
            match = True
            break
    if not match:
        write = f"INSERT INTO `rail` (`ID`, `network`, `length`, `width`) VALUES ('{rail.ID}', '{rail.network}', '{rail.length}', '{rail.width}')"
        cursor.execute(write)

def dat_update_railcon(rail):

    for c in rail.connections:
        write = f"INSERT INTO `rail_connections` (`railID`, `stationID`) VALUES ('{rail.ID}', '{c.station.ID}')"
        cursor.execute(write)

def dat_update_route(route):
    retrive = f"SELECT ID FROM route"
    cursor.execute(retrive)
    routeID = [x[0] for x in cursor.fetchall()]
    match = False
    for rid in routeID:
        if route.ID == rid:
            match = True
            break
    if not match:
        write = f"INSERT INTO `route` (`ID`, `network`) VALUES ('{route.ID}', '{route.network}')"
        cursor.execute(write)

def dat_update_route_station(route):
    retrive = f"SELECT 'ID' FROM `route_station`"
    cursor.execute(retrive)
    routeID = [x[0] for x in cursor.fetchall()]
    match = False
    for rid in routeID:
        if route.ID == rid:
            match = True
            break
    if not match:
        for s in route.stations:
            write = f"INSERT INTO `route_station` (`LineID`, `StationID`, `stopNumber`) VALUES ('{route.ID}', '{s.station.ID}', '{route.stations.index(s)}')"
            cursor.execute(write)

def dat_load_station(network):
    retrive = f"SELECT * FROM stations WHERE Network = '{network}'"
    cursor.execute(retrive)
    rows = [x[0] for x in cursor.fetchall()]
    for r in rows:
        if r[4]:
            create_station(0)
            for s in stations:
                if r[0] == s.station.ID:
                    retrive = f"SELECT * FROM platforms WHERE stationID = '{r[0]}'"
                    cursor.execute(retrive)
                    platform = [x[0] for x in cursor.fetchall()]
                    s.station.set_data(r[1], platform)

def dat_load_rails(network):
    retrive = f"SELECT * FROM `rail` WHERE 'Network' = '{network}'"
    cursor.execute(retrive)
    rows = [x[0] for x in cursor.fetchall()]
    for r in rows:
        retrive = f"SELECT 'StationID' FROM `rail_connections` WHERE 'railID' = '{r[0]}'"
        cursor.execute(retrive)
        connections = [x[0] for x in cursor.fetchall()]
        global clicknumber
        clicknumber=0
        for c in connections:
            for s in stations:
                if c[0] == s.ID:
                    connect_rails(s.widget_class, s.widget_class)

def dat_load_route(network):
    retrive = f"SELECT * FROM `rail` WHERE 'Network' = '{network}'"
    cursor.execute(retrive)
    rows = [x[0] for x in cursor.fetchall()]


networkName = "Testville"

def connect_rails(widget_class, event):
    global clicknumber
    global class1
    global widget1
    if clicknumber==0:
        widget1 = event.widget
        class1 = widget_class
        clicknumber+=1
    else:
        widget2 = event.widget
        station2 = widget_class.station
        x1 = widget1.winfo_x() + widget1.winfo_width()/2
        y1 = widget1.winfo_y() + widget1.winfo_height()/2
        x2 = widget2.winfo_x() + widget2.winfo_width()/2
        y2 = widget2.winfo_y() + widget2.winfo_height()/2
        connector = cvs_map.create_line(x1,y1,x2,y2,fill='black',width=10)
        con = [class1, widget_class]
        rail = Rail(networkName,con,connector)
        dat_update_rail(rail)
        dat_update_railcon(rail)
        rails.append(rail)
        widget_class.rail.append(rail)
        class1.rail.append(rail)
        widget_class.connected = True
        class1.connected = True
        widget1 = event.widget
        class1 = widget_class

# #region widgets
class Widgets:
    def open_rail(self, event):
        print("clicked on rail")
    # #region Dragging code
    def make_draggable(self, widget):
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        global clicknumber
        if not joining and not route_join:
            widget = event.widget
            widget._drag_start_x = event.x
            widget._drag_start_y = event.y
            clicknumber = 0
        elif not route_join:
            connect_rails(self, event)
        elif route_join:
            global route_stations
            if not event.widget in route_stations:
                route_stations.append(self)
                event.widget.configure(bg="yellow")
    clicknumber = 0

    def on_drag_motion(self, event):
        if not joining:
            widget = event.widget
            x = widget.winfo_x() - widget._drag_start_x + event.x
            y = widget.winfo_y() - widget._drag_start_y + event.y
            if self.connected:
                side = 0
                for r in self.rail:
                    for c in r.connections:
                        if c == self:
                            side = r.connections.index(c)
                    if side == 0:
                        cvs_map.coords(r.widget, x + widget.winfo_width()/2, y + widget.winfo_height()/2, cvs_map.coords(r.widget)[2], cvs_map.coords(r.widget)[3])
                    else:
                        cvs_map.coords(r.widget, cvs_map.coords(r.widget)[0], cvs_map.coords(r.widget)[1], x + widget.winfo_width()/2, y + widget.winfo_height()/2)
            widget.place(x=x, y=y)

#    class DragDropMixin:
#        def __init__(self, *args, **kwargs):
#            super().__init__(*args, **kwargs)
#
#            make_draggable(self)
#
#    class DnDFrame(DragDropMixin, Frame):
#        pass
    # #endregion

    def update_station(self, name, platforms, menu):
        self.station.set_data(name, platforms)
        menu.wm_title(f"{self.station.name}")
        dat_update_station(self.station)

    def update_rails(self, length, width):
        index = 0
        for r in self.rail:
            r.set_data(length[index].get(), width[index].get())
            dat_update_rail(r)
            index += 1

    def rail_menu(self, window, i):
        menu = window
        fr_rail_field = Frame(menu, width =200, height=400, bg="whitesmoke")
        fr_rail_field.grid(row=i, column=0, sticky="nsew")

        lbl_header = Label(fr_rail_field, text="Rails", bg="whitesmoke")
        lbl_header.grid(row=0, column=0, sticky="")
        index = 1
        ent_length = []
        ent_width = []
        for r in self.rail:
            for c in r.connections:
                if c != self:
                    lbl_rail = Label(fr_rail_field, text=f"Rail to {c.station.get_name()}", bg="whitesmoke")
                    lbl_rail.grid(row=index, column=0, sticky="ne")
                    index += 1
                    lbl_length = Label(fr_rail_field, text="Rail Length (minutes): ", bg="whitesmoke")
                    temp_length = Entry(fr_rail_field)
                    lbl_width = Label(fr_rail_field, text="Number of rails: ", bg="whitesmoke")
                    temp_width = Entry(fr_rail_field)
                    ent_length.append(temp_length)
                    ent_width.append(temp_width)
                    temp_index = ent_length.index(temp_length)
                    ent_length[temp_index].insert(0, f"{r.length}")
                    ent_width[temp_index].insert(0, f"{r.width}")
                    lbl_length.grid(row=index, column=0, sticky="ne")
                    temp_length.grid(row=index, column=1, sticky="nw")
                    index += 1
                    lbl_width.grid(row=index, column=0, sticky="ne")
                    temp_width.grid(row=index, column=1, sticky="nw")
                    index += 1
        return ent_length, ent_width

    def open_widget_menu(self, event):
        menu = Toplevel()
        menu.wm_title(f"{self.station.get_name()}")
        menu.rowconfigure(0, minsize=20, weight=1)
        menu.columnconfigure(0, minsize=20, weight=1)
        i = 0
        if self.is_station:
            fr_station_field = Frame(menu, width =200, height=400, bg="white")
            fr_station_field.grid(row=i, column=0, sticky="nsew")
            i+=1

            lbl_name = Label(fr_station_field, text="Station Name: ", bg="white")
            ent_name = Entry(fr_station_field)
            ent_name.insert(0, f"{self.station.name}")
            lbl_name.grid(row=0, column=0, sticky="ne")
            ent_name.grid(row=0, column=1, sticky="nw")

            lbl_ID = Label(fr_station_field, text="Station ID: ", bg="white")
            lbl_IDname = Label(fr_station_field, text=f"{self.station.ID}", bg="white")
            lbl_ID.grid(row=1, column=0, sticky="ne")
            lbl_IDname.grid(row=1, column=1, sticky="nw")

            lbl_platforms = Label(fr_station_field, text="Number of platforms: ", bg="white")
            ent_platforms = Entry(fr_station_field)
            ent_platforms.insert(0, f"{self.station.platforms}")
            lbl_platforms.grid(row=2, column=0, sticky="ne")
            ent_platforms.grid(row=2, column=1, sticky="nw")

            if len(schedules) > 0:
                fr_schedule = Frame(menu, width =200, height=400, bg="white")
                fr_schedule.grid(row=i, column=0, sticky="nsew")
                i+=1
                j=0
                for s in schedules:
                    if self in s.stops:
                        lbl_arrival = Label(fr_schedule, text=f"{s.route.name}: ", bg="white")
                        lbl_time = Label(fr_schedule, text=f"{s.stops[self]}", bg="white")
                        lbl_arrival.grid(row=j, column=0, sticky="nw")
                        lbl_time.grid(row=j, column=1, sticky="nw")
                        j+=1

        fr_submit_field = Frame(menu, width =200, height=400, bg="white")
        btn_submit = Button(fr_submit_field, text="Submit")
        if len(self.rail) > 0:
            temp = self.rail_menu(menu, i)
            i+=1
            length = temp[0]
            width = temp[1]
            if self.is_station:
                btn_submit.configure(command = lambda:[self.update_station(ent_name.get(), int(ent_platforms.get()), menu), self.update_rails(length, width)])
            else:
                btn_submit.configure(command = lambda:self.update_rails(length, width))
        elif self.is_station:
            btn_submit.configure(command = lambda:self.update_station(ent_name.get(), int(ent_platforms.get()), menu))

        fr_submit_field.grid(row=i, column=0, sticky="nsew")
        #btn_submit = Button(fr_submit_field, text="Submit", command= lambda:[self.update_station(ent_name.get(), int(ent_platforms.get()), menu), self.update_rails(ent_length, ent_width)])
        btn_exit = Button(fr_submit_field, text="Exit", command=menu.destroy)
        btn_submit.grid(row=0, column=0, sticky="ne")
        btn_exit.grid(row=0, column=1, sticky="nw")

    def get_name(self):
        return self.station.get_name()

    def __init__(self, image, is_station, length):
        btn_dnd = Button(cvs_map, image = image, bg = "white", relief = FLAT)
        self.make_draggable(btn_dnd)
        btn_dnd.bind("<Double-Button-1>", self.open_widget_menu)
        self.widget = btn_dnd
        if is_station:
            self.station = Station(networkName, self)
        else:
            self.station = Junction(networkName, self)
        btn_dnd.place(x=20,y=20)
        self.connected = False
        self.rail = []
        self.is_station = is_station
        self.length = length
        dat_update_station(self.station)
# #endregion

def route_menu(route):
    menu = Toplevel()
    menu.wm_title(f"{route.name}")
    menu.rowconfigure(0, minsize=20)
    menu.columnconfigure(0, minsize=20)
    fr_info = Frame(menu, bg="white")
    fr_info.grid(row=0, column=0, sticky="nsew")
    lbl_name = Label(fr_info, text = "Route name: ", bg="white")
    ent_name = Entry(fr_info)
    ent_name.insert(0, f"{route.name}")
    lbl_name.grid(row=0, column=0, sticky="ne")
    ent_name.grid(row=0, column=1, sticky="nw")
    fr_stops = Frame(menu, bg="whitesmoke")
    lbl_stops = Label(fr_stops, text = "Stops", bg="whitesmoke")
    lbl_times = Label(fr_stops, text = "Time Since Departure", bg="whitesmoke")
    fr_stops.grid(row=1, column=0, sticky="nsew")
    lbl_stops.grid(row=0, column=0, sticky="nw")
    lbl_times.grid(row=0, column=1, sticky="nw")
    i = 1
    for s in route.stations:
        lbl_stop = Label(fr_stops, text = f"{s.get_name()}", bg="whitesmoke")
        lbl_time = Label(fr_stops, text = f"{route.times[route.path.index(s)]}", bg="whitesmoke")
        lbl_stop.grid(row=i, column=0, sticky="nw")
        lbl_time.grid(row=i, column=1, sticky="nw")
        i+=1
    i = 0
    j=2
    if len(schedules) > 0:
        fr_sched_list = Frame(menu, bg="white")
        fr_sched_list.grid(row=j, column=0, sticky="nsew")
        j+=1
        for s in schedules:
            if s.route == route:
                lbl_depart = Label(fr_sched_list, text = f"Departure at:", bg="white")
                lbl_depart.grid(row=i, column=0, sticky="nw")
                i+=1
                for st in s.stops:
                    lbl_stop = Label(fr_sched_list, text = f"{st.get_name()}", bg="white")
                    lbl_time = Label(fr_sched_list, text = f"{s.stops[st]}", bg="white")
                    lbl_stop.grid(row=i, column=0, sticky="nw")
                    lbl_time.grid(row=i, column=1, sticky="nw")
                    i+=1

    fr_schedules = Frame(menu, bg="white")
    lbl_sched = Label(fr_schedules, text = "Times (12:00, 12:30...)", bg="white")
    ent_sched = Entry(fr_schedules)
    btn_sched = Button(fr_schedules, text="Create Schedule", command=lambda:schedule(route, ent_sched.get()))
    fr_schedules.grid(row=j, column=0, sticky="nsew")
    lbl_sched.grid(row=0, column=0, sticky="nw")
    ent_sched.grid(row=0, column=1, sticky="nw")
    btn_sched.grid(row=0, column=2, sticky="nw")

def show_routes(frame):
    if len(routes) > 0:
        temp_routes = []
        toggle = True
        i = 0
        for r in routes:
            if toggle:
                r.toggle_colour("white")
                toggle = False
            else:
                r.toggle_colour("bisque")
                toggle = True
            r.frame.grid(row=i, column=0, sticky="ew")
            r.label.grid(row=0, column=0, sticky="ew")
            frame.rowconfigure(i, minsize=40)
            i += 1
        btn_route.grid(row=i, column=0)

def clear_routes(temp_routes):
    for r in temp_routes:
        r.destroy()

hidden = True
def show_schedules(frame1, frame2):
    route_nodes(0)
    join_nodes(0)
    global hidden
    temp_routes = False
    if hidden:
        frame2.grid_remove()
        frame1.grid(row=1, column=1, sticky="ns")
        temp_routes = show_routes(frame1)
        hidden = False
    else:
        frame1.grid_remove()
        frame2.grid(row=1, column=1, sticky="ns")
        hidden = True

route_stations = []

routes = []
stations = []
junctions = []
rails =[]

# #region main
# create window
window = Tk()
window.title(f"NextTrain - {networkName}")

photo = PhotoImage(file = r"images\station.png")
photoimage = photo.subsample(4, 4)
station_img = photoimage
photo = PhotoImage(file = r"images\junction.png")
photoimage = photo.subsample(4, 4)
junction_img = photoimage
photo = PhotoImage(file = r"images\rail.png")
photoimage = photo.subsample(4, 4)
rail_img = photoimage

window.rowconfigure(1, minsize=800, weight=1)
window.columnconfigure(0, minsize=800, weight=1)

fr_options = Frame(window, width=100, height=20, bg="whitesmoke", relief = RIDGE)
fr_options2 = Frame(window, bg="whitesmoke", relief = RIDGE)
btn_file = Button(fr_options, text="File", bg="whitesmoke")
btn_edit = Button(fr_options, text="Edit", bg="whitesmoke")
fr_schedule = Frame(window, bg="whitesmoke")
btn_route = Button(fr_schedule, text="Create Route", bg="whitesmoke")

cvs_map = Canvas(window, width=100, height=100, bg="white")
fr_buttons = Frame(window, bg="grey")
btn_station = Button(fr_buttons, image=station_img, relief = FLAT, bg="grey")
btn_junction = Button(fr_buttons, image=junction_img, relief = FLAT, bg="grey")
btn_rail = Button(fr_buttons, image=rail_img, relief = FLAT, bg="grey")

fr_options.grid(row=0, column=0, sticky="ew")
fr_options2.grid(row=0, column=1, sticky="ew")
btn_file.grid(row=0, column=0, sticky="w", padx=5, pady=5)
btn_edit.grid(row=0, column=1, sticky="w", padx=5, pady=5)

btn_schedule = Button(fr_options2, text="Schedule", bg="whitesmoke", command=lambda:show_schedules(fr_schedule, fr_buttons))
btn_route.grid(row=1, column = 0, sticky="s")
cvs_map.grid(row=1, column=0, sticky="nsew")
fr_buttons.grid(row=1, column=1, sticky="ns")
btn_schedule.grid(row=0, column=0, sticky="new", padx=5, pady=5)

btn_station.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_junction.grid(row=2, column=0, sticky="ew", padx=5)
btn_rail.grid(row=3, column=0, sticky="ew", padx=5)

def create_station(event):
    stations.append(Widgets(station_img, True, 3))
def create_junction(event):
    junctions.append(Widgets(junction_img, False, 0))

##endregion

# #region graphs
Location = TypeVar('Location')
class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]: pass
class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass



class SimpleGraph:
    def __init__(self):
        self.edges: Dict[Location, List[Location]] = {}

    def neighbors(self, id: Location) -> List[Location]:
        return self.edges[id]

#example_graph = SimpleGraph()
#example_graph.edges = {
#    'A': ['B'],
#    'B': ['C'],
#    'C': ['B', 'D', 'F'],
#    'D': ['C', 'E'],
#    'E': ['F'],
#    'F': [],
#}

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self) -> bool:
        return not self.elements

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

def breadth_first_search(graph: Graph, start: Location, goal: Location):
    frontier = Queue()
    frontier.put(start)
    came_from: Dict[Location, Optional[Location]] = {}
    came_from[start] = None

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional

    return path

def create_graph():
    graph = SimpleGraph()
    for s in stations:
        temp = []
        for r in rails:
            if s in r.connections:
                temp.append(r)
        graph.edges[s]=temp
    for r in rails:
        graph.edges[r]=r.connections
    for j in junctions:
        temp = []
        for r in rails:
            if j in r.connections:
                temp.append(r)
        graph.edges[j]=temp
    return graph


def generate_path(stops):
    graph = create_graph()
    i = 1
    path = []
    prev = ""
    for s in stops:
        if i == 1:
            path.append(s)
        else:
            temp = breadth_first_search(graph, prev, s)
            temp.remove(temp[0])
            path += temp
        prev = s
        i += 1
    times = []
    time = 0
    i = 0
    for p in path:
        if i == 0:
            i+=1
        else:
            time += int(p.length)
        times.append(time)
    return path, times


#print('Reachable from A:')
#breadth_first_search(example_graph, 'A')
#print('Reachable from E:')
#breadth_first_search(example_graph, 'E')

##endregion
schedules = []
def schedule(route, times):
    times = times.split(", ")
    for t in times:
        path = {}
        stops = {}
        hours = t.split(":")
        time = (60 * int(hours[0]) + int(hours[1]))
        for p in route.path:
            temp = time + route.times[route.path.index(p)]
            temp = Decimal(temp) / Decimal(60)
            minutes, hours = math.modf(temp)
            #minutes = round(minutes, 2)
            minutes = Decimal(minutes) * Decimal(60)
            hours = int(hours)
            minutes = int(minutes)
            minutes = str(minutes)
            while len(minutes) < 2:
                minutes = "0" + minutes
            hours = str(hours)
            temp = hours + ":" + minutes
            path[p] = temp
            if p in route.stations:
                stops[p] = temp
        schedules.append(Schedules(networkName, route, stops, path))


joining = False
def join_nodes(event):
    global joining
    global clicknumber
    if not joining and event != 0:
        joining = True
        btn_rail.config(relief = SUNKEN, bg="whitesmoke")
    else:
        joining = False
        clicknumber=0
        btn_rail.config(relief = FLAT, bg="grey")

route_join = False
def route_nodes(event):
    global route_join
    global route_stations
    if not route_join and event != 0:
        route_join = True
        btn_route.config(relief = SUNKEN, text="Submit Route", bg="whitesmoke")
    else:
        route_join = False
        btn_route.config(relief = RAISED, text="Create Route", bg="whitesmoke")
        if len(route_stations) > 1:
            fr_route = Frame(fr_schedule)
            route = Routes(networkName, route_stations, fr_route)
            routes.append(route)
            path, times = generate_path(route.stations)
            route.set_path(path, times)
            for r in route_stations:
                r.widget.config(bg="white")
            route_stations=[]
            dat_update_route(route)
            dat_update_route_station(route)

def cancel_connections(event):
    global clicknumber
    global route_stations
    if joining:
        clicknumber=0
    if route_join:
        if len(route_stations) > 1:
            fr_route = Frame(fr_schedule)
            route = Routes(networkName, route_stations, fr_route)
            routes.append(route)
            path, times = generate_path(route.stations)
            route.set_path(path, times)
            for r in route_stations:
                r.widget_class.widget.config(bg="white")
            route_stations=[]

window.bind("<Button-3>", cancel_connections)
btn_station.bind("<Button-1>", create_station)
btn_junction.bind("<Button-1>", create_junction)
btn_rail.bind("<Button-1>", join_nodes)
btn_route.bind("<Button-1>", route_nodes)
class Schedules:
    def __init__(self, network, route, stops, path):
        self.network = network
        self.route = route
        self.stops = stops
        self.path = path
class Routes:
    def __init__(self, network, stations, frame):
        self.network = network
        self.ID = network + str(len(routes))
        self.stations = stations
        self.frame = frame
        self.name = f"{stations[0].get_name()} to {stations[-1].get_name()}"
        self.label = Label(self.frame, text=f"{self.name}", padx=5, pady=5)
        self.frame.bindtags("route")
        self.label.bindtags("route")
        window.bind_class("route", "<Double-Button-1>", lambda event: route_menu(self))
    def set_data (self, name, schedules):
        self.name = name
        self.schedules = schedules
        self.label.configure(text=f"{self.name}")
    def set_path(self, path, times):
        self.path = path
        self.times = times
    def toggle_colour(self, colour):
        self.frame.configure(bg=colour)
        self.label.configure(bg=colour)

class Rail:
    def __init__(self, network, connections, widget):
        self.network = network
        self.connections = connections
        self.widget = widget
        self.ID = network + str(len(rails))
        self.width = 0
        self.length = 0
    def set_data(self, length, width):
        self.width = width
        self.length = length
    def get_name(self):
        return self.ID

class Junction:
    def __init__(self, network, widget_class):
        self.network = network
        self.widget_class = widget_class
        self.ID = network + "J" + str(len(junctions))
    def get_name(self):
        return self.ID

class Station:
    def __init__(self, network, widget_class):
        self.network = network
        self.widget_class = widget_class
        self.ID = network + str(len(stations))
        self.name = f"Station{len(stations)}"
        self.platforms = 0
    def set_data(self, name, platforms):
        self.name = name
        self.platforms = platforms
    def get_name(self):
        return self.name

window.mainloop()
connection.commit()
connection.close()
