import Image from 'next/image'
import { Bookmark, Star } from 'lucide-react'

interface PropertyCardProps {
  type: string
  title: string
  guests: number
  bedrooms: number
  price: number
  rating: number
  imageUrl: string
  score?: number
}

export default function PropertyCard({ type, title, guests, bedrooms, price, rating, imageUrl, score }: PropertyCardProps) {
  return (
    <div className="group bg-white rounded-[24px] border border-slate-100 overflow-hidden hover:shadow-xl transition-all duration-300">
      <div className="relative h-[240px] w-full p-3 pb-0">
        <div className="relative w-full h-full rounded-[18px] overflow-hidden">
          {score !== undefined && (
            <div className="absolute top-3 left-3 z-20 bg-blue-600 border-2 border-white text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-md flex items-center gap-1">
              ✨ {(score * 100).toFixed(0)}% Match
            </div>
          )}
          <Image src={imageUrl} alt={title} fill unoptimized className="object-cover group-hover:scale-105 transition-transform duration-500" />
          <button className="absolute top-3 right-3 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-sm hover:scale-110 transition-transform text-slate-400 hover:text-blue-600 z-10">
            <Bookmark className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="p-5">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">{type}</p>
        <h3 className="text-slate-900 font-bold text-[17px] leading-tight mb-2 line-clamp-2">{title}</h3>
        <p className="text-[13px] text-slate-500 mb-6">
          {guests} guests • {bedrooms} bedrooms
        </p>

        <div className="flex items-end justify-between">
          <div className="flex items-baseline gap-1">
            <span className="text-xs text-slate-500 font-medium">From</span>
            <span className="text-lg font-bold text-slate-900">₹{price.toLocaleString()}</span>
            <span className="text-xs text-slate-500 font-medium">INR</span>
          </div>

          <div className="flex items-center gap-1">
            <span className="text-sm font-bold text-slate-900 mr-1">{rating.toFixed(1)}</span>
            <div className="flex text-amber-400">
              {[1, 2, 3, 4, 5].map((star) => (
                <Star key={star} className={`w-3.5 h-3.5 ${star <= Math.round(rating) ? 'fill-current' : 'fill-transparent text-slate-200'}`} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
