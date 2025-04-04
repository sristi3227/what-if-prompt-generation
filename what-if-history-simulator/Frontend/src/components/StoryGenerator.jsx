import React, { useState } from "react";
import axios from "axios";


function App() {
  const [prompt, setPrompt] = useState("");
  const [story, setStory] = useState("");
  const [loading, setLoading] = useState(false);

  const generateStory = async () => {
    if (!prompt.trim()) {
      setStory("Please enter a prompt.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/generate", {
        prompt,
      });
      setStory(response.data.story);
    } catch (error) {
      console.error("Error generating story:", error);
      setStory("Failed to generate story. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <h1>🕰️ Imagine a...</h1>
      <textarea style={{borderRadius:"10px", width:"600px"}}
        placeholder="Enter your 'What If?' prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={generateStory} disabled={loading}>
        {loading ? "Generating..." : "Generate a speculative scenario"}
      </button>
      {story && (
        <div className="story">
          <h2>Generated Story</h2>
          <p>{story}</p>
        </div>
      )}
    </div>
  );
}

export default App;