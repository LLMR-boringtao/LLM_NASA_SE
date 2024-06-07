import warnings
warnings.filterwarnings("ignore")

from pytest import mark
from backend.agents.conop import COPOP as Agent


@mark.agent
@mark.copop
class AgentTests:
    def test_agent_behaviours(self):
        request = """Extract the data from the request and context."""
        context = """"""
        agent_instance = Agent(request, context)
        result = agent_instance.actor()
        print(result)
        assert result is not None