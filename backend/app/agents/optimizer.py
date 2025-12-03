from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.app.utils.llm import get_llm

def content_optimizer_agent(state):
    """
    Refines content and merges hashtags.
    """
    print("--- CONTENT OPTIMIZER AGENT ---")
    platform_outputs = state.get("platform_outputs", {})
    hashtags = state.get("hashtags", {})
    metadata = state.get("metadata", {})
    
    llm = get_llm()
    
    optimized_outputs = {}
    
    for platform, content in platform_outputs.items():
        platform_tags = hashtags.get(platform, [])
        tags_str = " ".join(platform_tags)
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are a final content polisher.
            
            Platform: {platform}
            Draft Content: {content}
            Hashtags to Integrate: {tags}
            Brand Tone: {tone}
            
            Task:
            1. Polish the draft for clarity and engagement.
            2. Ensure the tone matches the brand.
            3. Append or integrate the hashtags naturally (or at the end, depending on platform norms).
            4. Return ONLY the final ready-to-post text.
            """
        )
        
        chain = prompt | llm | StrOutputParser()
        
        try:
            final_content = chain.invoke({
                "platform": platform,
                "content": content,
                "tags": tags_str,
                "tone": metadata.get("tone", "neutral")
            })
            optimized_outputs[platform] = final_content
        except Exception as e:
            print(f"Error optimizing for {platform}: {e}")
            optimized_outputs[platform] = content + f"\n\n{tags_str}"
            
    return {"platform_outputs": optimized_outputs}
