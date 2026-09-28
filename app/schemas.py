from pydantic import BaseModel, Field, field_validator

class UserInput(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=120)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, le=500)
    goal: str = Field(pattern=r"^(weight loss|muscle gain|general wellness|flexibility)$")
    intensity: str = Field(pattern=r"^(low|medium|high)$")

    @field_validator("user_id", "name")
    @classmethod
    def strip_text(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value

class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    feedback: str = Field(min_length=3, max_length=1000)
