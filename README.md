

# 🚀 ViralFlow AI: Multi-Agent Content Management System

![ViralFlow AI Banner](https://raw.githubusercontent.com/sanhariharan/ViralFlow.ai/main/asset.png)

A full-stack, production-ready multi-agent AI system for **LLM-powered content management**. Generate, optimize, and schedule platform-specific social media content with visuals—powered by LangGraph, Groq, and Tavily.

---

## ✨ Features

- **🧠 Multi-Agent Orchestration**: LangGraph coordinates specialized agents for each task.
- **📱 Platform Adaptation**: Customizes content for Twitter, Instagram, LinkedIn, YouTube, and Blogs.
- **📈 Trend Research**: Fetches trending hashtags using Tavily Search.
- **🎯 Optimization**: Refines content for tone, engagement, and SEO.
- **⏰ Scheduling**: Suggests best posting times for each platform.
- **🖼️ Visuals Gallery**: AI-curated images for your posts, powered by Google Serper.
- **⚡ Tech Stack**: FastAPI (Backend), Streamlit (Frontend), Groq (LLM), Tavily (Search), LangGraph (Agents).

---

## 🗂️ Project Structure

```plaintext
CMS-AGENT/
├── backend/
│   ├── app/
│   │   ├── agents/       # Agent logic
│   │   ├── graph/        # LangGraph workflow
│   │   ├── models/       # Pydantic models
│   │   └── utils/        # LLM and Tool setup
│   └── main.py           # FastAPI entry point
├── frontend/
│   └── app.py            # Streamlit UI
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🛠️ Quickstart

1. **Clone & Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2. **Environment Variables**
    Create a .env file in the root directory and add your API keys:
    ```
    GROQ_API_KEY=your_groq_key
    TAVILY_API_KEY=your_tavily_key
    SERPER_API_KEY=your_serper_key
    ```

3. **Run Backend**
    ```bash
    uv run uvicorn backend.main:app --reload
    ```
    Server will start at [http://localhost:8000](http://localhost:8000).

4. **Run Frontend**
    Open a new terminal:
    ```bash
    uv run streamlit run frontend/app.py
    ```
    UI will open at [http://localhost:8501](http://localhost:8501).

---

## 🧩 Agent Workflow

| Agent                | Role                                                                 |
|----------------------|----------------------------------------------------------------------|
| 🧠 Content Understanding | Extracts metadata (intent, audience, tone)                          |
| 🤖 Platform Adapters     | Parallel agents rewrite content for each platform                   |
| 🔥 Hashtag Research      | Finds trending hashtags via Tavily                                  |
| ✨ Optimizer             | Polishes content and integrates hashtags                            |
| ⏰ Scheduler             | Suggests best posting times                                         |
| 🖼️ Visuals Agent         | Finds relevant images for your content using Serper                 |

---

## 📸 Example UI

![ViralFlow AI UI](https://raw.githubusercontent.com/sanhariharan/ViralFlow.ai/main/assets/ui-screenshot.png)

---

## 💡 Innovative Ideas for Multi-Agent LLM CMS

- **Automated Content Calendar**: Agents collaborate to plan, generate, and schedule posts for weeks in advance.
- **Brand Consistency Agent**: Ensures all content matches brand guidelines and tone.
- **Sentiment Analysis Agent**: Analyzes audience reactions and adapts future content.
- **Localization Agent**: Translates and adapts content for different regions/languages.
- **Compliance Agent**: Checks content for legal, copyright, or platform policy violations.
- **A/B Testing Agent**: Generates multiple versions and tracks engagement to optimize future posts.
- **User Feedback Loop**: Integrates feedback from analytics to continuously improve content.

---

## 🛡️ License

MIT

---

###### ⚡ Powered by LangGraph, Groq & Tavily

---

