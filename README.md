# Twin Talk Engine

This is an AI-powered consultant service designed to act as a smart, conversational guide for the Festival Digital Twin Manager.

## Getting Started

Follow these steps to set up your local development environment:

1. **Install `uv`**: We use `uv` for lightning-fast Python package and project management.
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Sync Dependencies**: Create the virtual environment and install dependencies.
   ```bash
   uv sync
   ```

3. **Configure Environment Variables**: Copy the `.env.example` file to a new file named `.env` and add your Groq API key and preferred model name.
   ```bash
   cp .env.example .env
   ```

4. **Run the Application**: Start the FastAPI server with live reloading.
   ```bash
   uv run python main.py
   ```
   *(Alternatively, run the Uvicorn command directly:)*
   ```bash
   uv run uvicorn src.twin_talk_engine.api:app --reload
   ```
