interface Format {
  format_id: string
  resolution: string
  ext: string
  filesize: number | null
  fps: number
  type: string
}

interface ResolutionSelectorProps {
  formats: Format[]
  selectedFormat: Format | null
  onSelectFormat: (format: Format) => void
}

export default function ResolutionSelector({ formats, selectedFormat, onSelectFormat }: ResolutionSelectorProps) {
  const getQualityBadge = (resolution: string) => {
    const quality = parseInt(resolution)
    if (quality >= 2160) return { label: '4K', color: 'from-purple-500 to-pink-500' }
    if (quality >= 1440) return { label: '2K', color: 'from-blue-500 to-cyan-500' }
    if (quality >= 1080) return { label: 'FHD', color: 'from-green-500 to-emerald-500' }
    if (quality >= 720) return { label: 'HD', color: 'from-yellow-500 to-orange-500' }
    return { label: 'SD', color: 'from-gray-500 to-gray-600' }
  }

  return (
    <div className="mb-8 animate-fade-in">
      <div className="flex items-center gap-3 mb-4">
        <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">Select Quality</h3>
        <span className="px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded-full text-blue-400 text-sm font-medium">
          {formats.length} options
        </span>
      </div>
      <div className="glass rounded-xl overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gradient-to-r from-gray-800 to-gray-700 border-b border-gray-600">
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Quality</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Format</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">FPS</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Size</th>
                <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Type</th>
                <th className="px-6 py-4 text-center text-xs font-bold text-gray-300 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700/50">
              {formats.map((format, index) => {
                const badge = getQualityBadge(format.resolution)
                const isSelected = selectedFormat?.format_id === format.format_id
                return (
                  <tr
                    key={format.format_id}
                    className={`group hover:bg-gray-700/40 transition-all duration-200 cursor-pointer ${
                      isSelected ? 'bg-blue-900/30 border-l-4 border-blue-500' : 'border-l-4 border-transparent'
                    }`}
                    onClick={() => onSelectFormat(format)}
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <span className={`px-2 py-1 rounded-md text-xs font-bold text-white bg-gradient-to-r ${badge.color} shadow-lg`}>
                          {badge.label}
                        </span>
                        <span className="text-gray-100 font-bold text-lg">{format.resolution}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center gap-1 px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded-lg text-blue-400 font-semibold text-sm">
                        {format.ext.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-gray-300 font-medium">{format.fps ? `${format.fps} fps` : '-'}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-gray-300 font-medium">{format.filesize ? `${format.filesize} MB` : '-'}</span>
                    </td>
                    <td className="px-6 py-4">
                      {format.type === 'audio_only' ? (
                        <span className="inline-flex items-center gap-2 px-3 py-1 bg-purple-500/20 border border-purple-500/30 rounded-lg text-purple-400 font-medium">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
                          </svg>
                          Audio
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-2 px-3 py-1 bg-green-500/20 border border-green-500/30 rounded-lg text-green-400 font-medium">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/>
                          </svg>
                          Video
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-center">
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          onSelectFormat(format)
                        }}
                        className={`px-5 py-2 rounded-lg font-semibold transition-all duration-200 transform group-hover:scale-105 ${
                          isSelected
                            ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/50'
                            : 'bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-white'
                        }`}
                      >
                        {isSelected ? (
                          <span className="flex items-center gap-2">
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                            </svg>
                            Selected
                          </span>
                        ) : 'Select'}
                      </button>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
