from pydantic import BaseModel

class GeneratorSchema(BaseModel):
    user_id: int 
    key_length: int
    long_url: str
    domain: str
