import os
import sys
import bootstrap     # Demonstration specific setup.
import vispy.scene   # Canvas & visuals for rendering.
import numpy

import collections
import math

import data
import params

# style
SELECTED_PATH_WIDTH = 5
HISTORY_PATH_WIDTH = 3
PATH_WIDTH = 1
SELECTED_ARROW_SIZE = 20.0
ARROW_SIZE = 14.0
# colors
COLOR_NEUTRAL = numpy.asarray([0.5,0.5,0.5])
COLOR_SELECTED = numpy.asarray([0.8,0.2,0.8])

class Application(object):

    def __init__(self, title='nucl.ai Motion Matching'):
        self.canvas = vispy.scene.SceneCanvas(
                                title=title,
                                size=(1280, 720),
                                bgcolor='black',
                                show=False,
                                keys='interactive')

        self.params = params.Params()
        self.widget = self.canvas.central_widget
        self.view = self.canvas.central_widget.add_view()
        self.marker = vispy.scene.Markers(pos=numpy.asarray([[0,0]]), face_color='red', size=0, parent=self.view.scene)
        self.select = True # identify if the current tick select or advance the path
        # prepare display
        self.lines = []
        self.colors = []
        self.history = []
        self.history_pointer = 0
        for i in range(self.params.HISTORY_SIZE):
            line = vispy.scene.Line(parent=self.view.scene, color=COLOR_NEUTRAL, connect='strip', method='agg', width=HISTORY_PATH_WIDTH)
            line.transform = vispy.visuals.transforms.MatrixTransform()
            self.history.append(line)

        for i in range(self.params.TOP_PATHS_NUMBER):
            path_width = SELECTED_PATH_WIDTH if i == 0 else PATH_WIDTH
            arrow_size = SELECTED_ARROW_SIZE if i == 0 else ARROW_SIZE
            color = COLOR_SELECTED if i == 0 else COLOR_NEUTRAL
            # color = numpy.random.rand(3) # using fixed colors now
            self.colors.append(color)
            line = vispy.scene.Line(parent=self.view.scene, color=color, connect='strip', method='agg', width=path_width)
            line.transform = vispy.visuals.transforms.MatrixTransform()
            self.lines.append(line)

        self.timer_toggle = True
        self.player_position = numpy.asarray([0,0])
        if not os.path.exists('dota2.csv'):
            print("ERROR: Please download and extract this file...\nhttps://github.com/aigamedev/nuclai16/releases/download/0.0/dota2.csv.bz2\n")
            sys.exit(-1)
        self.data = data.Data('dota2.csv', self.params)
        # init the searched point with some random value - after first mouse move it's a
        self.data.mouse_xy = ( ( numpy.random.rand(2) * 10 - 5 ) - numpy.asarray(self.canvas.size) / 2 ) * self.params.SCALE_FACTOR

        self.grid = vispy.scene.visuals.GridLines(parent=self.view.scene, color=(1, 1, 1, 1))
        self.grid.transform = vispy.visuals.transforms.MatrixTransform()
        self.grid.transform.translate(numpy.asarray(self.canvas.size) / 2)
        self.canvas.show(visible=True)
        # HACK: Bug in VisPy 0.5.0-dev requires a click for layout to occur.
        self.canvas.events.mouse_press()


        @self.canvas.events.key_press.connect
        def on_key_press(event):
            if event.key.name == ' ':
                if self.timer_toggle: self.timer.stop()
                else: self.timer.start()
                self.timer_toggle = not self.timer_toggle


        @self.canvas.events.resize.connect
        def on_resize(event):
            self.grid.transform.reset()
            self.grid.transform.translate(numpy.asarray(self.canvas.size) / 2)
            # @TODO: translate paths


        @self.canvas.events.mouse_move.connect
        def on_mouse_move(event):
            self.data.mouse_xy = (numpy.asarray(self.view.camera.transform.imap(event.pos)) - numpy.asarray(self.canvas.size) / 2) * self.params.SCALE_FACTOR


        @self.canvas.events.draw.connect
        def on_draw(event):
            pass

    def draw_current_path_advance(self, ev):
        if self.select:
            _, new_path = self.data.get_paths()
        else:
            self.data.advance()
            new_path = False
        for i in range(self.params.TOP_PATHS_NUMBER):
            if i != 0 and not self.select: continue # just advancing, no need to redraw all selection
            if i >= len(self.data.selected_paths):
                # clear and skip
                self.lines[i].set_data(pos=numpy.asarray([[0,0],[0,0]]))
                continue

            current = self.data.selected_paths[i][4]
            draw_to = self.params.MOVE_ALONG_STEP_SIZE

            if i == 0:
                draw_to += self.data.advance_point
                marker_point = current[self.data.advance_point][0:2]

            current = current[0:draw_to]
            self.lines[i].set_data(pos=current[:,[0,1]])
            if self.select:
                self.lines[i].transform.reset()
                self.lines[i].transform.translate((self.data.selected_paths[i][3] * -1))
                self.lines[i].transform.translate(self.data.player_position)
                # to have [0,0] in the screen center
                self.lines[i].transform.translate(numpy.asarray(self.canvas.size) / 2)

            if i == 0:
                self.marker.set_data(pos=numpy.asarray([marker_point]), face_color=self.colors[i], size=15)
                self.marker.transform = self.lines[i].transform

        if new_path:
            # append history
            self.history[self.history_pointer].transform.reset()
            self.history[self.history_pointer].transform = vispy.visuals.transforms.MatrixTransform()
            current = self.data.previous_path[0][4][0:self.data.previous_path[1]]
            self.history[self.history_pointer].set_data(current[:,[0,1]])
            self.history[self.history_pointer].transform.translate((self.data.previous_path[0][3] * -1))
            self.history[self.history_pointer].transform.translate(self.data.previous_path[0][5])
            self.history[self.history_pointer].transform.translate(numpy.asarray(self.canvas.size) / 2)
            self.history_pointer += 1
            if self.history_pointer == self.params.HISTORY_SIZE: self.history_pointer = 0

        self.select = not self.select


    def process(self, _):
        return


    def run(self):
        self.timer = vispy.app.Timer(interval=1.0 / 30.0)
        self.timer.connect(self.draw_current_path_advance)
        self.timer.start(0.033) # 30 FPS
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')
    app = Application()
    app.run()
