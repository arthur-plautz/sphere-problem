from models.generation import RandomGeneration
from models.ticket import Ticket
from threading import Thread
from time import perf_counter

class Ixphere(RandomGeneration, Thread):
    def __init__(self, queue, seed, time_unit, capacity):
        RandomGeneration.__init__(self, seed, time_unit)
        Thread.__init__(self)

        self.queue = queue
        self.capacity = capacity

        self._reset_experience()

    def stats(self, total_time, experiences_time):
        self.occupation = experiences_time / total_time
        print(f"\nTaxa de ocupacao: {str(self.occupation)[:4]}")

    def _reset_experience(self):
        self.experience = None

    def run(self):
        start = perf_counter()

        experiences_time = 0
        while (not self.queue.empty) or experiences_time == 0:
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
                    start_experience = perf_counter()

                ticket = Ticket(len(tickets)+1)
                tickets.append(ticket)

                client = self.queue.remove()
                client.receive_ticket(ticket)

            for ticket in tickets:
                ticket.end_show()

            print(f"[Ixfera] Pausando a experiencia {self.experience}")
            end_experience = perf_counter()

            self._reset_experience()
            experiences_time += end_experience - start_experience

        end = perf_counter()
        total_time = end - start

        self.stats(total_time, experiences_time)
