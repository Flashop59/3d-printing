document.getElementById("estimateBtn").addEventListener("click", async () => {
  const file = document.getElementById("fileInput").files[0];
  if (!file) {
    alert("Please upload an STL file first!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("infill_density", document.getElementById("infillDensity").value);
  formData.append("infill_pattern", document.getElementById("infillPattern").value);
  formData.append("layer_height", document.getElementById("layerHeight").value);
  formData.append("wall_thickness", document.getElementById("wallThickness").value);
  formData.append("top_bottom", document.getElementById("topBottom").value);

  document.getElementById("result").innerText = "Processing...";

  const response = await fetch("https://your-backend.onrender.com/estimate", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  document.getElementById("result").innerText = `Estimated Weight: ${data.weight_g.toFixed(2)} g`;
});
