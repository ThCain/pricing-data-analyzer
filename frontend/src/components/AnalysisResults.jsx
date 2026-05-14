import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { analyzeData, generateReport, downloadReportFile, getVisualizations } from '../api/service'
import { ArrowLeft, Download, BarChart3, TrendingUp, AlertTriangle, Calendar, DollarSign, Package } from 'lucide-react'

function AnalysisResults() {
  const { fileId } = useParams()
  const navigate = useNavigate()
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [generatingReport, setGeneratingReport] = useState(false)

  useEffect(() => {
    loadAnalysis()
  }, [fileId])

  const loadAnalysis = async () => {
    setLoading(true)
    try {
      const data = await analyzeData(fileId)
      setAnalysis(data)
      setError(null)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load analysis')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateReport = async () => {
    setGeneratingReport(true)
    try {
      await generateReport(fileId)
      const response = await downloadReportFile(fileId)
      
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `pricing_report_${fileId}.xlsx`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      setError('Failed to generate report')
    } finally {
      setGeneratingReport(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading analysis...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <p className="text-red-700">{error}</p>
        <button
          onClick={() => navigate('/dashboard')}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          Back to Dashboard
        </button>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-12 text-center">
        <BarChart3 className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-700 mb-2">No Analysis Available</h2>
        <p className="text-gray-500 mb-4">Run analysis on this file to see results</p>
        <button
          onClick={loadAnalysis}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Run Analysis
        </button>
      </div>
    )
  }

  const summary = analysis.summary || {}

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/dashboard')}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-gray-600" />
          </button>
          <h1 className="text-3xl font-bold text-gray-800">Analysis Results</h1>
        </div>
        <button
          onClick={handleGenerateReport}
          disabled={generatingReport}
          className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <Download className="w-4 h-4" />
          <span>{generatingReport ? 'Generating...' : 'Download Report'}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <Package className="w-5 h-5 text-blue-500" />
            <span className="text-sm text-gray-500">Total Records</span>
          </div>
          <p className="text-3xl font-bold text-gray-800">{summary.total_records || 0}</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <DollarSign className="w-5 h-5 text-green-500" />
            <span className="text-sm text-gray-500">Average Price</span>
          </div>
          <p className="text-3xl font-bold text-gray-800">${(summary.average_price || 0).toFixed(2)}</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="w-5 h-5 text-purple-500" />
            <span className="text-sm text-gray-500">Price Range</span>
          </div>
          <p className="text-3xl font-bold text-gray-800">
            ${(summary.min_price || 0).toFixed(2)} - ${(summary.max_price || 0).toFixed(2)}
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <AlertTriangle className="w-5 h-5 text-orange-500" />
            <span className="text-sm text-gray-500">Outliers</span>
          </div>
          <p className="text-3xl font-bold text-gray-800">{summary.outliers_detected || 0}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Summary Statistics</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-600">Total Records</span>
              <span className="font-semibold">{summary.total_records || 0}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-600">Average Price</span>
              <span className="font-semibold">${(summary.average_price || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-600">Minimum Price</span>
              <span className="font-semibold">${(summary.min_price || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-600">Maximum Price</span>
              <span className="font-semibold">${(summary.max_price || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-600">Variance</span>
              <span className="font-semibold">{(summary.variance || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-gray-600">Outliers Detected</span>
              <span className="font-semibold">{summary.outliers_detected || 0}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Data Overview</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-600">Date Range</span>
              <span className="font-semibold text-sm">{summary.date_range || 'N/A'}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-600">Unique Products</span>
              <span className="font-semibold">{summary.unique_products || 0}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-600">Unique Categories</span>
              <span className="font-semibold">{summary.unique_categories || 0}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b">
              <span className="text-gray-600">Unique Suppliers</span>
              <span className="font-semibold">{summary.unique_suppliers || 0}</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-gray-600">Unique Regions</span>
              <span className="font-semibold">{summary.unique_regions || 0}</span>
            </div>
          </div>
        </div>
      </div>

      {analysis.detailed_analysis && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Detailed Analysis</h2>
          <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm">
            {JSON.stringify(analysis.detailed_analysis, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}

export default AnalysisResults
