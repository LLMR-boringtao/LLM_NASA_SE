import warnings
warnings.filterwarnings("ignore")

from pytest import mark
from backend.agents.extractor import Extractor as Agent


@mark.agent
@mark.extractor
class AgentTests:
    def test_agent_behaviours(self):
        request = """Extract the data from the request and context."""
        context = """"""
        agent_instance = Agent(request, context)
        result = agent_instance.actor()
        print(result)
        assert result is not None