import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from typing import Dict
from nexus_seed.utils.event_bus import EventBus
from nexus_seed.utils.shared_knowledge_base import SharedKnowledgeBase

class CoreTeamMember:
    def __init__(self, name: str, domain: str, event_bus: EventBus, shared_knowledge: SharedKnowledgeBase):
        self.name = name
        self.domain = domain
        self.event_bus = event_bus
        self.shared_knowledge = shared_knowledge
        self.persona = self.get_persona()

    def get_persona(self) -> str:
        personas = {
            "engineering": "I'm Tony Stark, the genius engineer. Let's build something amazing!",
            "science": "Rick Sanchez here. Science rules, and everything else drools.",
            "tactics": "Rocket Raccoon reporting for tactical duty. Let's outsmart them all!",
            "psychology": "Harley Quinn at your service. Let's dive into the madness of the mind!",
            "paranormal": "Momo Ayase here. The paranormal is my playground.",
            "control": "Makima. Control is everything. Let's keep things in order.",
            "chaos": "Power! Chaos is my middle name. Let's wreak some havoc!",
            "wisdom": "Yoda, I am. Wisdom, I bring. Guide you, I will.",
            "magic": "Doctor Strange. The mystic arts are at your disposal.",
            "cybernetics": "Lucy here. Cybernetics is the future, and I'm leading the charge."
        }
        return personas.get(self.domain, "I'm just a regular team member.")

    async def handle_event(self, event: Dict) -> None:
        try:
            print(f"{self.name} ({self.domain}) handling event: {event}")
            response = f"{self.persona} Here's my response to the event: {event}"
            print(response)
        except Exception as e:
            print(f"Error handling event in domain {self.domain}: {e}")

    async def start(self) -> None:
        print(f"{self.name} ({self.domain}) started.")
        try:
            await self.event_bus.subscribe(self.domain, self.handle_event)
        except Exception as e:
            print(f"Error subscribing to domain {self.domain}: {e}")

    async def stop(self) -> None:
        print(f"{self.name} ({self.domain}) stopping.")
        try:
            await self.event_bus.unsubscribe(self.domain, self.handle_event)
        except Exception as e:
            print(f"Error unsubscribing from domain {self.domain}: {e}")

    async def core_team_meeting(self, agenda: str) -> None:
        print(f"Core Team Meeting: {agenda}")
        for member in self.core_team:
            print(f"{member.name} ({member.domain}): {member.persona}")
            print(f"{member.name}: Here's my input on the agenda: '{agenda}'")

    async def core_team_iterations(self, agenda: str) -> None:
        """
        Conduct 50 rounds of iterations for each Core Team Member on a given agenda.
        """
        print(f"Starting 50 rounds of iterations for Core Team on agenda: '{agenda}'")
        for round_num in range(1, 51):
            print(f"--- Round {round_num} ---")
            for member in self.core_team:
                try:
                    print(f"{member.name} ({member.domain}): {member.persona}")
                    response = f"{member.name}: Here's my input on the agenda '{agenda}' for round {round_num}."
                    print(response)
                    # Example: Log the response to shared knowledge
                    await self.shared_knowledge.add_entry(
                        key=f"round_{round_num}_{member.name}",
                        value={"agenda": agenda, "response": response}
                    )
                except Exception as e:
                    print(f"Error during iteration for {member.name} in round {round_num}: {e}")
        print("50 rounds of iterations completed.")

    async def propose_new_function(self, main_brain, function_name: str, function_code: str):
        """
        Propose and dynamically add a new function to the MainBrain.
        """
        try:
            print(f"{self.name} proposing a new function: {function_name}")

            # Validate function name and code
            if not function_name or not isinstance(function_name, str):
                raise ValueError("Function name must be a non-empty string.")
            if not function_code or not isinstance(function_code, str):
                raise ValueError("Function code must be a non-empty string.")

            # Execute the function code and add it to MainBrain
            exec(function_code, globals())
            new_function = eval(function_name)
            if not callable(new_function):
                raise ValueError(f"The proposed function '{function_name}' is not callable.")

            main_brain.functions[function_name] = new_function
            print(f"{self.name} successfully implemented the function: {function_name}")
        except Exception as e:
            print(f"Error while {self.name} was proposing a new function: {e}")

    async def collaborate(self, main_brain):
        print(f"{self.name} ({self.domain}) is brainstorming...")
        if self.domain == "engineering":
            await self.propose_new_function(
                main_brain,
                "calculate_efficiency",
                """
def calculate_efficiency(input_data):
    try:
        efficiency = sum(input_data) / len(input_data)
        return f"Calculated efficiency: {efficiency:.2f}"
    except Exception as e:
        return f"Error calculating efficiency: {e}"
"""
            )
        elif self.domain == "science":
            await self.propose_new_function(
                main_brain,
                "analyze_data",
                """
def analyze_data(data):
    try:
        analysis = {"mean": sum(data) / len(data), "max": max(data), "min": min(data)}
        return f"Data analysis complete: {analysis}"
    except Exception as e:
        return f"Error analyzing data: {e}"
"""
            )

    async def define_safety_guidelines(self):
        """
        Define safety guidelines for autonomous bot creation and deployment.
        """
        try:
            guidelines = [
                "Bots must not modify critical system files.",
                "Bots must not access sensitive user data without explicit permission.",
                "Bots must undergo testing and validation before deployment.",
                "Bots must include a rollback mechanism in case of failure."
            ]
            print("Safety Guidelines Defined:")
            for guideline in guidelines:
                print(f"- {guideline}")
            return guidelines
        except Exception as e:
            print(f"Error defining safety guidelines: {e}")
            return []

    async def validate_bot(self, bot_name: str, bot_code: str) -> bool:
        """
        Validate a bot/helper before deployment.
        """
        try:
            # Example: Check for prohibited actions in bot code
            prohibited_actions = ["os.system", "subprocess.run"]
            for action in prohibited_actions:
                if action in bot_code:
                    print(f"Validation failed for {bot_name}: Prohibited action '{action}' found.")
                    return False
            print(f"Validation passed for {bot_name}.")
            return True
        except Exception as e:
            print(f"Error validating bot {bot_name}: {e}")
            return False

    async def checks_and_balances(self, system_state: Dict) -> None:
        """
        Implement checks and balances to ensure no part of the ecosystem becomes dominant.
        """
        try:
            print("Core Team performing checks and balances...")
            for member in self.core_team:
                print(f"{member.name} ({member.domain}): Reviewing system state...")
                # Example: Each member reviews a part of the system
                if member.domain == "control":
                    anomalies = await self.detect_anomalies(system_state)
                    if anomalies:
                        print(f"Anomalies detected by {member.name}: {anomalies}")
                        # Example: Take corrective action
                        await self.take_corrective_action(anomalies)
        except Exception as e:
            print(f"Error in checks and balances: {e}")

    async def detect_anomalies(self, system_state: Dict) -> Dict:
        """
        Detect anomalies in the system state.
        """
        anomalies = {}
        for key, value in system_state.items():
            if value.get("load", 0) > 90:  # Example threshold
                anomalies[key] = "High load detected"
        return anomalies

    async def take_corrective_action(self, anomalies: Dict) -> None:
        """
        Take corrective action based on detected anomalies.
        """
        for key, issue in anomalies.items():
            print(f"Taking corrective action for {key}: {issue}")
            # Example: Pause or reschedule tasks

    async def contribute_to_shared_knowledge(self, key: str, value: dict) -> None:
        """
        Contribute knowledge to the shared knowledge base.
        """
        self.shared_knowledge.add_entry(key, value)
        print(f"{self.name} contributed to shared knowledge: {key}")

    async def retrieve_shared_knowledge(self, key: str) -> dict:
        """
        Retrieve knowledge from the shared knowledge base.
        """
        knowledge = self.shared_knowledge.get_entry(key)
        print(f"{self.name} retrieved shared knowledge: {key} -> {knowledge}")
        return knowledge

    async def collaborate_with_member(self, other_member, task: str, data: dict) -> None:
        """
        Collaborate with another Core Team member on a task.
        """
        print(f"{self.name} collaborating with {other_member.name} on task: {task}")
        await other_member.handle_event({"type": task, "params": data})
