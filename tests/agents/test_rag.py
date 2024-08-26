import warnings
warnings.filterwarnings("ignore")

from pytest import mark
from backend.plugins.rag import RAGAgent as Agent


@mark.agent
@mark.rag
class AgentTests:
    def test_agent_behaviours(self):
        request = """backend/data/market"""
        agent_instance = Agent(request)
        result = agent_instance.actor()
        assert result is not None