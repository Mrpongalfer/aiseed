import pytest
import asyncio
from nexus_seed.services.main_brain import MainBrain
from nexus_seed.utils.event_bus import EventBus

@pytest.fixture
def event_bus():
    return EventBus()

@pytest.fixture
def main_brain(event_bus):
    return MainBrain(event_bus)

@pytest.mark.asyncio
async def test_generate_response(main_brain):
    response = await main_brain.generate_response("Hello, AI!")
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_train_random_forest(main_brain):
    data = [[1, 2], [3, 4], [5, 6], [7, 8]]
    labels = [0, 1, 0, 1]
    result = await main_brain.train_random_forest(data, labels)
    assert "successfully" in result

@pytest.mark.asyncio
async def test_predict_random_forest(main_brain):
    data = [[1, 2], [3, 4], [5, 6], [7, 8]]
    labels = [0, 1, 0, 1]
    await main_brain.train_random_forest(data, labels)
    predictions = await main_brain.predict_random_forest([[2, 3]])
    assert "Predictions" in predictions

@pytest.mark.asyncio
async def test_local_model_inference(main_brain):
    prompt = "What is the capital of France?"
    response = await main_brain.local_model_inference(prompt)
    assert isinstance(response, str)
    assert len(response) > 0
