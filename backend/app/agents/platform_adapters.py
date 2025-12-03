from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.app.utils.llm import get_llm

def platform_adapter_agent(state, platform):
    """
    Generates platform-specific content.
    """
    print(f"--- PLATFORM ADAPTER AGENT: {platform} ---")
    base_content = state["base_content"]
    metadata = state.get("metadata", {})
    
    llm = get_llm()
    
    instructions = {
        "twitter": "Rewrite in <280 chars. Add a hook. Add a CTA (optional). Include 1-3 placeholders for hashtags.",
        "instagram": "Focus on emotional storytelling. Write an engaging caption. Use line-break formatting. Add placeholders for 20 hashtags.",
        "linkedin": "Use a professional tone. Focus on value delivery. Use bullet points. Add a CTA at the end.",
        "youtube": "Generate a Video Title, SEO Description, and a comma-separated Tag List.",
        "blog": "Write a 300-600 word blog post. SEO-optimized. Include subheadings and a summary paragraph."
    }
    
    instruction = instructions.get(platform.lower(), "Rewrite the content for this platform.")
    
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert social media manager.
        
        Platform: {platform}
        Task: {instruction}
        
        Base Content: {content}
        Metadata: {metadata}
        
        Generate the content for {platform}. Do NOT include hashtags yet, just the text body (unless specified as placeholders).
        """
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        result = chain.invoke({
            "platform": platform,
            "instruction": instruction,
            "content": base_content,
            "metadata": metadata
        })
        
        # Store in state
        current_outputs = state.get("platform_outputs", {})
        current_outputs[platform] = result
        return {"platform_outputs": current_outputs}
        
    except Exception as e:
        print(f"Error in {platform} Adapter: {e}")
        return {}

# Wrapper functions for each platform to be used as nodes
def twitter_agent(state):
    return platform_adapter_agent(state, "twitter")

def instagram_agent(state):
    return platform_adapter_agent(state, "instagram")

def linkedin_agent(state):
    return platform_adapter_agent(state, "linkedin")

def youtube_agent(state):
    return platform_adapter_agent(state, "youtube")

def blog_agent(state):
    return platform_adapter_agent(state, "blog")
