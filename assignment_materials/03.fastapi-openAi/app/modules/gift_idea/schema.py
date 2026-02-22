from pydantic import BaseModel, Field


class Gift(BaseModel):
    idea: str = Field(description="The description of the event")
    cost: str = Field(description="The budget for but gift")


class Gift_Idea(BaseModel):
    event: str = Field(description="The description of the event")
    budget: str = Field(description="The budget for but gift")
    gifts: list[Gift] = Field(description="The list of gift adjust with budget")
