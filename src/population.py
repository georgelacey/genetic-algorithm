from individual import Individual
from random import Random

rand = Random()


class Population(object):

    def __init__(self, size):
        self.members = list()
        for current in range(0, size):
            self.members.append(Individual())

    def __str__(self):
        return_string = ""
        position = 0
        for member in self.members:
            return_string += "%d:\tx: %e\ty: %e\tfit: %e\n" %\
                             (position, member.x, member.y, member.fitness())
            position += 1
        return_string += "Average fit:\t%e\n" % self.avg_fitness()
        best = self.best_fitness()
        return_string += "Best fit:\tx:%e,\ty:%e\tf:%e" %\
                         (best.x, best.y, best.fitness())
        return return_string

    def total_fitness(self, members=None):
        total = 0

        if members is None:
            members = self.members

        for member in members:
            total += member.fitness()

        return total

    def avg_fitness(self):
        return float(self.total_fitness() / len(self.members))

    def best_fitness(self):
        return self.best_member().fitness()

    def best_member(self):
        best_member = self.members[0]

        for member in self.members:
            if float(member.fitness()) > best_member.fitness():
                best_member = member
        return best_member

    def roulette(self, members=None):
        total = self.total_fitness(members=members)
        position = rand.uniform(0, total)

        if members is None:
            members = self.members

        for member in members:
            position -= member.fitness()
            if position <= 0:
                return member

    def mutate(self, chance):
        for member in self.members:
            if rand.random() < chance/100:
                member.mutate()

    def elite(self, amount):
        sorted_members = sorted(self.members, key=lambda
                                x: x.fitness(), reverse=True)[:amount]

        return sorted_members

    def advance_generation(self, n_elite, crossover_rate=0.5, n_arena=4, mutation=0):
        new_generation = list()

        while len(new_generation) < len(self.members) - n_elite:
            if n_arena > 0:
                x, y = self.tournament_selection(n_arena, crossover_rate)

            new_generation.append(x)
            new_generation.append(y)

        # Remove excess members
        while len(new_generation) > len(self.members) - n_elite:
            new_generation.pop()

        for member in new_generation:
            if rand.random() < mutation/100:
                member.mutate()

        # elitism
        new_generation += self.elite(n_elite)

        self.members = new_generation

    def remove_member(self, member):
        self.members.remove(member)

    def tournament_selection(self, arena_size, rate):
        parents = list()
        for i in range(arena_size):
            parents.append(self.members[rand.randint(0, len(self.members) - 1)])
        parents = sorted(parents, key=lambda x: x.fitness(), reverse=True)

        if rand.random() < rate:
            return parents[0].crossover(parents[1])
        else:
            return parents[0], parents[1]
