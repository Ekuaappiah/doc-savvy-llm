import React, { useState } from 'react';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !query) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('query', query);

    try {
      const res = await fetch('http://localhost:8080/upload/', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      console.log(data)
      setResponse(data.answer);
    } catch (err) {
      console.error(err);
      setResponse("Error uploading file.");
    }
  };

  return (
    <div className="p-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="block"
        />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query"
          className="block w-full p-2 border"
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2">Submit</button>
      </form>
      <div className="mt-4">
        <strong>Answer:</strong> <p>{response}</p>
      </div>
    </div>
  );
}

export default UploadForm;
