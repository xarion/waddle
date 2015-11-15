class ChunkedStream:
    def __init__(self, chunk_size=10, total_chunks=10):
        self.chunk_size = chunk_size
        self.total_chunks = total_chunks
        self.stream = None

    def __call__(self, f):
        def wrapped_f(*args):
            self.stream = f(*args)

            chunk_count = 0
            current_chunk = []
            while chunk_count < self.total_chunks:
                current_chunk.append(self.stream.next())
                if len(current_chunk) >= self.chunk_size:
                    yield current_chunk
                    current_chunk = []
                    chunk_count += 1

        return wrapped_f
