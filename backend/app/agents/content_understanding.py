from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from backend.app.utils.llm import get_llm
from backend.app.models.schemas import ContentMetadata

def content_understanding_agent(state):
    """
    Analyzes user's input to extract structured metadata.
    """
    print("--- CONTENT UNDERSTANDING AGENT ---")
    base_content = state["base_content"]
    tone = state["tone"]
    
    llm = get_llm()
    
    parser = JsonOutputParser(pydantic_object=ContentMetadata)
    
    prompt = ChatPromptTemplate.from_template(
        """
        Analyze the following content and extract structured metadata.
        
        Content: {content}
        Desired Tone: {tone}
        
        Return a JSON object with the following keys:
        - intent: What is the goal of this post?
        - audience: Who is the target audience?
        - keywords: List of top 5 keywords.
        - topic: The main topic.
        - tone: The detected or requested tone.
        - summary: A brief summary of the content.
        
        {format_instructions}
        """
    )
    
    chain = prompt | llm | parser
    
    try:
        metadata = chain.invoke({
            "content": base_content,
            "tone": tone,
            "format_instructions": parser.get_format_instructions()
        })
        return {"metadata": metadata}
    except Exception as e:
        print(f"Error in Content Understanding Agent: {e}")
        # Fallback metadata
        return {"metadata": {
            "intent": "general",
            "audience": "general",
            "keywords": [],
            "topic": "general",
            "tone": tone,
            "summary": base_content[:100]
        }}
