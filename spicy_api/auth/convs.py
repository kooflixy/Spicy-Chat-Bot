from pydantic import BaseModel

class SpicyConv(BaseModel):
    conv_id: str
    char_id: str
    content: str
    created_at: int


def dict_to_SpicyConv(convs_list: list[dict]) -> list[SpicyConv]:
    res = []
    for conv in convs_list:
        res.append(
            SpicyConv(
                conv_id=conv['id'],
                char_id=conv['character_id'],
                content=conv['last_message']['content'],
                created_at=conv['last_message']['createdAt'],
            )
        )
    return res