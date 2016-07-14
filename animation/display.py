import os
import sys
import bootstrap     # Demonstration specific setup.
import vispy.scene   # Canvas & visuals for rendering.
import numpy

import collections
import math

import paths_data
import params

# style
SELECTED_PATH_WIDTH = 5
PATH_WIDTH = 1
SELECTED_ARROW_SIZE = 20.0
ARROW_SIZE = 14.0

# colors
COLOR_NEUTRAL = numpy.asarray([0.5,0.5,0.5])
COLOR_SELECTED = numpy.asarray([0.8,0.2,0.8])

class Application(object):

    def __init__(self, example_idx, title='nucl.ai Motion Matching'):
        self.canvas = vispy.scene.SceneCanvas(
                                title=title,
                                size=(1280, 720),
                                bgcolor='black',
                                show=False,
                                keys='interactive')

        self.example_idx = example_idx
        self.params = params.Params()
        self.widget = self.canvas.central_widget
        self.view = self.canvas.central_widget.add_view()
        self.marker = vispy.scene.Markers(pos=numpy.asarray([[0,0]]), face_color='red', size=0, parent=self.view.scene)
        # prepare display
        self.lines = []
        self.vectors = []
        self.colors = []
        for i in range(self.params.TOP_PATHS_NUMBER):
            path_width = SELECTED_PATH_WIDTH if i == 0 else PATH_WIDTH
            arrow_size = SELECTED_ARROW_SIZE if i == 0 else ARROW_SIZE
            color = COLOR_SELECTED if i == 0 else COLOR_NEUTRAL
            vectors_line = []
            # color = numpy.random.rand(3) # using fixed colors now
            self.colors.append(color)
            line = vispy.scene.Line(parent=self.view.scene, color=color, connect='strip', method='agg', width=path_width)
            line.transform = vispy.visuals.transforms.MatrixTransform()
            self.lines.append(line)
            for j in range(self.params.SEGMENT_SIZE):
                if not self.params.VECTOR_POINT or self.params.VECTOR_POINT == j:
                    arr1 = vispy.scene.Arrow(numpy.asarray([[0,0],[0,0]]), parent=self.view.scene, color=color, method='agg', arrow_size=arrow_size, width=path_width)
                    arr1.transform = vispy.visuals.transforms.MatrixTransform()
                    arr2 = vispy.scene.Arrow(numpy.asarray([[0,0],[0,0]]), parent=self.view.scene, color=color, method='agg', arrow_size=arrow_size, width=path_width)
                    arr2.transform = arr1.transform
                    self.marker.transform = arr1.transform
                    vectors_line.append([arr1, arr2])
                else: vectors_line.append([None, None])
            self.vectors.append(vectors_line)

        self.timer_toggle = True
        self.player_position = numpy.asarray([0,0])
        if not os.path.exists('dota2.csv'):
            print("ERROR: Please download and extract this file...\nhttps://github.com/aigamedev/nuclai16/releases/download/0.0/dota2.csv.bz2\n")
            sys.exit(-1)
        self.paths_data = paths_data.PathsData('dota2.csv', self.params, follow_player=(example_idx == 3), advancing=(example_idx == 3 or example_idx == 2))
        # init the searched point with some random value - after first mouse move it's a
        self.paths_data.mouse_xy = ( ( numpy.random.rand(2) * 10 - 5 ) - numpy.asarray(self.canvas.size) / 2 ) * self.params.SCALE_FACTOR

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
            # @TODO: translate paths and vectors


        @self.canvas.events.mouse_move.connect
        def on_mouse_move(event):
            self.paths_data.mouse_xy = (numpy.asarray(self.view.camera.transform.imap(event.pos)) - numpy.asarray(self.canvas.size) / 2) * self.params.SCALE_FACTOR


        @self.canvas.events.draw.connect
        def on_draw(event):
            pass


    def draw_vector(self, ev):
        selected_paths = self.paths_data.get_paths()
        for i in range(self.params.TOP_PATHS_NUMBER):
            if i >= len(selected_paths):
                # clear and skip
                self.lines[i].set_data(pos=numpy.asarray([[0,0],[0,0]]))
                for p_i, point in enumerate(selected_path):
                    if self.params.VECTOR_POINT and p_i != self.params.VECTOR_POINT: continue
                    self.vectors[i][p_i][0].set_data(pos=numpy.asarray([[0,0],[0,0]]), arrows=None)

            selected_path = selected_paths[i][4]
            self.lines[i].set_data(pos=selected_path[:,[0,1]])
            self.lines[i].transform.reset()
            self.lines[i].transform.translate((selected_path[0][0:2] * -1))
            self.lines[i].transform.translate(numpy.asarray(self.canvas.size) / 2)

            for p_i, point in enumerate(selected_path):
                if self.params.VECTOR_POINT and p_i != self.params.VECTOR_POINT: continue

                # draw the angle
                angle = (selected_paths[i][1] * self.params.SEGMENT_SIZE + p_i) % 361 # the index in data vector
                v_x = math.cos(angle) * math.hypot(selected_path[p_i][2], selected_path[p_i][3])
                v_y = math.sin(angle) * math.hypot(selected_path[p_i][2], selected_path[p_i][3])
                vector = numpy.asarray([[0,0], [v_x, v_y]])

                self.vectors[i][p_i][0].set_data(pos=vector, arrows=vector.reshape(1,4))
                self.vectors[i][p_i][0].transform.reset()
                self.vectors[i][p_i][0].transform.translate((selected_path[p_i][0:2]))
                self.vectors[i][p_i][0].transform.translate((selected_path[0][0:2] * -1))
                self.vectors[i][p_i][0].transform.translate(numpy.asarray(self.canvas.size) / 2)


    def draw_closest_with_team_vectors(self, ev):
        selected_paths = self.paths_data.get_paths()
        for i in range(self.params.TOP_PATHS_NUMBER):
            if i >= len(selected_paths):
                # clear and skip
                self.lines[i].set_data(pos=numpy.asarray([[0,0],[0,0]]))

                for p_i, point in enumerate(selected_path):
                    if self.params.VECTOR_POINT and p_i != self.params.VECTOR_POINT: continue
                    self.vectors[i][p_i][0].set_data(pos=numpy.asarray([[0,0],[0,0]]), arrows=None)
                    self.vectors[i][p_i][1].set_data(pos=numpy.asarray([[0,0],[0,0]]), arrows=None)

            selected_path = self.paths_data.segments[selected_paths[i][2]][selected_paths[i][1]]
            self.lines[i].set_data(pos=selected_path[:,[0,1]])
            self.lines[i].transform.reset()
            self.lines[i].transform.translate((selected_path[0][0:2] * -1))
            self.lines[i].transform.translate(numpy.asarray(self.canvas.size) / 2)

            for p_i, point in enumerate(selected_path):
                if self.params.VECTOR_POINT and p_i != self.params.VECTOR_POINT: continue
                nearest_frined = []
                nearest_enemy = []
                # get the nearest friend / enemy to 
                for hero_id in self.paths_data.data.keys():
                    if hero_id != selected_paths[i][2]: # it's not the own player
                        if hero_id in self.paths_data.segments and len(self.paths_data.segments[hero_id]) > selected_paths[i][1] and len(self.paths_data.segments[hero_id][selected_paths[i][1]]) > 0:
                            hero_point = self.paths_data.segments[hero_id][selected_paths[i][1]][p_i]
                            distance = math.hypot(hero_point[0] - point[0], hero_point[1] - point[1])
                            if self.paths_data.user_team_lookup[hero_id] == self.paths_data.user_team_lookup[selected_paths[i][2]]: # friend
                                if len(nearest_frined) == 0 or nearest_frined[1] > distance: nearest_frined = (hero_id, distance, hero_point[0:2])
                            else: # enemy
                                if len(nearest_enemy) == 0 or nearest_enemy[1] > distance: nearest_enemy = (hero_id, distance, hero_point[0:2])

                friend_vector = numpy.asarray([point[0:2], nearest_frined[2]]) if nearest_frined else numpy.asarray([[0,0],[0,0]])
                self.vectors[i][p_i][0].set_data(pos=friend_vector, arrows=friend_vector.reshape(1,4))
                self.vectors[i][p_i][0].transform.reset()
                self.vectors[i][p_i][0].transform.translate((selected_path[0][0:2] * -1))
                self.vectors[i][p_i][0].transform.translate(numpy.asarray(self.canvas.size) / 2)
                enemy_vector = numpy.asarray([point[0:2], nearest_enemy[2]]) if nearest_enemy else numpy.asarray([[0,0],[0,0]])
                self.vectors[i][p_i][1].set_data(pos=enemy_vector, arrows=enemy_vector.reshape(1,4))


    def draw_current_path_advance(self, ev):

        selected_paths = self.paths_data.get_paths()

        for i in range(self.params.TOP_PATHS_NUMBER):
            if i >= len(selected_paths):
                # clear and skip
                self.lines[i].set_data(pos=numpy.asarray([[0,0],[0,0]]))
                continue

            current = selected_paths[i][4]
            draw_to = self.params.MOVE_ALONG_STEP_SIZE

            if i == 0:
                draw_to += self.paths_data.advance_point
                #marker_point = current[self.paths_data.advance_point][0:2]
                marker_point = selected_paths[i][3]
                # append short history
                if selected_paths[i][1] > 0 and len(self.paths_data.segments[selected_paths[i][2]][selected_paths[i][1] - 1]) > 0:
                    current = numpy.concatenate((self.paths_data.segments[selected_paths[i][2]][selected_paths[i][1] - 1][-self.params.MOVE_ALONG_STEP_SIZE/3:], current))

            current = current[0:draw_to]

            self.lines[i].set_data(pos=current[:,[0,1]])
            self.lines[i].transform.reset()
            self.lines[i].transform.translate((selected_paths[i][3] * -1))
            self.lines[i].transform.translate(self.paths_data.player_position)
            # to have [0,0] in the screen center
            self.lines[i].transform.translate(numpy.asarray(self.canvas.size) / 2)

            if i == 0:
                self.marker.set_data(pos=numpy.asarray([marker_point]), face_color=self.colors[i], size=15)
                self.marker.transform = self.lines[i].transform


    def process(self, _):
        return


    def run(self):
        self.timer = vispy.app.Timer(interval=1.0 / 30.0)
        if self.example_idx == 0:
            self.timer.connect(self.draw_vector)
        elif self.example_idx == 1:
            self.timer.connect(self.draw_closest_with_team_vectors)
        elif self.example_idx == 2 or self.example_idx == 3:
            self.timer.connect(self.draw_current_path_advance)
        self.timer.start(0.5) # 30 FPS
        vispy.app.run()


if __name__ == "__main__":
    vispy.set_log_level('WARNING')
    vispy.use(app='glfw')

    import argparse
    parser = argparse.ArgumentParser(description='nucl.ai16')
    parser.add_argument('-e','--example', help='Description for foo argument', default=0, type=int)
    args = parser.parse_args()
    app = Application(args.example)
    app.run()
