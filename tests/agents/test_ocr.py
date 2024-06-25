import warnings
warnings.filterwarnings("ignore")

from pytest import mark
from backend.agents.ocr import OCRAgent as Agent

@mark.agent
@mark.ocr
class AgentTests:
    def test_agent_behaviours(self):
        request = """/Users/boringtao/Projects/NASA/backend/agents/data/market"""
        agent_instance = Agent(request)
        result = agent_instance.actor()
        print(result)
        assert result is not None