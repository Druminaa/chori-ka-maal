import Image from 'next/image'

interface VideoCardProps {
  title: string
  thumbnail: string
  channel: string
  duration: number
}

export default function VideoCard({ title, thumbnail, channel, duration }: VideoCardProps) {
  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="glass rounded-2xl p-6 mb-8 glass-hover shadow-xl">
      <div className="flex flex-col md:flex-row gap-6">
        <div className="relative w-full md:w-80 h-48 rounded-xl overflow-hidden shadow-lg">
          <Image
            src={thumbnail}
            alt={title}
            fill
            className="object-cover"
          />
          <div className="absolute bottom-2 right-2 bg-black/80 px-2 py-1 rounded text-sm font-semibold">
            {formatDuration(duration)}
          </div>
        </div>
        <div className="flex-1">
          <h2 className="text-2xl font-bold mb-3 leading-tight text-gray-100">{title}</h2>
          <p className="text-gray-400 flex items-center gap-2">
            <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
            <span className="font-medium">{channel}</span>
          </p>
        </div>
      </div>
    </div>
  )
}
