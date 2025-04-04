import asyncio
import json
from nexus_seed.kernel import Kernel
from nexus_seed.utils.event_bus import EventBus
from nexus_seed.services.main_brain import MainBrain

async def test_main_brain(main_brain: MainBrain):
    print("Testing MainBrain...")
    results = []

    # Test Protocol Omnitide
    try:
        result = await main_brain.protocol_omnitide()
        results.append(f"Protocol Omnitide: {result}")
    except Exception as e:
        results.append(f"Protocol Omnitide failed: {e}")

    # Test Omnitide syncnexus pppowerpong
    try:
        result = await main_brain.omnitide_syncnexus_pppowerpong()
        results.append(f"Omnitide syncnexus pppowerpong: {result}")
    except Exception as e:
        results.append(f"Omnitide syncnexus pppowerpong failed: {e}")

    # Test Blah Blah Blah
    try:
        result = await main_brain.blah_blah_blah()
        results.append(f"Blah Blah Blah: {result}")
    except Exception as e:
        results.append(f"Blah Blah Blah failed: {e}")

    return results

async def test_random_forest(main_brain: MainBrain):
    """
    Test the Random Forest model training and prediction.
    """
    print("Testing Random Forest...")
    results = []

    # Test training
    try:
        data = [[1, 2], [3, 4], [5, 6], [7, 8]]
        labels = [0, 1, 0, 1]
        train_result = await main_brain.train_random_forest(data, labels)
        results.append(f"Train Random Forest: {train_result}")
    except Exception as e:
        results.append(f"Train Random Forest failed: {e}")

    # Test prediction
    try:
        test_data = [[2, 3], [6, 7]]
        predict_result = await main_brain.predict_random_forest(test_data)
        results.append(f"Predict Random Forest: {predict_result}")
    except Exception as e:
        results.append(f"Predict Random Forest failed: {e}")

    return results

async def test_mistral_inference(main_brain: MainBrain):
    """
    Test the Mistral Instruct model inference.
    """
    print("Testing Mistral Instruct model...")
    results = []

    try:
        prompt = "Explain the concept of adaptive intelligence in simple terms."
        response = await main_brain.mistral_inference(prompt)
        results.append(f"Mistral Inference Response: {response}")
    except Exception as e:
        results.append(f"Mistral Inference failed: {e}")

    return results

async def test_core_team(event_bus: EventBus):
    print("Testing Core Team...")
    results = []

    # Publish test events for each domain
    test_events = [
        {"domain": "engineering", "event": {"type": "test_event", "data": "Engineering Test"}},
        {"domain": "science", "event": {"type": "test_event", "data": "Science Test"}},
        {"domain": "chaos", "event": {"type": "test_event", "data": "Chaos Test"}},
    ]

    for test in test_events:
        try:
            await event_bus.publish(test["domain"], test["event"])
            results.append(f"Event published to {test['domain']}: {test['event']}")
        except Exception as e:
            results.append(f"Failed to publish event to {test['domain']}: {e}")

    return results

async def test_event_bus(event_bus: EventBus):
    print("Testing EventBus...")
    results = []

    # Test event publishing and subscription
    async def test_callback(event):
        print(f"Test callback received event: {event}")
        results.append(f"Test callback received event: {event}")

    try:
        event_bus.subscribe("test_event", test_callback)
        await event_bus.publish("test_event", {"type": "test_event", "data": "Test Data"})
        results.append("EventBus test passed.")
    except Exception as e:
        results.append(f"EventBus test failed: {e}")

    return results

async def test_kernel():
    print("Testing Kernel...")
    kernel = Kernel("/home/pong/Desktop/AIseed/config/system_config.json")
    await kernel.start()

    # Test MainBrain
    main_brain = next(service for service in kernel.services if isinstance(service, MainBrain))
    main_brain_results = await test_main_brain(main_brain)

    # Test Random Forest
    random_forest_results = await test_random_forest(main_brain)

    # Test Mistral Inference
    mistral_results = await test_mistral_inference(main_brain)

    # Test Core Team
    core_team_results = await test_core_team(kernel.event_bus)

    # Test EventBus
    event_bus_results = await test_event_bus(kernel.event_bus)

    # Stop the kernel
    await kernel.start()

    return {
        "main_brain": main_brain_results,
        "random_forest": random_forest_results,
        "mistral_inference": mistral_results,
        "core_team": core_team_results,
        "event_bus": event_bus_results,
    }

async def main():
    print("Starting system tests...")
    results = await test_kernel()

    # Log results
    with open("/home/pong/Desktop/AIseed/logs/test_results.log", "w") as log_file:
        json.dump(results, log_file, indent=4)

    print("System tests completed. Results logged to /home/pong/Desktop/AIseed/logs/test_results.log.")

if __name__ == "__main__":
    asyncio.run(main())
