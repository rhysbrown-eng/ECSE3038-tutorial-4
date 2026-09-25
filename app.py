from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Device(BaseModel):
    name: str
    room: str
    temp: float
    online: bool


class DevicePatch(BaseModel):
    name: Optional[str] = None
    room: Optional[str] = None
    temp: Optional[float] = None
    online: Optional[bool] = None


readings = [
    {"name": "front-door", "room": "hall",    "temp": 27.4, "online": True},
    {"name": "hall-lamp",  "room": "hall",    "temp": 26.1, "online": True},
    {"name": "attic",      "room": "attic",   "temp": 31.9, "online": True},
    {"name": "fridge",     "room": "kitchen", "temp": 4.2,  "online": False},
    {"name": "patio",      "room": "outside", "temp": 29.8, "online": True},
]


@app.get("/devices")
def get_devices():
    return readings


@app.get("/devices/{name}")
def get_device(name: str):
    for device in readings:
        if device["name"] == name:
            return device
    raise HTTPException(status_code=404, detail="No device called " + name)


@app.post("/devices", status_code=201)
def create_device(device: Device):
    new_device = device.model_dump()

    for reading in readings:
        if reading["name"] == new_device["name"]:
            raise HTTPException(status_code=409, 
                                detail="No device called " + new_device["name"] +  " already exists"
                                )

    readings.append(new_device)
    return new_device


@app.put("/devices/{name}")
def update_device(name:str, device: Device):
    for i, reading in enumerate(readings):
        if reading["name"] == name:
            idx = i
            break
    else:
        raise HTTPException(status_code=404, detail="No device called " + name)

    device_dict = device.model_dump()
    readings[idx] = device_dict
    return device_dict

@app.delete("/devices/{name}")
def delete_device(name:str):
    for reading in readings:
        if reading["name"] == name:
            readings.remove(reading)
            break
    else:
        raise HTTPException(status_code=404, detail="No device called " + name)
    
    return {"deleted": name}

@app.patch("/devices/{name}")
def optional_field_update(name:str, changes: DevicePatch):
    for reading in readings:
        if reading["name"] == name:
            device_dict = changes.model_dump(exclude_unset=True)
            reading.update(device_dict)
            return reading

    raise HTTPException(status_code=404, detail="No device called " + name)