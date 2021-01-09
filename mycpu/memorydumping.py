from mycpu import mycpu
import pickle

class MemoryDummping():
    filename = "stored.bin"
    cpu: mycpu.MyCpu

    def __init__(self, cpu):
        self.cpu = cpu
        self.cpu.addCallback("stdin", self.keycallback)

    def _load(self):
        print("Loading " + self.filename)
        f = open(self.filename, "rb")
        data = pickle.load(f)
        self.cpu.reg = data["reg"]
        self.cpu.mem = data["mem"]
        self.cpu.stack = data["stack"]
        f.close()

    def _save(self):
        pass

    def keycallback(self, key):
        ret = False
        if key == b'\x1b[20~': #F9
            ret = True
            self._load()
        elif key == b'\x1b[24~': # F12
            ret = True
            print("Saving to " + self.filename + "...")
            f = open(self.filename, "wb")
            data = {"reg": self.cpu.reg, "stack": self.cpu.stack, "mem": self.cpu.mem}
            pickle.dump(data, f)
            f.close()
        else:
            pass

        return ret