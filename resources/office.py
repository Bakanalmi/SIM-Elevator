import simpy

class Office:
    def __init__(self, env, values, floor):
        self.env = env
        self.capacity = values.get('environment').get('cap_floor')
        self.working_time = values.get('time').get('work') * 3600
        self.res = simpy.Resource(env, capacity=self.capacity)
        self.floor = floor

    def request(self, token):
        print('[%d]\tToken %d starts working on floor %d'  % (self.env.now, token.id, self.floor.floor))
        request = self.res.request()
        yield request

        yield self.env.timeout(self.working_time)
        self.res.release(request)
