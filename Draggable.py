from matplotlib.patches import Rectangle
from matplotlib.text import Text, Annotation

class dragged():
    def __init__(self, canvas,arr_drag_dict,bm) -> None:
        self.dragged = None
        self.dragged_axes = None
        self.bm = bm
        self.canvas = canvas
        self.arr_drag_dict = arr_drag_dict
        self.key = None

    def on_pick_event(self, event):
        " Store which text object was picked and were the pick event occurs."
        try:
            print(event.artist.get_label())
            print(event.artist)
            event.artist.set_animated(True)
        except Exception as e:
            print(e)
        if isinstance(event.artist, Text):
            self.dragged = event.artist
            self.key = str(self.dragged.get_gid())
            print(self.key)
            transf = event.artist.axes.transData.inverted()
            if self.arr_drag_dict[self.key] is not False:
                self.text = str(self.dragged.get_text()) 
                bbox = self.dragged.get_window_extent().transformed(transf)
                x0, y0, x1, y1 = bbox.x0, bbox.y0, bbox.x1, bbox.y1
                rectangle = Rectangle((x0, y0), x1 - x0, y1 - y0, fill=True, edgecolor='white',color="white", linewidth=1, clip_on = False)
                rect_artist = event.artist.axes.add_patch(rectangle)
                self.bm.add_patch_artist(rect_artist)
            self.pick_pos = (event.mouseevent.xdata, event.mouseevent.ydata)
            if not self.pick_pos[0]:
                display_coords = (event.mouseevent.x, event.mouseevent.y)
                self.pick_pos = self.dragged.axes.transData.inverted().transform(display_coords)


    def on_motion_event(self, event):
        if self.dragged is None or event.inaxes!=self.dragged_axes:
            self.dragged = None
            return
        old_pos = self.dragged.get_position()
        print(old_pos)
        new_pos = (old_pos[0] + event.xdata - self.pick_pos[0],old_pos[1] + event.ydata - self.pick_pos[1])
        old_pos = self.dragged.set_position(new_pos)
        self.pick_pos = (event.xdata, event.ydata)
        self.dragged.set_animated(True)
        self.bm.update()
        return True
    def on_release_event(self, event):
        " Update text position and redraw"
        if self.dragged is not None :
            old_pos = self.dragged.get_position()
            print(old_pos)
            display_coords = (event.x, event.y)
            axes_coords = self.dragged.axes.transData.inverted().transform(display_coords)
            new_pos = (old_pos[0] + axes_coords[0] - self.pick_pos[0],old_pos[1] + axes_coords[1] - self.pick_pos[1])
            if self.arr_drag_dict[self.key] is not False:
                annot_origin = self.arr_drag_dict[self.key]
                annot = self.dragged.axes.annotate(text = self.text, xy = annot_origin, xytext = new_pos, fontsize=8, arrowprops={"width":0.01, "headlength":5, "headwidth":5, "color":"black", "edgecolor":None, "linewidth":0.2}, rotation= "vertical", picker = True)
                # annot = self.dragged.axes.text(x=new_pos[0],y=new_pos[1], s = self.text , rotation= "vertical")
                annot.set_gid(self.key)
                self.bm.add_artist(annot)
                self.arr_drag_dict[self.key] = False
                self.bm.update(self.dragged)
            else:
                self.dragged.set_position(new_pos)
                self.bm.update()
            self.dragged = None
            self.text = None
        return True
