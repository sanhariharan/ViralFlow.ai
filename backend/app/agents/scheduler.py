from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from backend.app.utils.llm import get_llm

def scheduling_advisor_agent(state):
    """
    Generates posting time suggestions.
    """
    print("--- SCHEDULING ADVISOR AGENT ---")
    platforms = state.get("platforms", [])
    metadata = state.get("metadata", {})
    
    llm = get_llm()
    parser = JsonOutputParser()
    
    prompt = ChatPromptTemplate.from_template(
        """
        Suggest the best posting times for the following platforms based on general best practices and the target audience.
        
        Platforms: {platforms}
        Audience: {audience}
        Topic: {topic}
        
        Return a JSON object where keys are platform names and values are strings describing the best time (e.g., "Tuesday 10 AM").
        
        {format_instructions}
        """
    )
    
    chain = prompt | llm | parser
    
    try:
        schedules = chain.invoke({
            "platforms": platforms,
            "audience": metadata.get("audience", "general"),
            "topic": metadata.get("topic", "general"),
            "format_instructions": parser.get_format_instructions()
        })
        return {"schedules": schedules}
    except Exception as e:
        print(f"Error in Scheduling Agent: {e}")
        return {"schedules": {p: "Best time unknown" for p in platforms}}
