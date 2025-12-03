from typing import TypedDict, List, Dict, Any, Annotated
import operator

def merge_dicts(a: Dict, b: Dict) -> Dict:
    return {**a, **b}

def merge_lists(a: List, b: List) -> List:
    return a + b

class AgentState(TypedDict):
    base_content: str
    platforms: List[str]
    tone: str
    metadata: Dict[str, Any]
    platform_outputs: Annotated[Dict[str, str], merge_dicts]
    hashtags: Annotated[Dict[str, List[str]], merge_dicts]
    schedules: Annotated[Dict[str, str], merge_dicts]
    visuals: Annotated[List[str], merge_lists]
