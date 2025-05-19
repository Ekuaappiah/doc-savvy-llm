import React, { useState, useRef } from 'react';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const fileInputRef = useRef(null); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !query) return;

    setLoading(true);
    setResponse('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('query', query);

    try {
      const res = await fetch('http://localhost:8080/upload/', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      setResponse(data.answer || 'No answer returned');
    } catch (err) {
      console.error(err);
      setResponse('An error occurred while uploading the file.');
    } finally {
      setLoading(false);
    }
  };

 const handleReset = () => {
    setFile(null);
    setQuery('');
    setResponse('');
    if (fileInputRef.current) {
      fileInputRef.current.value = null;  
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4 py-12">
      <div className="w-full max-w-2xl bg-white rounded-3xl shadow-2xl p-10 border border-gray-200">
        <h2 className="text-4xl font-bold text-gray-900 mb-2 text-center">
          Document Q&A
        </h2>
        <p className="text-gray-600 text-sm text-center mb-8">
          Upload a document and ask a question about its content.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Upload File
            </label>
            <input
              type="file"
              ref={fileInputRef}
              onChange={(e) => setFile(e.target.files[0])}
              className="block w-full text-sm text-gray-700 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Your Question
            </label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., What is the summary of this document?"
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />
          </div>

          <div className="flex space-x-4">
            <button
              type="submit"
              disabled={loading}
              className={`w-full ${
                loading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
              } text-white font-medium py-2.5 rounded-lg transition duration-200 shadow-md`}
            >
              {loading ? 'Generating.....' : 'Analyze Document'}
            </button>

            <button
              type="button"
              onClick={handleReset}
              disabled={loading}
              className="w-full bg-gray-400 hover:bg-gray-500 text-white font-medium py-2.5 rounded-lg transition duration-200 shadow-md"
            >
              Reset Form
            </button>
          </div>
        </form>

        {response && (
          <div className="mt-10 bg-gray-50 p-6 rounded-xl border border-gray-200 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Answer</h3>
            <p className="text-gray-700 whitespace-pre-wrap text-sm">{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default UploadForm;
