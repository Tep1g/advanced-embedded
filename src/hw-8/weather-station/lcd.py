import st7796

_RGB_BLACK = st7796.RGB(0, 0, 0)
_RGB_WHITE = st7796.RGB(255,255,255)

_Y_RES = const(320)
_X = const(0)
_MEAS_X = _X + 110

_TEMP_LABEL = "Temp: "
_TEMP_LABEL_Y = _Y_RES - 320

_HUMID_LABEL = "Humid: "
_HUMID_LABEL_Y = _Y_RES - 280

_PRES_LABEL = "Pres: "
_PRES_LABEL_Y = _Y_RES - 240

_GRAPH_LABEL_X = const(0)
_GRAPH_LABEL_Y = _Y_RES - 0

def init(with_labels: bool=False):
    st7796.Init()
    st7796.Clear(_RGB_BLACK)

    if with_labels:
        st7796.Text2(_TEMP_LABEL, _X, _TEMP_LABEL_Y, _RGB_WHITE, _RGB_BLACK)
        st7796.Text2(_HUMID_LABEL, _X, _HUMID_LABEL_Y, _RGB_WHITE, _RGB_BLACK)
        st7796.Text2(_PRES_LABEL, _X, _PRES_LABEL_Y, _RGB_WHITE, _RGB_BLACK)        

def plot(data: list, graph_label: str):
    st7796.Clear(_RGB_BLACK)
    st7796.Text2(graph_label, _GRAPH_LABEL_X, _GRAPH_LABEL_Y, _RGB_WHITE, _RGB_BLACK)
    x = range(len(data))
    st7796.Plot(X=x, Y=data, Xmin=min(x), Ymin=min(data), Xmax=max(x), Ymax=max(data), color=_RGB_WHITE)

def update_values(temperature: str, humidity: str, pressure: str):
    st7796.Text2(temperature, _MEAS_X, _TEMP_LABEL_Y, _RGB_WHITE, _RGB_BLACK)
    st7796.Text2(humidity, _MEAS_X, _HUMID_LABEL_Y, _RGB_WHITE, _RGB_BLACK)
    st7796.Text2(pressure, _MEAS_X, _PRES_LABEL_Y, _RGB_WHITE, _RGB_BLACK)