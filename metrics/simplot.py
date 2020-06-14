import matplotlib.pyplot as plt

class Metrics:
    def __init__(self, env, values, title):
        self.env = env
        self.start = values.get('time').get('from')
        self.timeout = values.get('metrics')
        self.title = title

        self.wait_time = []
        self.gather_times = []

        self.arrival_source = None
        self.arrival_values = []
        self.waiting_values = []

        n_elev = values.get('environment').get('n_elevator')
        self.consum_energetic = [[] for _ in range(n_elev)]

        self.figure = plt.figure()
        self.dashboard = self.figure.add_subplot(111)
        self.arribades = self.figure.add_subplot(221)
        self.esperes = self.figure.add_subplot(222)
        self.consum = self.figure.add_subplot(212)

    def gather(self):
        while True:
            now = self.env.now/3600 + self.start
            self.gather_times.append(now)

            if self.arrival_source != None:
                howmany = len(self.arrival_source.waiting)
                self.arrival_values.append(howmany)
            else:
                self.arrival_values.append(0)

            if len(self.wait_time) > 0:
                wait_avg = sum(self.wait_time) / len(self.wait_time) 
                self.waiting_values.append(wait_avg)
                self.wait_time.clear()
            else:
                self.waiting_values.append(0)

            yield self.env.timeout(self.timeout)

    def build(self):
        self.dashboard.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

        self.arribades.set_title('Arribades')
        self.arribades.bar(self.gather_times, self.arrival_values)

        self.esperes.set_title('Temps espera')
        self.esperes.bar(self.gather_times, self.waiting_values)

        self.consum.set_title('Consum energetic')
        self.consum.plot(self.gather_times, self.waiting_values)
        self.consum.plot(self.gather_times, self.arrival_values)
        
        #plt.plot(self.gather_times, self.arrival_values)
        plt.suptitle(self.title)

    def show(self):
        self.build()
        plt.show()

    def waiting(self, time):
        self.wait_time.append(abs(time))