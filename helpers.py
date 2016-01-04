# coding=utf-8
from settings import streaming_config


class ChunkedStream:
    def __init__(self):
        self.chunk_size = streaming_config["chunk_size"]
        self.total_chunks = streaming_config["total_chunks"]
        self.stream = None

    def __call__(self, f):
        def wrapped_f(*args):
            self.stream = f(*args)

            chunk_count = 0
            current_chunk = []
            while chunk_count < self.total_chunks or self.total_chunks != -1:
                current_chunk.append(self.stream.next())
                if len(current_chunk) >= self.chunk_size:
                    yield current_chunk
                    current_chunk = []
                    chunk_count += 1

        return wrapped_f


class Dictrement:
    def __init__(self):
        self.underlying = dict()

    def get_dict(self):
        return self.underlying

    def get(self, key):
        return self.underlying[key] \
            if key in self.underlying \
            else None

    def increment(self, key):
        if key not in self.underlying:
            self.underlying[key] = 0
        self.underlying[key] += 1
