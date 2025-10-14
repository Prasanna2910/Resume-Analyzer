import React, { useState } from "react";
import ResumeAnalysis from "./components/ResumeAnalysis";
import "./app.css"

function App() {
  const [result, setResult] = useState(null);

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("resume", file);

    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Resume Analyzer</h1>
      <input type="file" onChange={handleUpload} className="mb-6" />
      {result && <ResumeAnalysis result={result} />}
    </div>
  );
}

export default App;
