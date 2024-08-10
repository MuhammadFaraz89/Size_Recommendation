import React, { useState } from 'react';
import axios from 'axios';

function TshirtSize() {
    const [file, setFile] = useState(null);
    const [size, setSize] = useState("");
    const [error, setError] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setError("");  // Reset error when a new file is selected
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await axios.post('http://localhost:5000/upload', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                setSize(response.data.result);
                setError("");
            } catch (error) {
                console.error("There was an error uploading the file!", error);
                setError("Failed to upload the file. Please try again.");
            }
        } else {
            setError("Please select a file to upload.");
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="file">
                        Upload T-Shirt Image
                    </label>
                    <input
                        type="file"
                        id="file"
                        onChange={handleFileChange}
                        className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                    />
                </div>
                {error && <p className="text-red-500 text-xs italic">{error}</p>}
                <div className="flex items-center justify-between">
                    <button
                        type="submit"
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        Upload
                    </button>
                </div>
            </form>
            {size && (
                <div className="bg-green-100 border-t border-b border-green-500 text-green-700 px-4 py-3">
                    <p>Recommended Size: {size}</p>
                </div>
            )}
        </div>
    );
}

export default TshirtSize;
