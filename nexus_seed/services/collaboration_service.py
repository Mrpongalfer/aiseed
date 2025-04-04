from typing import Dict, Any, List

class CollaborationService:
    def __init__(self):
        self.collaboration_sessions: Dict[str, List[str]] = {}

    def start_session(self, session_id: str, participants: List[str]) -> None:
        """
        Start a new collaboration session.
        """
        self.collaboration_sessions[session_id] = participants
        print(f"Collaboration session '{session_id}' started with participants: {participants}")

    def share_task(self, session_id: str, task: Dict[str, Any]) -> None:
        """
        Share a task with all participants in a session.
        """
        if session_id in self.collaboration_sessions:
            participants = self.collaboration_sessions[session_id]
            print(f"Task shared in session '{session_id}' with participants: {participants}")
        else:
            print(f"Session '{session_id}' does not exist.")
