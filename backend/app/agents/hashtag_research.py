from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from backend.app.utils.llm import get_llm
from backend.app.utils.tools import get_tavily_search

def hashtag_research_agent(state):
    """
    Fetches trending hashtags using Tavily and LLM.
    """
    print("--- HASHTAG RESEARCH AGENT ---")
    metadata = state.get("metadata", {})
    platforms = state.get("platforms", [])
    
    topic = metadata.get("topic", "")
    keywords = metadata.get("keywords", [])
    
    tavily = get_tavily_search()
    llm = get_llm()
    
    # 1. Search for trends
    search_query = f"trending hashtags for {topic} {' '.join(keywords)}"
    try:
        search_results = tavily.invoke(search_query)
    except Exception as e:
        print(f"Tavily search failed: {e}")
        search_results = []
        
    # 2. Generate hashtags per platform
    parser = JsonOutputParser()
    
    prompt = ChatPromptTemplate.from_template(
        """
        Based on the following search results and topic, generate a list of optimized hashtags for each platform.
        
        Topic: {topic}
        Keywords: {keywords}
        Search Results: {search_results}
        Target Platforms: {platforms}
        
        Return a JSON object where keys are platform names (lowercase) and values are lists of hashtags (strings).
        Example:
        {{
            "twitter": ["#tag1", "#tag2"],
            "instagram": ["#tag1", "#tag2", ...]
        }}
        
        {format_instructions}
        """
    )
    
    chain = prompt | llm | parser
    
    try:
        hashtags = chain.invoke({
            "topic": topic,
            "keywords": keywords,
            "search_results": search_results,
            "platforms": platforms,
            "format_instructions": parser.get_format_instructions()
        })
        return {"hashtags": hashtags}
    except Exception as e:
        print(f"Error in Hashtag Agent: {e}")
        return {"hashtags": {p: [] for p in platforms}}
