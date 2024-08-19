from pydantic import BaseModel


class KeysSchema(BaseModel):
    private_key: str
    public_key: str
