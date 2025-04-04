import asyncpg
from typing import Dict, Any

class PersistenceOverseer:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None

    async def initialize(self):
        """
        Initialize the connection pool.
        """
        self.pool = await asyncpg.create_pool(self.db_url, min_size=1, max_size=10)
        print("Database connection pool initialized.")

    async def save_service_state(self, service_name: str, state: Dict[str, Any]) -> None:
        """
        Save the state of a specific service.
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO service_states (service_name, state) VALUES ($1, $2) "
                "ON CONFLICT (service_name) DO UPDATE SET state = $2",
                service_name, state
            )

    async def load_service_state(self, service_name: str) -> Dict[str, Any]:
        """
        Load the state of a specific service.
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT state FROM service_states WHERE service_name = $1", service_name)
            return row["state"] if row else {}

    async def save_global_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """
        Save a global snapshot of the system state.
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO global_snapshots (snapshot) VALUES ($1)",
                snapshot
            )

    async def load_global_snapshot(self) -> Dict[str, Any]:
        """
        Load the latest global snapshot.
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT snapshot FROM global_snapshots ORDER BY created_at DESC LIMIT 1")
            return row["snapshot"] if row else {}
