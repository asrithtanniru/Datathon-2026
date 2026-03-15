import PropertyCard from '@/components/PropertyCard'
import { ChevronDown, Filter, LayoutGrid, List, Home, Hotel, Building, Tent, MapPin } from 'lucide-react'

const MOCK_PROPERTIES = [
  {
    type: 'VILLA',
    title: 'Five Palm Jumeirah Beachfront Villa - Pool, Jacuzzi',
    guests: 8,
    bedrooms: 4,
    price: 1920,
    rating: 4.6,
    imageUrl: 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=800&auto=format&fit=crop',
  },
  {
    type: 'VILLA',
    title: 'Two Bedroom Arabian Summerhouse Family Suite',
    guests: 6,
    bedrooms: 3,
    price: 890,
    rating: 3.2,
    imageUrl: 'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?q=80&w=800&auto=format&fit=crop',
  },
  {
    type: 'VILLA',
    title: 'Beach Front Villa in Five Palm Jumeirah Hotel',
    guests: 6,
    bedrooms: 2,
    price: 750,
    rating: 5.0,
    imageUrl: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=800&auto=format&fit=crop',
  },
  {
    type: 'VILLA',
    title: 'Arabian Summerhouse Superior',
    guests: 8,
    bedrooms: 3,
    price: 1299,
    rating: 3.8,
    imageUrl: 'https://images.unsplash.com/photo-1510798831971-661eb04b3739?q=80&w=800&auto=format&fit=crop',
  },
  {
    type: 'VILLA',
    title: 'Stylish Luxury Sunshine Villa Perfect for Families',
    guests: 4,
    bedrooms: 2,
    price: 1000,
    rating: 4.9,
    imageUrl: 'https://images.unsplash.com/photo-1449844908441-8829872d2607?q=80&w=800&auto=format&fit=crop',
  },
  {
    type: 'VILLA',
    title: 'Spacious Garden Villa near the Beach',
    guests: 6,
    bedrooms: 3,
    price: 1450,
    rating: 3.6,
    imageUrl: 'https://images.unsplash.com/photo-1513694203232-719a280e022f?q=80&w=800&auto=format&fit=crop',
  },
]

export default function ListingsPage() {
  return (
    <div className="min-h-screen bg-[#f1f5f9] pb-24">
      <div className="bg-white border-b border-slate-100 px-4 sm:px-6 lg:px-8 py-3 w-full overflow-x-auto overflow-y-hidden shadow-sm sticky top-20 z-40">
        <div className="max-w-[1400px] mx-auto flex items-center justify-between min-w-[800px]">
          <div className="flex items-center gap-2 lg:gap-6 w-full">
            <button className="gradient-active px-6 py-3.5 rounded-2xl flex items-center gap-3 font-semibold text-sm shadow-md transition-transform hover:scale-105">
              <LayoutGrid className="w-4 h-4" />
              ALL CATEGORY
              <ChevronDown className="w-4 h-4 ml-2 opacity-70" />
            </button>

            <div className="flex items-center space-x-2">
              <button className="px-6 py-3.5 rounded-2xl flex items-center gap-3 font-medium text-sm text-slate-500 hover:bg-slate-50 transition-colors">
                <Home className="w-5 h-5 opacity-70" /> House
              </button>
              <button className="px-6 py-3.5 rounded-2xl flex items-center gap-3 font-medium text-sm text-slate-500 hover:bg-slate-50 transition-colors">
                <Building className="w-5 h-5 opacity-70" /> Hotel
              </button>
              <button className="px-6 py-3.5 rounded-2xl flex items-center gap-3 font-semibold text-sm text-blue-600 bg-blue-50/50 border-b-2 border-blue-600">
                <Hotel className="w-5 h-5" /> Villa
              </button>
              <button className="px-6 py-3.5 rounded-2xl flex items-center gap-3 font-medium text-sm text-slate-500 hover:bg-slate-50 transition-colors">
                <Building className="w-5 h-5 opacity-70" /> Appartment
              </button>
              <button className="px-6 py-3.5 rounded-2xl flex items-center gap-3 font-medium text-sm text-slate-500 hover:bg-slate-50 transition-colors">
                <Tent className="w-5 h-5 opacity-70" /> Camp House
              </button>
            </div>
          </div>

          <div className="shrink-0 flex items-center gap-3 pl-8 ml-4 border-l border-slate-100">
            <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center border-2 border-white shadow-sm overflow-hidden">
              <MapPin className="w-5 h-5" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-900 leading-tight">India</p>
              <p className="text-xs text-slate-500">Coimbatore</p>
            </div>
            <ChevronDown className="w-4 h-4 text-slate-400 ml-2" />
          </div>
        </div>
      </div>

      <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 pt-10">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 mb-1 flex items-center gap-2">
              <span className="text-blue-600 font-black">—</span> Coimbatore, India Villa
            </h1>
            <p className="text-sm text-slate-500 font-medium ml-6">649 Villas available in Coimbatore</p>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3 text-slate-400 mr-2 border-r border-slate-200 pr-5">
              <button className="hover:text-slate-900 text-slate-900 transition-colors">
                <LayoutGrid className="w-5 h-5 fill-current" />
              </button>
              <button className="hover:text-slate-900 transition-colors">
                <List className="w-5 h-5" />
              </button>
            </div>

            <button className="flex items-center gap-3 bg-white border border-slate-200 rounded-xl px-5 py-2.5 text-sm font-semibold text-slate-700 hover:shadow-sm transition-all">
              <Filter className="w-4 h-4 text-slate-400" />
              Filters
              <ChevronDown className="w-4 h-4 text-slate-400 ml-4" />
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
          {MOCK_PROPERTIES.map((property, idx) => (
            <PropertyCard key={idx} {...property} />
          ))}
        </div>
      </div>
    </div>
  )
}
