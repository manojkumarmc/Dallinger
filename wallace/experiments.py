"""The base experiment class."""

from wallace.models import Network, Node
from wallace.nodes import Agent
import random
import inspect


class Experiment(object):

    def __init__(self, session):
        from recruiters import PsiTurkRecruiter
        self.task = "Experiment title"
        self.session = session
        self.practice_repeats = 0
        self.experiment_repeats = 0
        self.recruiter = PsiTurkRecruiter

    def setup(self):
        # Create the networks if they don't already exist.
        if not self.networks():
            for _ in range(self.practice_repeats):
                network = self.network()
                network.role = "practice"
                self.save(network)
            for _ in range(self.experiment_repeats):
                network = self.network()
                network.role = "experiment"
                self.save(network)

    def networks(self, role="all"):
        if role == "all":
            return Network.query.all()
        else:
            return Network\
                .query\
                .filter_by(role=role)\
                .order_by(Network.creation_time)\
                .all()

    def save(self, *objects):
        if len(objects) > 0:
            self.session.add_all(objects)
        self.session.commit()

    def newcomer_arrival_trigger(self, newcomer):
        pass

    def transmission_reception_trigger(self, transmissions):
        # Mark transmissions as received
        for t in transmissions:
            t.mark_received()

    def information_creation_trigger(self, info):
        self.save(info.origin)

    def step(self):
        pass

    def create_agent_trigger(self, agent, network):
        network.add_agent(agent)
        self.process(network).step()

    def assign_agent_to_participant(self, participant_uuid):

        networks = set(self.networks())
        participant_nodes = set(Node.query.filter_by(participant_uuid=participant_uuid).all())
        participated_networks = set([node.network for node in participant_nodes])
        available_networks = networks - participated_networks
        legal_networks = [net for net in available_networks if not net.full()]

        if not legal_networks:
            raise Exception

        if len(participated_networks) < self.practice_repeats:
            chosen_network = next((net for net in legal_networks if net.role == "practice"))
        else:
            plenitude = [len(net.nodes(type=Agent)) for net in legal_networks]
            min_p = min(plenitude)
            chosen_network = random.choice([net for net, p in zip(legal_networks, plenitude) if p == min_p])

        # Generate the right kind of newcomer.
        if inspect.isclass(self.agent):
            if issubclass(self.agent, Node):
                newcomer = self.agent(participant_uuid=participant_uuid)
            else:
                raise ValueError("{} is not a subclass of Node".format(self.agent))
        else:
            newcomer = self.agent(network=chosen_network)(participant_uuid=participant_uuid)

        self.save(newcomer)

        # Add the newcomer to the network.
        chosen_network.add(newcomer)
        self.create_agent_trigger(agent=newcomer, network=chosen_network)
        return newcomer

    def is_experiment_over(self):
        return all([net.full() for net in self.networks()])

    def participant_completion_trigger(self, participant_uuid=None):

        self.participant_attention_check(participant_uuid=participant_uuid)

        if self.is_experiment_over():
            # If the experiment is over, stop recruiting and export the data.
            self.recruiter().close_recruitment()
        else:
            # Otherwise recruit a new participant.
            self.recruiter().recruit_new_participants(n=1)

    def bonus(self, participant_uuid=None):
        """Compute the bonus for the given participant.
        This is called automatically when a participant finishes,
        it is called immediately prior to the participant_completion_trigger"""
        return 0

    def bonus_reason(self):
        return "Thank for participating! Here is your bonus."

    def participant_attention_check(self, participant_uuid=None):
        """
        Perform a check on a participant to see if they have passed
        some sort of attention check. If they fail the check, you
        may wish to fail their nodes.
        """
        pass
