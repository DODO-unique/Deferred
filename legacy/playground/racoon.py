from pydantic import BaseModel

class Raccoon(BaseModel):
    name: str
    hunger: int
    awake: bool

class EnclosureState(BaseModel):
    food_supply: int
    # each raccoons is a dictionary. This dictionary types as "string" : Raccoon(...) EZ
    raccoons: dict[str, Raccoon]


# now, I define a case, say, like this. It is just a simple dictionary, and that is fine.
RAW_STATE = {
    "food_supply": 20,
    "raccoons": {
        "Bandit": {"name": "Bandit", "hunger": 3, "awake": True},
        "Socks": {"name": "Socks", "hunger": 7, "awake": False},
    }
}

# We will pick that state, then upload it into the EnclosureState

state = EnclosureState(**RAW_STATE)

# now, all we have to do is state.raccoons['Socks'].name and boom, we get the name. Ez. That is how we can change stuff too

# say we want to add something new, we can create functions that systematically do that. 
# if say we want another read this, we can just export the state in a function. So say:

def global_state_read() -> EnclosureState:
    return EnclosureState(**RAW_STATE)