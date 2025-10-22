document.getElementById("estimateBtn").addEventListener("click", async () => {
  const file = document.getElementById("fileInput").files[0];
  if (!file) {
    alert("Please upload an STL file!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("infill_density", document.getElementById("infillDensity").value);
  formData.append("infill_pattern", document.getElementById("infillPattern").value);
  formData.append("layer_height", document.getElementById("layerHeight").value);
  formData.append("wall_thickness", document.getElementById("wallThickness").value);
  formData.append("top_bottom", document.getElementById("topBottom").value);
  formData.append("material", document.getElementById("material").value);

  document.getElementById("result").innerText = "Calculating...";

  try {
    const response = await fetch("https://your-backend-url.onrender.com/estimate", {
      method: "POST",
      body: formData
    });
    const data = await response.json();
    document.getElementById("result").innerText =
      `Estimated Weight: ${data.weight_g.toFixed(2)} g`;
  } catch (err) {
    document.getElementById("result").innerText =
      "⚠️ Error: Backend not reachable. Try again later.";
  }
});