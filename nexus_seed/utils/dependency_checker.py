import importlib

class DependencyChecker:
    @staticmethod
    def check_dependency(module_name: str) -> bool:
        try:
            importlib.import_module(module_name)
            print(f"Dependency '{module_name}' is available.")
            return True
        except ImportError:
            print(f"Dependency '{module_name}' is missing.")
            return False

