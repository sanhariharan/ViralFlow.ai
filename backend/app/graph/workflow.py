from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from backend.app.models.state import AgentState

from backend.app.agents.content_understanding import content_understanding_agent
from backend.app.agents.platform_adapters import (
    twitter_agent, instagram_agent, linkedin_agent, youtube_agent, blog_agent
)
from backend.app.agents.hashtag_research import hashtag_research_agent
from backend.app.agents.optimizer import content_optimizer_agent
from backend.app.agents.scheduler import scheduling_advisor_agent
from backend.app.agents.visuals import visuals_agent

def create_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("content_understanding", content_understanding_agent)
    
    workflow.add_node("twitter_adapter", twitter_agent)
    workflow.add_node("instagram_adapter", instagram_agent)
    workflow.add_node("linkedin_adapter", linkedin_agent)
    workflow.add_node("youtube_adapter", youtube_agent)
    workflow.add_node("blog_adapter", blog_agent)
    
    workflow.add_node("hashtag_research", hashtag_research_agent)
    workflow.add_node("visuals_search", visuals_agent)
    workflow.add_node("content_optimizer", content_optimizer_agent)
    workflow.add_node("scheduling_advisor", scheduling_advisor_agent)
    
    # Set entry point
    workflow.set_entry_point("content_understanding")
    
    # Conditional edges to parallel platform adapters
    def route_to_platforms(state):
        selected_platforms = state.get("platforms", [])
        # Map platform names to node names
        routes = []
        if "twitter" in selected_platforms:
            routes.append("twitter_adapter")
        if "instagram" in selected_platforms:
            routes.append("instagram_adapter")
        if "linkedin" in selected_platforms:
            routes.append("linkedin_adapter")
        if "youtube" in selected_platforms:
            routes.append("youtube_adapter")
        if "blog" in selected_platforms:
            routes.append("blog_adapter")
            
        # Always run research agents
        routes.append("hashtag_research")
        routes.append("visuals_search")
        
        return routes

    # Add edges from content understanding to platform adapters
    workflow.add_conditional_edges(
        "content_understanding",
        route_to_platforms,
        {
            "twitter_adapter": "twitter_adapter",
            "instagram_adapter": "instagram_adapter",
            "linkedin_adapter": "linkedin_adapter",
            "youtube_adapter": "youtube_adapter",
            "blog_adapter": "blog_adapter",
            "hashtag_research": "hashtag_research",
            "visuals_search": "visuals_search"
        }
    )
    
    # All adapters go to hashtag research (synchronization point)
    # Note: In LangGraph, we can just point them all to the next node.
    # However, to run hashtag research in parallel or after, we need to be careful.
    # The prompt says: "Step 4 – Hashtag Agent (Tavily) Gets hashtags per platform."
    # "Step 5 – Optimizer Agent Improves each output; merges hashtags."
    
    # We can run hashtag research in parallel with adapters, OR after them.
    # Let's run it after adapters to keep it simple, or we can make it a separate branch from content_understanding.
    # Let's make hashtag_research run after content_understanding as well, in parallel with adapters?
    # No, the prompt implies a flow. Let's gather everything at the optimizer.
    
    # Actually, hashtag research depends on metadata (topic/keywords), not the drafted content.
    # So it can run in parallel with adapters.
    
    # workflow.add_edge("content_understanding", "hashtag_research") # Removed as it is now in conditional edges
    
    # Now we need to join everything at the optimizer.
    # LangGraph waits for all parent nodes to finish before executing a node if it has multiple incoming edges?
    # No, standard LangGraph behavior is it runs when ANY incoming edge fires unless configured otherwise.
    # But we want to wait for ALL selected adapters AND hashtag research.
    
    # To simplify, let's serialize: Adapters -> Hashtag -> Optimizer -> Scheduler
    # But we want parallel adapters.
    
    # Let's have all adapters point to a "join" node or just point to hashtag_research?
    # If we point all adapters to hashtag_research, it might run multiple times.
    
    # Better approach:
    # Content Understanding -> [Adapters (Parallel), Hashtag Research (Parallel)] -> Optimizer -> Scheduler
    
    # But Optimizer needs both Adapter outputs AND Hashtags.
    # So Optimizer should be the join point.
    
    workflow.add_edge("twitter_adapter", "content_optimizer")
    workflow.add_edge("instagram_adapter", "content_optimizer")
    workflow.add_edge("linkedin_adapter", "content_optimizer")
    workflow.add_edge("youtube_adapter", "content_optimizer")
    workflow.add_edge("blog_adapter", "content_optimizer")
    
    workflow.add_edge("hashtag_research", "content_optimizer")
    workflow.add_edge("visuals_search", "content_optimizer")
    
    # Optimizer -> Scheduler -> End
    workflow.add_edge("content_optimizer", "scheduling_advisor")
    workflow.add_edge("scheduling_advisor", END)
    
    return workflow.compile()
