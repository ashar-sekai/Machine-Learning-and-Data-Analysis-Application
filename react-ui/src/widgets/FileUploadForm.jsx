import React, { useState } from "react";
import axios from "axios";

const FileUploadForm = () => {
  const [file, setFile] = useState(null);
  const [modelType, setModelType] = useState("supervised");
  const [modelName, setModelName] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !modelName) {
      alert("Please select a file and enter a model name.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("model_type", modelType);
    formData.append("model_name", modelName);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData);
      setResponse(res.data.message || "Upload successful.");
    } catch (error) {
      console.error("Upload failed:", error);
      setResponse("Upload failed.");
    }
  };

  return (
    <div className="p-4 border rounded-md shadow bg-white max-w-md mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">Upload Dataset</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="file"
          accept=".csv,.xlsx"
          onChange={(e) => setFile(e.target.files[0])}
          className="block w-full"
        />

        <select
          value={modelType}
          onChange={(e) => setModelType(e.target.value)}
          className="w-full border px-2 py-1"
        >
          <option value="supervised">Supervised</option>
          <option value="unsupervised">Unsupervised</option>
        </select>

        <input
          type="text"
          placeholder="Model Name (e.g., RandomForest)"
          value={modelName}
          onChange={(e) => setModelName(e.target.value)}
          className="w-full border px-2 py-1"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Upload & Train
        </button>
      </form>

      {response && (
        <div className="mt-4 text-center text-green-700 font-medium">{response}</div>
      )}
    </div>
  );
};

export default FileUploadForm;
