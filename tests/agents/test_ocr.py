import warnings
warnings.filterwarnings("ignore")

from pytest import mark
from backend.plugins.ocr import OCRAgent as Agent

@mark.agent
@mark.ocr
class AgentTests:
    def test_agent_behaviours(self):
        request = """backend/data/nasa/img"""
        agent_instance = Agent(request)
        result = agent_instance.actor()
        print(result)
        assert result is not None