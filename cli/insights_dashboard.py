from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, Static
from textual.containers import Container

class InsightsDashboard(App):
    CSS_PATH = "styles.css"

    def __init__(self, insights: dict):
        super().__init__()
        self.insights = insights

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(
            Static(self.render_insights(), id="insights_box"),
        )

    def render_insights(self) -> str:
        """
        Render insights dynamically.
        """
        return "\n".join([f"{key}: {value}" for key, value in self.insights.items()])

async def main():
    insights = {
        "Pipeline Status": "Success",
        "Deployment Status": "In Progress",
        "Last Commit": "Deploying changes",
    }
    app = InsightsDashboard(insights)
    await app.run_async()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
