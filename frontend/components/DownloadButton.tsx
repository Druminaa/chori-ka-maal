interface DownloadButtonProps {
  onClick: () => void
  disabled: boolean
  loading: boolean
  progress: number
  success: boolean
}

export default function DownloadButton({ onClick, disabled, loading, progress, success }: DownloadButtonProps) {
  return (
    <div className="glass rounded-2xl p-6 shadow-xl">
      <button
        onClick={onClick}
        disabled={disabled}
        className="w-full py-4 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-xl font-bold text-lg hover:from-emerald-600 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 shadow-lg shadow-emerald-500/50"
      >
        {loading ? 'Downloading...' : success ? '✓ Download Complete!' : '⬇ Download Now'}
      </button>

      {loading && (
        <div className="mt-4">
          <div className="flex justify-between text-sm mb-2">
            <span>Progress</span>
            <span>{progress}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-all duration-300 animate-pulse"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {success && (
        <div className="mt-4 p-4 bg-green-900/30 border border-green-500 rounded-lg text-green-400 text-center animate-pulse">
          ✓ Your download has started successfully!
        </div>
      )}
    </div>
  )
}
