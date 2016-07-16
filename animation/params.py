class Params:
    SEGMENT_SIZE = 10
    TOP_PATHS_NUMBER = 5
    SAMPLE_SIZE = 150
    SCALE_FACTOR = 200
    TELEPORT_THRESHOLD = 40 # it defines a disatnce where we elimiate a segment - we skip all teleports
    HISTORY_SIZE = 100

    def __init__(self):
        self.VECTOR_POINT = int(self.SEGMENT_SIZE / 2)
        self.MOVE_ALONG_STEP_SIZE = int(self.SEGMENT_SIZE / 2)
