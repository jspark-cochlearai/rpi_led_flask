"""
LED light pattern like Google Home
"""

import apa102
import time
import threading
try:
    import queue as Queue
except ImportError:
    import Queue as Queue


class Pixels:
    PIXELS_N = 3

    def __init__(self):
        self.basis = [0] * 3 * self.PIXELS_N
        self.green_basis = [0] * 3 * self.PIXELS_N
        self.red_basis = [0] * 3 * self.PIXELS_N
        #self.basis[0] = 2
        #self.basis[3] = 1
        #self.basis[4] = 1
        #self.basis[7] = 2
        self.basis[1] = 2
        self.basis[4] = 2
        self.basis[7] = 2

        self.green_basis[1] = 2
        #self.green_basis[4] = 2
        #self.green_basis[7] = 2

        self.red_basis[0] = 2
        self.red_basis[3] = 2
        self.red_basis[6] = 2

        self.colors = [0] * 3 * self.PIXELS_N
        self.dev = apa102.APA102(num_led=self.PIXELS_N)

        self.next = threading.Event()
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def wakeup(self, direction=0, rgb="g"):
        def f():
            self._wakeup(direction, rgb=rgb)

        self.next.set()
        self.queue.put(f)

    def listen(self):
        self.next.set()
        self.queue.put(self._listen)

    def think(self):
        self.next.set()
        self.queue.put(self._think)

    def speak(self):
        self.next.set()
        self.queue.put(self._speak)

    def blink(self, rgb="g"):
        def f2():
            self._blink(rgb=rgb)
        self.next.set()
        self.queue.put(f2)

    def off(self):
        self.next.set()
        self.queue.put(self._off)

    def _run(self):
        while True:
            func = self.queue.get()
            func()

    def _wakeup(self, direction=0, rgb="g"):
        #for i in range(1, 25):
        if rgb == "g":
            for i in range(1, 2):
                colors = [i * v for v in self.green_basis]
                self.write(colors)
                time.sleep(0.01)
            self.colors = colors
        elif rgb == "r":
            for i in range(1, 20):
                colors = [i * v for v in self.red_basis]
                self.write(colors)
                time.sleep(0.01)
            self.colors = colors
        else:
            print("Color unspecified.")
            self.colors = colors

    def _listen(self):
        for i in range(1, 25):
            colors = [i * v for v in self.basis]
            self.write(colors)
            time.sleep(0.01)

        self.colors = colors

    def _think(self):
        colors = self.colors

        self.next.clear()
        while not self.next.is_set():
            colors = colors[3:] + colors[:3]
            self.write(colors)
            time.sleep(0.2)

        t = 0.1
        for i in range(0, 5):
            colors = colors[3:] + colors[:3]
            self.write([(v * (4 - i) / 4) for v in colors])
            time.sleep(t)
            t /= 2

        # time.sleep(0.5)

        self.colors = colors

    def _speak(self):
        colors = self.colors
        gradient = -1
        position = 24

        self.next.clear()
        while not self.next.is_set():
            position += gradient
            self.write([(v * position / 24) for v in colors])

            if position == 24 or position == 4:
                gradient = -gradient
                time.sleep(0.2)
            else:
                time.sleep(0.01)

        while position > 0:
            position -= 1
            self.write([(v * position / 24) for v in colors])
            time.sleep(0.01)

        # self._off()

    def _blink(self, rgb="g"):

        #for i in range(1, 20):
        #    colors = [i * v for v in self.red_basis]
        #    self.write(colors)
        #    time.sleep(0.01)


        #colors = self.colors
        if rgb == "r":
            colors = [1 * v for v in self.red_basis]
        elif rgb == "g":
            colors = [1 * v for v in self.green_basis]
        gradient = 1
        position = 1

        self.next.clear()
        #while not self.next.is_set():
        i_blink = 0
        while True:
            position += gradient
            self.write([(v * position / 2) for v in colors])

            if position == 24 or position == 1:
                gradient = -gradient
                time.sleep(0.2)
                i_blink += 1
                if i_blink >= 6:
                    break
            else:
                time.sleep(0.01)

        while position > 0:
            position -= 1
            self.write([(v * position / 2) for v in colors])
            time.sleep(0.01)
        

    def _off(self):
        self.write([0] * 3 * self.PIXELS_N)

    def write(self, colors):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(colors[3*i]), int(colors[3*i + 1]), int(colors[3*i + 2]))

        self.dev.show()


'''
pixels = Pixels()

if __name__ == '__main__':
    while True:

        try:
            pixels.wakeup(rgb="g")
            time.sleep(0.5)
            pixels.wakeup(rgb="r")
            time.sleep(0.5)
            pixels.wakeup(rgb="g")
            time.sleep(0.5)
            pixels.wakeup(rgb="r")
            time.sleep(0.5)
            pixels.wakeup(rgb="g")
            time.sleep(0.5)
            
            #pixels.think()
            #time.sleep(3)
            #pixels.speak()
            #time.sleep(3)
            #pixels.off()
            #time.sleep(3)
            
        except KeyboardInterrupt:
            break


    pixels.off()
    time.sleep(1)
'''
