import { useEffect, useState, useRef } from 'react';
import api from '../services/api';

export default function FilePreview({ file, onClose }) {
  const [fileUrl, setFileUrl] = useState(null);
  const currentUrlRef = useRef(null);

  const fileId = file?.id;

  useEffect(() => {
    if (!fileId) return;

    const fetchFile = async () => {
      try {
        const response = await api.get(`/files/${fileId}`, {
          responseType: 'blob',
        });
        const url = URL.createObjectURL(response.data);
        if (currentUrlRef.current) {
          URL.revokeObjectURL(currentUrlRef.current);
        }
        currentUrlRef.current = url;
        setFileUrl(url);
      } catch (error) {
        console.error('Error fetching file:', error);
      }
    };

    fetchFile();

    return () => {
      if (currentUrlRef.current) {
        URL.revokeObjectURL(currentUrlRef.current);
        currentUrlRef.current = null;
      }
    };
  }, [fileId]);

  if (!file) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-900 p-6 rounded-xl w-[600px]">
        <h2 className="font-bold mb-4 text-white">{file.name}</h2>

        {fileUrl ? (
          <iframe
            src={fileUrl}
            className="w-full h-96 border rounded"
            title="preview"
          />
        ) : (
          <div className="w-full h-96 border rounded flex items-center justify-center">
            Loading...
          </div>
        )}

        <button
          onClick={onClose}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
        >
          Close
        </button>
      </div>
    </div>
  );
}
