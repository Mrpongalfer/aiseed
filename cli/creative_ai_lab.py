import sys
import os
import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Input, Button, Static, Select
from textual.containers import Container, ScrollableContainer
from textual.reactive import reactive
from nexus_seed.services.main_brain import MainBrain
from nexus_seed.utils.event_bus import EventBus

class CreativeAILab(App):
    CSS_PATH = "styles.css"  # Optional: Add a CSS file for styling

    def __init__(self, event_bus: EventBus, main_brain: MainBrain):
        super().__init__()
        self.event_bus = event_bus
        self.main_brain = main_brain
        self.output = reactive("Welcome to the Creative AI Lab!\n")
        self.selected_algorithm = None
        self.selected_template = None
        self.ai_parameters = {"learning_rate": 0.001, "epochs": 10, "batch_size": 32}

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            ScrollableContainer(Label(self.output, id="output_window"), id="lab_output"),
            Static(self.render_menu(), id="menu_box"),
        )

    def render_menu(self) -> str:
        """
        Render the Creative AI Lab menu dynamically.
        """
        return """
        Creative AI Lab:
        1. Select Algorithm
        2. Choose AI Template
        3. Adjust AI Parameters
        4. Train AI Model
        5. Deploy AI Agent
        6. Save AI Model
        7. Load AI Model
        8. Combine AI Functions
        9. Autonomous Bot Creation
        10. System Evolution Viewer
        11. Enable Drag-and-Drop
        12. Shared Knowledge Viewer
        0. Exit Creative AI Lab
        """

    async def on_key(self, event):
        """
        Handle key presses to navigate menus and execute actions.
        """
        key = event.key
        if key.isdigit():
            await self.handle_menu_selection(int(key))

    async def handle_menu_selection(self, selection: int):
        """
        Handle menu selection and execute actions.
        """
        if selection == 1:
            await self.select_algorithm()
        elif selection == 2:
            await self.choose_template()
        elif selection == 3:
            await self.adjust_parameters()
        elif selection == 4:
            await self.train_model()
        elif selection == 5:
            await self.deploy_agent()
        elif selection == 6:
            await self.save_model()
        elif selection == 7:
            await self.load_model()
        elif selection == 8:
            await self.combine_functions()
        elif selection == 9:
            await self.autonomous_bot_creation()
        elif selection == 10:
            await self.show_system_evolution_viewer()
        elif selection == 11:
            await self.enable_drag_and_drop()
        elif selection == 12:
            await self.show_shared_knowledge_viewer()
        elif selection == 0:
            self.exit_lab()
        else:
            self.output += "\nInvalid selection. Try again."
        self.refresh()

    async def select_algorithm(self):
        """
        Allow the user to select an algorithm from a predefined list.
        """
        algorithms = ["Random Forest", "Neural Network", "Support Vector Machine", "K-Nearest Neighbors"]
        print("Available Algorithms:")
        for i, algo in enumerate(algorithms, 1):
            print(f"{i}. {algo}")
        choice = int(input("Select an algorithm (1-4): "))
        self.selected_algorithm = algorithms[choice - 1]
        self.output += f"\nSelected Algorithm: {self.selected_algorithm}"

    async def choose_template(self):
        """
        Allow the user to choose an AI template from a predefined list.
        """
        templates = ["Chatbot", "Image Classifier", "Recommendation System", "Sentiment Analyzer"]
        print("Available Templates:")
        for i, template in enumerate(templates, 1):
            print(f"{i}. {template}")
        choice = int(input("Select a template (1-4): "))
        self.selected_template = templates[choice - 1]
        self.output += f"\nSelected Template: {self.selected_template}"

    async def adjust_parameters(self):
        """
        Allow the user to adjust AI parameters.
        """
        print("Current Parameters:")
        for param, value in self.ai_parameters.items():
            print(f"{param}: {value}")
        for param in self.ai_parameters.keys():
            new_value = input(f"Enter new value for {param} (or press Enter to keep {self.ai_parameters[param]}): ")
            if new_value:
                self.ai_parameters[param] = float(new_value)
        self.output += f"\nUpdated Parameters: {self.ai_parameters}"

    async def train_model(self):
        """
        Train the AI model based on the selected algorithm and parameters.
        """
        if not self.selected_algorithm:
            self.output += "\nPlease select an algorithm first."
            return
        self.output += f"\nTraining {self.selected_algorithm} model with parameters: {self.ai_parameters}..."
        # Example: Simulate training
        await asyncio.sleep(3)
        self.output += f"\n{self.selected_algorithm} model trained successfully!"

    async def deploy_agent(self):
        """
        Deploy an AI agent based on the selected template.
        """
        if not self.selected_template:
            self.output += "\nPlease choose a template first."
            return
        self.output += f"\nDeploying AI Agent: {self.selected_template}..."
        # Example: Simulate deployment
        await asyncio.sleep(2)
        self.output += f"\nAI Agent '{self.selected_template}' deployed successfully!"

    async def save_model(self):
        """
        Save the trained AI model to a file.
        """
        model_name = input("Enter a name for the model: ")
        self.output += f"\nSaving model '{model_name}'..."
        # Example: Simulate saving
        await asyncio.sleep(1)
        self.output += f"\nModel '{model_name}' saved successfully!"

    async def load_model(self):
        """
        Load a saved AI model from a file.
        """
        model_name = input("Enter the name of the model to load: ")
        self.output += f"\nLoading model '{model_name}'..."
        # Example: Simulate loading
        await asyncio.sleep(1)
        self.output += f"\nModel '{model_name}' loaded successfully!"

    async def combine_functions(self):
        """
        Combine AI functions to create a custom AI agent.
        """
        functions = ["Text Generation", "Image Recognition", "Data Analysis", "Anomaly Detection"]
        print("Available Functions:")
        for i, func in enumerate(functions, 1):
            print(f"{i}. {func}")
        choices = input("Select functions to combine (comma-separated, e.g., 1,3): ")
        selected_functions = [functions[int(choice) - 1] for choice in choices.split(",")]
        self.output += f"\nCombining functions: {', '.join(selected_functions)}..."
        # Example: Simulate function combination
        await asyncio.sleep(2)
        self.output += f"\nCustom AI Agent with functions {', '.join(selected_functions)} created successfully!"

    async def autonomous_bot_creation(self):
        """
        Allow the system to autonomously create, test, and deploy bots/helpers.
        """
        self.output += "\nStarting autonomous bot creation..."
        try:
            # Recognize patterns and identify tasks
            patterns = await self.main_brain.recognize_patterns()
            self.output += f"\nRecognized Patterns: {patterns}"

            # Create bots/helpers for identified tasks
            for pattern in patterns:
                bot_name = f"Bot_{pattern['task']}"
                bot_code = f"""
async def {bot_name}(params):
    # Example bot logic
    print(f"Executing {bot_name} with params: {{params}}")
    return "Task completed successfully."
"""
                await self.main_brain.register_function(bot_name, bot_code)
                self.output += f"\nCreated bot: {bot_name}"

            # Test and deploy bots
            for pattern in patterns:
                bot_name = f"Bot_{pattern['task']}"
                test_result = await self.main_brain.execute_task(bot_name, pattern["params"])
                self.output += f"\nTest result for {bot_name}: {test_result}"
                self.output += f"\nDeploying {bot_name}..."
                await self.main_brain.deploy_ai_agent(bot_name, pattern["params"])
                self.output += f"\n{bot_name} deployed successfully."

        except Exception as e:
            self.output += f"\nError during autonomous bot creation: {e}"

    async def show_system_evolution_viewer(self):
        """
        Display the System Evolution Viewer with shared knowledge and collaboration logs.
        """
        self.output += "\nOpening System Evolution Viewer..."
        try:
            # Display shared knowledge
            shared_knowledge = self.main_brain.shared_knowledge.list_entries()
            self.output += f"\nShared Knowledge Base:\n{shared_knowledge}"

            # Display collaboration logs
            self.output += "\nCollaboration Logs:\n"
            for member in self.main_brain.core_team:
                self.output += f"{member.name} ({member.domain}) collaborated on tasks.\n"
        except Exception as e:
            self.output += f"\nError displaying System Evolution Viewer: {e}"

    async def enable_drag_and_drop(self):
        """
        Enable drag-and-drop interactions for modules and workflows.
        """
        self.output += "\nEnabling drag-and-drop interactions..."
        try:
            # Example: Simulate drag-and-drop functionality
            print("Drag a module to rearrange it:")
            modules = ["Module A", "Module B", "Module C"]
            print(f"Available Modules: {', '.join(modules)}")
            source = input("Enter the module to move: ")
            target = input("Enter the target position: ")
            modules.remove(source)
            modules.insert(int(target), source)
            self.output += f"\nUpdated Module Order: {', '.join(modules)}"
        except Exception as e:
            self.output += f"\nError enabling drag-and-drop: {e}"

    async def adapt_modules_in_real_time(self):
        """
        Adapt modules in real time based on system performance.
        """
        self.output += "\nAdapting modules in real time..."
        try:
            while True:
                # Fetch system performance metrics
                metrics = await self.main_brain.get_system_metrics()
                print(f"System Metrics: {metrics}")
                # Adapt modules based on metrics
                if metrics["cpu_percent"] > 80:
                    print("High CPU usage detected. Reallocating resources...")
                elif metrics["memory_percent"] > 75:
                    print("High memory usage detected. Optimizing memory allocation...")
                await asyncio.sleep(5)  # Check every 5 seconds
        except Exception as e:
            self.output += f"\nError adapting modules: {e}"

    async def show_shared_knowledge_viewer(self):
        """
        Display the Shared Knowledge Viewer with intents, tasks, and outcomes.
        """
        self.output += "\nOpening Shared Knowledge Viewer..."
        try:
            # Retrieve intent logs
            intent_logs = self.main_brain.shared_knowledge.get_entry("intent_logs")
            if not intent_logs:
                self.output += "\nNo intents logged yet."
                return

            # Display intent logs
            self.output += "\nIntent Logs:\n"
            for log in intent_logs:
                self.output += f"Intent: {log['intent']} -> Task: {log['task']} -> Outcome: {log['outcome']}\n"
        except Exception as e:
            self.output += f"\nError displaying Shared Knowledge Viewer: {e}"

    def exit_lab(self):
        """
        Exit the Creative AI Lab.
        """
        self.output += "\nExiting Creative AI Lab. Goodbye!"
        self.exit()

async def main():
    """
    Initialize and run the Creative AI Lab.
    """
    event_bus = EventBus()
    main_brain = MainBrain(event_bus)
    app = CreativeAILab(event_bus, main_brain)
    try:
        await app.run_async()
    except KeyboardInterrupt:
        print("Shutting down Creative AI Lab...")

if __name__ == "__main__":
    asyncio.run(main())
