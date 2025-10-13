import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error(error);
      alert("Upload failed!");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Resume Analyzer</h1>

      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: "10px" }}>
        Upload Resume
      </button>

      {response && (
        <div style={{ marginTop: "20px" }}>
          <h3>Analysis Result:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
