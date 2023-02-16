from fastapi import FastAPI
from pydantic import BaseModel

from create_card_modeles import get_name_value_measure
from sentenize import create_cores

app = FastAPI()


class Characteristic(BaseModel):
    text: str
    core: bool = False


@app.post('/detector')
async def get_characteristics(characteristic: Characteristic):
    raw_text = characteristic.text
    if characteristic.core:
        output_core = create_cores(raw_text)
    else:
        output_core = create_cores(raw_text)
        output_core = get_name_value_measure(output_core)
    return output_core