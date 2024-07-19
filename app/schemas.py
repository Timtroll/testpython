from pydantic import BaseModel, ConfigDict

class MemeBase(BaseModel):
    title: str
    description: str

class MemeCreate(MemeBase):
    image_url: str

class Meme(MemeBase):
    id: int
    image_url: str

    model_config = ConfigDict(from_attributes=True)
