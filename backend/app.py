from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import tempfile, subprocess, json, trimesh, os

app = FastAPI()

@app.post("/estimate")
async def estimate(
    file: UploadFile = File(...),
    infill_density: float = Form(20.0),
    infill_pattern: str = Form("Grid"),
    layer_height: float = Form(0.3),
    wall_thickness: float = Form(1.2),
    top_bottom: float = Form(0.8),
):
    # Save STL file
    temp_dir = tempfile.mkdtemp()
    stl_path = os.path.join(temp_dir, file.filename)
    with open(stl_path, "wb") as f:
        f.write(await file.read())

    # Try CuraEngine
    try:
        cfg = {
            "layer_height": layer_height,
            "wall_thickness": wall_thickness,
            "infill_sparse_density": infill_density,
            "infill_pattern": infill_pattern,
            "top_bottom_thickness": top_bottom
        }

        config_path = os.path.join(temp_dir, "config.json")
        with open(config_path, "w") as cf:
            json.dump(cfg, cf)

        output_path = os.path.join(temp_dir, "out.gcode")
        subprocess.run(["CuraEngine", "slice", "-v", "-j", config_path, "-l", stl_path, "-o", output_path], check=True)

        # Approximation (if CuraEngine not available)
        weight_g = 0.0
    except Exception:
        mesh = trimesh.load_mesh(stl_path)
        volume = mesh.volume
        material_density = 1.24  # g/cm³ for PLA
        scale_factor = infill_density / 100
        weight_g = (volume * scale_factor * material_density) / 1000  # convert mm³ → g

    return JSONResponse({"weight_g": weight_g})
