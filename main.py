from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import tempfile, subprocess, json, os, trimesh

app = FastAPI()

@app.post("/estimate")
async def estimate(
    file: UploadFile = File(...),
    infill_density: float = Form(20.0),
    infill_pattern: str = Form("Grid"),
    layer_height: float = Form(0.3),
    wall_thickness: float = Form(1.2),
    top_bottom: float = Form(0.8),
    material: str = Form("PLA")
):
    temp_dir = tempfile.mkdtemp()
    stl_path = os.path.join(temp_dir, file.filename)
    with open(stl_path, "wb") as f:
        f.write(await file.read())

    mesh = trimesh.load_mesh(stl_path)
    volume = mesh.volume

    densities = {"PLA": 1.24, "ABS": 1.04, "PETG": 1.27, "TPU": 1.21}
    density = densities.get(material.upper(), 1.24)

    weight_g = (volume * (infill_density / 100) * density) / 1000

    return JSONResponse({"weight_g": weight_g})