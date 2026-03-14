from fastapi import FastAPI, HTTPException

app = FastAPI()

# Drone status variable
drone_status = "docked"   # possible: docked, landed, flying


@app.get("/")
def home():
    return {"message": "Base Station API Running"}


# Function that only works when variable is called
@app.post("/drone-action/")
def drone_action(variable: str):

    if drone_status not in ["docked", "landed"]:
        raise HTTPException(
            status_code=403,
            detail="Drone must be docked or landed"
        )

    return {
        "status": "request accepted",
        "variable_called": variable,
        "drone_status": drone_status
    }


# Change drone status
@app.post("/set-status/")
def set_status(status: str):
    global drone_status
    drone_status = status
    return {"drone_status": drone_status}


# Check system status
@app.get("/status")
def status():
    return {
        "base_station": "online",
        "drone_status": drone_status
    }