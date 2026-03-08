'use client'

import { useState } from 'react'
import Navbar from '@/components/Navbar'
import VideoCard from '@/components/VideoCard'
import ResolutionSelector from '@/components/ResolutionSelector'
import DownloadButton from '@/components/DownloadButton'
import Footer from '@/components/Footer'
import axios from 'axios'

interface VideoInfo {
  title: string
  thumbnail: string
  channel: string
  duration: number
  formats: Format[]
}

interface Format {
  format_id: string
  resolution: string
  ext: string
  filesize: number | null
  fps: number
  type: string
}

export default function Home() {
  const [url, setUrl] = useState('')
  const [videoInfo, setVideoInfo] = useState<VideoInfo | null>(null)
  const [selectedFormat, setSelectedFormat] = useState<Format | null>(null)
  const [loading, setLoading] = useState(false)
  const [downloading, setDownloading] = useState(false)
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(0)
  const [success, setSuccess] = useState(false)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const fetchVideoInfo = async () => {
    if (!url.trim()) {
      setError('Please enter a valid YouTube URL')
      return
    }

    setLoading(true)
    setError('')
    setVideoInfo(null)
    setSelectedFormat(null)
    setSuccess(false)

    try {
      const response = await axios.post(`${API_URL}/api/video-info`, { url }, {
        timeout: 15000
      })
      setVideoInfo(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch video info')
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!selectedFormat || !url || !videoInfo) return

    setDownloading(true)
    setProgress(0)
    setSuccess(false)

    try {
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(interval)
            return 90
          }
          return prev + 10
        })
      }, 300)

      const response = await axios.post(`${API_URL}/api/download`, {
        url,
        format_id: selectedFormat.format_id,
        type: selectedFormat.type
      }, {
        responseType: 'blob'
      })

      clearInterval(interval)
      setProgress(100)
      
      const blob = new Blob([response.data])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      
      const ext = selectedFormat.type === 'audio_only' ? 'mp3' : selectedFormat.ext
      link.download = `${videoInfo.title}.${ext}`
      
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(downloadUrl)
      
      setSuccess(true)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Download failed')
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-1 container mx-auto px-4 py-12 max-w-4xl">
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent drop-shadow-lg">
            YouTube Downloader
          </h1>
          <p className="text-gray-400 text-lg mb-8">Fast, simple, and free video downloads</p>
          
          <div className="glass rounded-2xl p-8 shadow-2xl">
            <div className="flex flex-col md:flex-row gap-4">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && fetchVideoInfo()}
                placeholder="Paste YouTube URL here..."
                className="flex-1 px-6 py-4 rounded-xl bg-gray-900 border border-gray-600 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-gray-100 placeholder-gray-500"
              />
              <button
                onClick={fetchVideoInfo}
                disabled={loading}
                className="px-8 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl font-semibold text-white hover:from-blue-600 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 shadow-lg shadow-blue-500/30"
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Loading...
                  </span>
                ) : 'Fetch Video Info'}
              </button>
            </div>
            
            {error && (
              <div className="mt-4 p-4 bg-red-900/30 border border-red-500 rounded-lg text-red-400">
                {error}
              </div>
            )}
          </div>
        </div>

        {videoInfo && (
          <VideoCard
            title={videoInfo.title}
            thumbnail={videoInfo.thumbnail}
            channel={videoInfo.channel}
            duration={videoInfo.duration}
          />
        )}

        {videoInfo && (
          <ResolutionSelector
            formats={videoInfo.formats}
            selectedFormat={selectedFormat}
            onSelectFormat={(format) => {
              setSelectedFormat(format)
              setSuccess(false)
              setProgress(0)
            }}
          />
        )}

        {selectedFormat && (
          <DownloadButton
            onClick={handleDownload}
            disabled={downloading}
            loading={downloading}
            progress={progress}
            success={success}
          />
        )}
      </main>

      <Footer />
    </div>
  )
}
