from collections import deque
from matplotlib.text import Text
from matplotlib.patches import FancyArrow
class BlitManager:
    def __init__(self, canvas, animated_artists=()):
        self.canvas = canvas
        self._artists = deque()
        self._bg = None
        for a in animated_artists:
            self.add_artist(a)

        self.cid = canvas.mpl_connect("draw_event", self.on_draw)
    def _later(self, evt=None):
        self.timer = self.canvas.new_timer(interval=1000)
        self.timer.single_shot = True
        self.timer.add_callback(self.update_background)
        self.timer.start()
    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        if event is not None:
            if event.canvas != self.canvas:
                raise RuntimeError
        self._later()
        self._draw_animated()

    def update_background(self):
        self._bg = self.canvas.copy_from_bbox(self.canvas.figure.bbox)
    def _draw_animated(self, leave_out = None):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        index = None
        for i,a in enumerate(self._artists):
            if a == leave_out:
                index = i
                print(f"the artist I AM NOT DRAWING IS {a}")
            else:
                fig.draw_artist(a)
        if index:
            del self._artists[index]
    def add_artist(self, art):
        """Add a new Artist object to the Blit Manager"""
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)
    def add_patch_artist(self, patch):
        if patch.figure != self.canvas.figure:
            raise RuntimeError
        patch.set_animated(True)
        self._artists.appendleft(patch)
    def update(self, annot=None):
        """Update the screen with animated artists."""
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            self.canvas.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated(leave_out = annot)
            # update the GUI state
            self.canvas.blit(self.canvas.figure.bbox)
        # let the GUI event loop process anything it has to do
        self.canvas.flush_events()
    def return_data(self):
        return self._bg, self._artists
    def on_zoom(self):
        for art in self._artists:
            if isinstance(art,Text) or isinstance(art,FancyArrow):
                art.set_clip_on(True)

    def on_home(self, zoomed_in):
        if zoomed_in is True:
            for art in self._artists:
                if isinstance(art,Text) or isinstance(art,FancyArrow):
                    art.set_clip_on(False)

    def adjust_subplots(self):
        self.canvas.figure.subplots_adjust(left = 0.017, hspace = 1.3)
    def stop_work(self):
        self.is_working = False
        # Additional cleanup or resource release code here
        # Destroy the current instance
        del self
