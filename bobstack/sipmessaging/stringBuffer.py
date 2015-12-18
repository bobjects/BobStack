import threading
import io
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

MAX_BUFFER = 1024**2*4

class StringBuffer(object):
    def __init__(self, max_size=MAX_BUFFER):
        self.buffers = []
        self.max_size = max_size
        self.lock = threading.Lock()
        self.closing = False
        self.eof = False
        self.read_pos = 0
        self.write_pos = 0

    def write(self, data):
        self.lock.acquire()
        try:
            if not self.buffers:
                self.buffers.append(StringIO())
                self.write_pos = 0
            buffer = self.buffers[-1]
            buffer.seek(self.write_pos)
            buffer.write(data)
            if buffer.tell() >= self.max_size:
                buffer = StringIO()
                self.buffers.append(buffer)
            self.write_pos = buffer.tell()
        finally:
            self.lock.release()

    def read(self, length=-1):
        self.lock.acquire()
        read_buf = StringIO()
        try:
            remaining = length
            while True:
                if not self.buffers:
                    break
                buffer = self.buffers[0]
                buffer.seek(self.read_pos)
                read_buf.write(buffer.read(remaining))
                self.read_pos = buffer.tell()
                if length == -1:
                    # we did not limit the read, we exhausted the buffer, so delete it.
                    # keep reading from remaining buffers.
                    del self.buffers[0]
                    self.read_pos = 0
                else:
                    #we limited the read so either we exhausted the buffer or not:
                    remaining = length - read_buf.tell()
                    if remaining > 0:
                        # exhausted, remove buffer, read more.
                        # keep reading from remaining buffers.
                        del self.buffers[0]
                        self.read_pos = 0
                    else:
                        # did not exhaust buffer, but read all that was requested.
                        # break to stop reading and return data of requested length.
                        break
        finally:
            self.lock.release()
        return read_buf.getvalue()

    def peek(self, length=-1):
        self.lock.acquire()
        buffers = list(self.buffers)
        read_pos = self.read_pos
        answer = self.read(length=length)
        self.buffers = buffers
        self.read_pos = read_pos
        return answer

    def readline(self):
        # TODO - very inefficient, fix that.
        # TODO - left off testing this.  Python never returned from this function.  Presumably a problem with peek().  Debug with PyCharm's debugger.
        asString = self.peek()
        match = re.search(u'^(.*)\r\n',asString)
        if match:
            return match.group(0)
        else:
            return asString

    def __len__(self):
        len = 0
        self.lock.acquire()
        try:
            for buffer in self.buffers:
                buffer.seek(0, 2)
                if buffer == self.buffers[0]:
                    len += buffer.tell() - self.read_pos
                else:
                    len += buffer.tell()
            return len
        finally:
            self.lock.release()

    def close(self):
        self.eof = True