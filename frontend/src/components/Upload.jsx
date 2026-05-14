import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { uploadFile } from '../api/service'
import { Upload as UploadIcon, CheckCircle, AlertCircle, FileText } from 'lucide-react'

function Upload() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  const navigate = useNavigate()

  const onDrop = useCallback((e) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files[0]
    handleFile(droppedFile)
  }, [])

  const onDragOver = useCallback((e) => {
    e.preventDefault()
  }, [])

  const handleFile = (selectedFile) => {
    setError(null)
    setSuccess(null)
    
    if (!selectedFile) return
    
    const validTypes = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']
    const fileExtension = selectedFile.name.split('.').pop().toLowerCase()
    
    if (!validTypes.includes(selectedFile.type) && !['csv', 'xlsx', 'xls'].includes(fileExtension)) {
      setError('Please upload a CSV or Excel file')
      return
    }
    
    setFile(selectedFile)
  }

  const handleUpload = async () => {
    if (!file) return
    
    setUploading(true)
    setError(null)
    
    try {
      const result = await uploadFile(file)
      setSuccess('File uploaded successfully!')
      setTimeout(() => {
        navigate(`/analysis/${result.file_id}`)
      }, 1500)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading file')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Upload Pricing Data</h1>
        <p className="text-gray-600 mb-6">Upload your CSV or Excel file containing pricing data for analysis</p>
        
        <div
          onDrop={onDrop}
          onDragOver={onDragOver}
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            file ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'
          }`}
        >
          {file ? (
            <div className="space-y-2">
              <FileText className="w-12 h-12 text-blue-500 mx-auto" />
              <p className="text-lg font-medium text-gray-700">{file.name}</p>
              <p className="text-sm text-gray-500">{(file.size / 1024).toFixed(2)} KB</p>
            </div>
          ) : (
            <div className="space-y-2">
              <UploadIcon className="w-12 h-12 text-gray-400 mx-auto" />
              <p className="text-lg text-gray-600">Drag and drop your file here</p>
              <p className="text-sm text-gray-500">or click to browse</p>
              <input
                type="file"
                onChange={(e) => handleFile(e.target.files[0])}
                accept=".csv,.xlsx,.xls"
                className="hidden"
                id="file-input"
              />
              <label
                htmlFor="file-input"
                className="inline-block mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer transition-colors"
              >
                Browse Files
              </label>
            </div>
          )}
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 text-red-500" />
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {success && (
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center space-x-2">
            <CheckCircle className="w-5 h-5 text-green-500" />
            <p className="text-green-700">{success}</p>
          </div>
        )}

        {file && (
          <div className="mt-6 flex space-x-4">
            <button
              onClick={handleUpload}
              disabled={uploading}
              className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {uploading ? 'Uploading...' : 'Upload & Analyze'}
            </button>
            <button
              onClick={() => {
                setFile(null)
                setError(null)
                setSuccess(null)
              }}
              disabled={uploading}
              className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors font-medium"
            >
              Cancel
            </button>
          </div>
        )}

        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold text-gray-700 mb-2">Expected File Format</h3>
          <p className="text-sm text-gray-600 mb-2">Your file should contain the following columns:</p>
          <ul className="text-sm text-gray-600 space-y-1">
            <li><span className="font-medium">product_name</span> (required) - Product identifier</li>
            <li><span className="font-medium">price</span> (required) - Numeric price value</li>
            <li><span className="font-medium">date</span> (required) - Transaction date</li>
            <li><span className="font-medium">category</span> (optional) - Product category</li>
            <li><span className="font-medium">quantity</span> (optional) - Order quantity</li>
            <li><span className="font-medium">supplier</span> (optional) - Supplier name</li>
            <li><span className="font-medium">region</span> (optional) - Geographic region</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Upload
