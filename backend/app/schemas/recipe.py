from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ResourceType(str, Enum):
    HANDS = "hands"          # Human attention (chopping, whisking, plating)
    BURNER = "burner"        # Stovetop burner
    OVEN = "oven"            # Oven space
    COUNTER = "counter"      # Passive resting/marinating space

class TaskNode(BaseModel):
    id: str = Field(description="Unique short id, e.g. task_1")
    description: str
    duration_minutes: int
    required_resources: List[ResourceType] = Field(
        description="['hands', 'burner'] for active sautéing, ['burner'] for passive boiling"
    )
    depends_on: List[str] = Field(
        default_factory=list, 
        description="IDs of tasks that MUST finish before this task starts"
    )
    review_alert: Optional[str] = Field(
        None, description="Warning attached directly to this step based on reviews"
    )

class RecipeGraph(BaseModel):
    title: str
    ingredients: List[str]
    blogger_tips: List[str] = Field(default_factory=list)
    community_tips: List[str] = Field(default_factory=list)
    tasks: List[TaskNode]

class ScheduledTask(BaseModel):
    task_id: str
    description: str
    start_minute: int
    end_minute: int
    assigned_resources: List[ResourceType]
    review_alert: Optional[str] = None