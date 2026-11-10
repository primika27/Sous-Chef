from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class TaskType(str, Enum):
    ACTIVE = "active"     # Requires cook's hands (chopping, stirring)
    PASSIVE = "passive"   # Thermal/ambient (boiling, baking, resting)

class ResourceRequirements(BaseModel):
    hands: int = Field(default=1, description="Hands required: 1 or 2 (0 if fully unattended passive)")
    burners: int = Field(default=0, description="Number of stovetop burners occupied")
    oven: bool = Field(default=False, description="Whether an oven/broiler is required")

class TaskNode(BaseModel):
    id: str = Field(description="Unique short id, e.g. task_1")
    instruction: str = Field(description="Clear, imperative action command")
    duration: int = Field(description="Duration in minutes (estimation if not clear)")
    type: TaskType = Field(default=TaskType.ACTIVE, description="Type of task")
    resources: List[ResourceRequirements] = Field(
        default_factory=list,
        description="['hands', 'burner'] for active sautéing, ['burner'] for passive boiling"
    )
    dependencies: List[str] = Field(
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
    start_time: int # in minutes from the start of the recipe
    end_time: int # in minutes from the start of the recipe
    assigned_resources: List[ResourceRequirements] = Field(default_factory=list)
    review_alert: Optional[str] = None