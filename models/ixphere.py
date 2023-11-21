from models.generation import RandomGeneration
from models.ticket import Ticket
from threading import Thread
from time import perf_counter

class Ixphere(RandomGeneration, Thread):
    def __init__(self, queue, seed, time_unit, permanence, capacity):
        RandomGeneration.__init__(self, seed, time_unit)
        Thread.__init__(self)

        self.queue = queue
        self.permanence = permanence
        self.capacity = capacity
        self.occupation = 0

        self._reset_experience()

    def stats(self, total_time, experiences):
        self.occupation = (experiences * self.permanence * self.time_unit) / total_time
        print(f"\nTaxa de ocupacao: {str(self.occupation)[:4]}")

    def _reset_experience(self):
        self.experience = None

    def run(self):
        start = perf_counter()

        experiences = 0
        while (not self.queue.empty) or experiences == 0:
            tickets = []
            for _ in range(self.capacity):
                if self.experience:
                    if self.queue.empty:
                        break
                    client = self.queue.next()
                    if client.category != self.experience:
                        break
                else:
                    client = self.queue.next()
                    self.experience = client.category
                    print(f"[Ixfera] Iniciando a experiencia {self.experience}")

                ticket = Ticket(len(tickets)+1)
                tickets.append(ticket)

                client = self.queue.remove()
                client.receive_ticket(ticket)

            for ticket in tickets:
                ticket.end_show()
            print(f"[Ixfera] Pausando a experiencia {self.experience}")
            self._reset_experience()
            experiences += 1

        end = perf_counter()
        total_time = end - start

        self.stats(total_time, experiences)
