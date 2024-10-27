import st7796

_RGB_BLACK = st7796.RGB(0, 0, 0)
_RGB_WHITE = st7796.RGB(255,255,255)

def init():
    st7796.Init()
    st7796.Clear(_RGB_BLACK)

def plot(data: list):
    x = range(len(data))
    st7796.Plot(X=x, Y=data, Xmin=min(x), Ymin=min(data), Xmax=max(x), Ymax=max(data), color=_RGB_WHITE)