function submitImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
  
    if (!file) {
      alert("Please select an image to upload.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file);
  
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("result").innerText = `Predicted Blood Group: ${data.blood_group}, Confidence: ${data.confidence}`;
      })
      .catch((error) => {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error processing image.";
      });
  }
  