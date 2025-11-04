# Event Planner AI

AI-powered event planning assistant built with CrewAI and Streamlit.

## Setup

1. **Clone and navigate to project**
   ```bash
   git clone https://github.com/lokesht01/Event_Planner_AI.git
   cd Event_Planner_AI
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   
   Create `.env` file:
  API_KEY=your_api_key_here

## Run

```bash
streamlit run app.py
```

Access at `http://localhost:8501`

## Tech Stack

- **CrewAI** - AI agent orchestration
- **Streamlit** - Web interface
- **Python-dotenv** - Environment management

## Project Structure

```
Event_Planner_AI/
├── app.py              # Streamlit UI
├── flow.py             # AI workflow logic
├── requirements.txt    # Dependencies
```
