import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from backend.app.models.state import AgentState

def visuals_agent(state: AgentState):
    """
    Generates a search query for visuals and fetches images using Google Serper.
    """
    print("--- VISUALS AGENT ---")
    
    # 1. Check if Serper API key is set
    if not os.getenv("SERPER_API_KEY"):
        print("Skipping visuals: SERPER_API_KEY not found.")
        return {"visuals": []}

    metadata = state.get("metadata", {})
    topic = metadata.get("topic", "general topic")
    keywords = metadata.get("keywords", [])
    
    # 2. Generate Search Query using Groq
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    prompt = ChatPromptTemplate.from_template(
        """
        You are a creative director. Based on the topic '{topic}' and keywords {keywords},
        generate a SINGLE, descriptive Google Image search query to find high-quality, aesthetic images 
        suitable for social media posts.
        
        Return ONLY the search query string. No quotes, no explanations.
        """
    )
    
    chain = prompt | llm | StrOutputParser()
    try:
        search_query = chain.invoke({"topic": topic, "keywords": keywords}).strip()
        print(f"Visuals Search Query: {search_query}")
        
        # 3. Search using Serper
        search = GoogleSerperAPIWrapper(type="images", k=4)
        results = search.results(search_query)
        
        image_urls = []
        if "images" in results:
            image_urls = [img["imageUrl"] for img in results["images"][:4]]
            
        return {"visuals": image_urls}
        
    except Exception as e:
        print(f"Error in Visuals Agent: {e}")
        return {"visuals": []}
