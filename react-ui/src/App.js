import React from "react";
import FileUploadForm from "./widgets/FileUploadForm";

function App() {
  return (
    <div className="App">
      <h1>🧠 Anomaly Detection App</h1>
      <FileUploadForm />
    </div>
  );
}

import FluidGlass from './widgets/FluidGlass';

function App() {
  return (
    <div className="relative w-full h-screen">
      <FluidGlass mode="lens" />
      {/* Add other components here */}
    </div>
  );
}

export default App;




