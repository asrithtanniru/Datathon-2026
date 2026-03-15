'use client'

import { useEffect, useState, Suspense } from 'react'
import axios from 'axios'
import PropertyCard from '@/components/PropertyCard'
import { ChevronDown, Filter, LayoutGrid, List, Home, Hotel, Building, Tent, MapPin } from 'lucide-react'
import { useSearchParams } from 'next/navigation'

function ListingsContent() {
  const searchParams = useSearchParams()
  const searchQuery = searchParams.get('q')

  const [properties, setProperties] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchListings = async () => {
      setLoading(true)
      try {
        if (searchQuery) {
          const response = await axios.post('http://127.0.0.1:8000/search', {
            query: searchQuery,
            top_k: 1,
          })
          setProperties(response.data.results || [])
        } else {
          const response = await axios.get('http://127.0.0.1:8000/listings')
          setProperties(response.data)
        }
      } catch (error) {
        console.error('Error fetching listings:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchListings()
  }, [searchQuery])

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
              <span className="text-blue-600 font-black">—</span> {searchQuery ? `AI Search: "${searchQuery}"` : 'Coimbatore, India Villa'}
            </h1>
            <p className="text-sm text-slate-500 font-medium ml-6">
              {properties.length} {searchQuery ? 'matches found based on your prompt' : 'Villas available in Coimbatore'}
            </p>
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
          {loading ? (
            <div className="col-span-full py-10 text-center text-slate-500 font-medium">Loading listings...</div>
          ) : properties.length > 0 ? (
            properties.map((property: any, idx) => (
              <PropertyCard
                key={idx}
                type={property.category || 'PROPERTY'}
                title={property.title || 'Untitled Property'}
                guests={property.guests || 2}
                bedrooms={property.bedrooms || 1}
                price={property.price || 0}
                rating={4.5}
                score={property.score}
                imageUrl={`http://127.0.0.1:8000/uploads/${property.image_filename}`}
              />
            ))
          ) : (
            <div className="col-span-full py-10 text-center text-slate-500 font-medium">No listings found. Be the first to upload!</div>
          )}
        </div>
      </div>
    </div>
  )
}

export default function ListingsPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center text-slate-500 font-medium">Loading AI Engine...</div>}>
      <ListingsContent />
    </Suspense>
  )
}
