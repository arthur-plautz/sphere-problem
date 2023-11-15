from models.generation import RandomGeneration
from models.ticket import Ticket
from threading import Thread

class Ixphere(RandomGeneration, Thread):
    def __init__(self, queue, seed, time_unit, permanence, capacity):
        RandomGeneration.__init__(self, seed, time_unit)
        Thread.__init__(self)

        self.queue = queue
        self.permanence = permanence
        self.capacity = capacity

        self._reset_experience()

    def _reset_experience(self):
        self.experience = None

    def run(self):
        experiences = 0
        while (not self.queue.empty) or experiences == 0:
            tickets = []
            for _ in range(self.capacity):
                if self.experience:
                    client = self.queue.next()
                    if client.category != self.experience:
                        break;
                else:
                    client = self.queue.next()
                    self.experience = client.category
                    print(f"[Ixfera] Iniciando a experiencia {self.experience}")

                ticket = Ticket(len(tickets)+1)
                tickets.append(ticket)

                client = self.queue.remove()
                client.give_ticket(ticket)
                client.semaphore.release()

            self.generate_time(self.permanence, random=False)
            for ticket in tickets:
                ticket.semaphore.release()
            print(f"[Ixfera] Pausando a experiencia {self.experience}")
            self._reset_experience()
            experiences += 1
