import React, { useState, useEffect } from "react";

function UploadComponent() {
  const [imageFile, setImageFile] = useState(null);
  const [originalPreview, setOriginalPreview] = useState(null);
  const [maskPreview, setMaskPreview] = useState(null);
  const [overlayPreview, setOverlayPreview] = useState(null);
  const [opacity, setOpacity] = useState(225);

  const CLASS_LABELS = [
    { id: 1, name: "White Blood Cell (WBC)", color: "#1f77b4" },
    { id: 2, name: "Red Blood Cell (RBC)", color: "#ff7f0e" },
    { id: 3, name: "Epithelial Cell", color: "#2ca02c" },
    { id: 4, name: "Bacterium (Rod)", color: "#d62728" },
    { id: 5, name: "Yeast", color: "#9467bd" },
    { id: 6, name: "Small EPC Sheet", color: "#8c564b" },
    { id: 7, name: "Large EPC Sheet", color: "#e377c2" },
  ];

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      setOriginalPreview(null);
      setMaskPreview(null);
      setOverlayPreview(null);
    }
  };

  const submitImage = async (file, currentOpacity) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("opacity", currentOpacity.toString());

    const response = await fetch("http://127.0.0.1:8000/predict/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      console.error("Upload failed");
      return;
    }

    const data = await response.json();
    setOriginalPreview(`data:image/png;base64,${data.original}`);
    setMaskPreview(`data:image/png;base64,${data.mask}`);
    setOverlayPreview(`data:image/png;base64,${data.overlay}`);
  };

  const handleSubmit = () => {
    if (imageFile) {
      submitImage(imageFile, opacity);
    }
  };

  useEffect(() => {
    if (!imageFile || !overlayPreview) return;

    const timeoutId = setTimeout(() => {
      submitImage(imageFile, opacity);
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [opacity, imageFile, overlayPreview]);

  return (
    <div>
      <h2 style={{ textAlign: "center" }}>Welcome to CellSeg!</h2>
      <p>
        Upload a urinary microscopy image. Our AI model will segment cellular structures and generate a visual overlay and color-coded mask.
      </p>
      <div style={{ display: "flex", justifyContent: "center", gap: "1rem", marginBottom: "1rem", alignItems: "center" }}>
        <div style={{ display: "flex", gap: "4px", alignItems: 'center',}}>
          <label htmlFor="file-upload" className="custom-file-upload">
            Choose File
          </label>
          <input
            id="file-upload"
      	    type="file"
      	    accept="image/*"
      	    onChange={handleFileChange}
      	    style={{ display: "none" }}
      	  />
      	  {imageFile && (
      	    <span>{imageFile.name}</span>
      	  )}
        </div>
        <button onClick={handleSubmit}>Submit Image</button>
      </div>
      {originalPreview && maskPreview && overlayPreview && (
        <div>
          <div style={{ display: "flex", justifyContent: "center", gap: "2rem", marginTop: "2rem" }}>
            <div>
              <h4 style={{ textAlign: "center" }}>Original Image</h4>
              <img
                src={originalPreview}
                alt="Original"
                style={{ width: "256px", height: "256px", objectFit: "cover", border: "1px solid #ccc" }}
              />
            </div>
            <div>
              <h4 style={{ textAlign: "center" }}>Segmentation Mask</h4>
              <img
                src={maskPreview}
                alt="Mask"
                style={{ width: "256px", height: "256px", objectFit: "cover", border: "1px solid #ccc" }}
              />
            </div>
            <div>
              <h4 style={{ textAlign: "center" }}>Overlay</h4>
              <img
                src={overlayPreview}
                alt="Overlay"
                style={{ width: "256px", height: "256px", objectFit: "cover", border: "1px solid #ccc" }}
              />
              <div style={{ textAlign: "center", marginTop: "0.5rem" }}>
                <label>
                  Overlay Opacity: {opacity}
                  <input
                    type="range"
                    min="0"
                    max="255"
                    value={opacity}
                    onChange={(e) => setOpacity(Number(e.target.value))}
                    style={{ marginLeft: "1rem" }}
                  />
                </label>
              </div>
            </div>
          </div>

          <div style={{ marginTop: "2rem", textAlign: "center" }}>
            <h4>Segmentation Class Legend</h4>
            <div style={{ display: "flex", justifyContent: "center", flexWrap: "wrap", gap: "1rem" }}>
              {CLASS_LABELS.map((cls) => (
                <div key={cls.id} style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                  <div style={{
                    width: "16px",
                    height: "16px",
                    backgroundColor: cls.color,
                    borderRadius: "3px",
                    border: "1px solid #333"
                  }} />
                  <span>{cls.id} – {cls.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UploadComponent;
