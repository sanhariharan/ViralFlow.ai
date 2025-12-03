from fastapi import FastAPI, HTTPException
from backend.app.models.schemas import ContentRequest, GenerationResponse, VisualsRequest
from backend.app.graph.workflow import create_graph
from backend.app.agents.visuals import visuals_agent
import uvicorn

app = FastAPI(title="AI Social Media Content Manager")

# Initialize Graph
graph = create_graph()

@app.post("/generate", response_model=GenerationResponse)
async def generate_content(request: ContentRequest):
    try:
        # Initial state
        initial_state = {
            "base_content": request.base_content,
            "platforms": [p.lower() for p in request.platforms],
            "tone": request.tone,
            "metadata": {},
            "platform_outputs": {},
            "hashtags": {},
            "schedules": {},
            "visuals": []
        }
        
        # Run the graph
        # invoke returns the final state
        final_state = graph.invoke(initial_state)
        
        return GenerationResponse(
            platform_outputs=final_state.get("platform_outputs", {}),
            hashtags=final_state.get("hashtags", {}),
            schedules=final_state.get("schedules", {}),
            visuals=final_state.get("visuals", []),
            metadata=final_state.get("metadata", {})
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/regenerate_visuals")
async def regenerate_visuals(request: VisualsRequest):
    try:
        # Construct a minimal state for the agent
        state = {
            "metadata": {
                "topic": request.topic,
                "keywords": request.keywords
            }
        }
        # Call the agent function directly
        result = visuals_agent(state)
        return {"visuals": result.get("visuals", [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
