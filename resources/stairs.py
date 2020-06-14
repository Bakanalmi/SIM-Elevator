import simpy, time

class Stairs:
    def __init__(self, env, values):
        self.env = env
        self.velocity = values.get('stairs').get('velocity')
        self.capacity = values.get('stairs').get('capacity')
        self.res = simpy.Resource(env, capacity=self.capacity)
        self.floors = {}

    def request(self, token):
        print('[%d]\tToken %d is taking the stairs.'  % (self.env.now, token.id))
        request = self.res.request()
        yield request

        timeout = abs(token.current - token.destination) * self.velocity
        yield self.env.timeout(timeout)
        self.res.release(request)
        token.current = token.destination

    def set_floors(self, floors):
        for key, floor in floors.items():
            self.floors[key] = floor