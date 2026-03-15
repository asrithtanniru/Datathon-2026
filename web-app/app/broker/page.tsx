'use client'

import { useState } from 'react'
import { UploadCloud, Image as ImageIcon, MapPin, IndianRupee, Home, Bed, Users, X } from 'lucide-react'
import Image from 'next/image'
import axios from 'axios'
import { useRouter } from 'next/navigation'

export default function BrokerUploadPage() {
  const [images, setImages] = useState<string[]>([])
  const [files, setFiles] = useState<File[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0]
      const imageUrl = URL.createObjectURL(file)
      setImages((prev) => [...prev, imageUrl])
      setFiles((prev) => [...prev, file])
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0]
      const imageUrl = URL.createObjectURL(file)
      setImages((prev) => [...prev, imageUrl])
      setFiles((prev) => [...prev, file])
    }
  }

  const removeImage = (index: number) => {
    setImages((prev) => prev.filter((_, i) => i !== index))
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (files.length === 0) {
      alert('Please upload an image.')
      return
    }

    const formData = new FormData(e.currentTarget)
    formData.append('file', files[0])

    // Convert or set missing fields properly
    setIsLoading(true)
    try {
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      alert('Listing uploaded and analyzed successfully!')
      router.push('/listings')
    } catch (error: any) {
      console.error(error)
      alert(error.response?.data?.detail || 'An error occurred during upload.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#f1f5f9] pb-24 px-4 sm:px-6 lg:px-8 pt-8">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 mb-2">Create New Listing</h1>
          <p className="text-slate-500 text-sm sm:text-base">Upload property images to let VisionEstate AI automatically analyze the space and categorize your listing.</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-[24px] shadow-sm border border-slate-100 overflow-hidden">
          {/* Section 1: AI Image Upload */}
          <div className="p-6 sm:p-8 border-b border-slate-100 bg-slate-50/50">
            <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
              <span className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
                <ImageIcon className="w-4 h-4" />
              </span>
              Property Media
            </h2>

            <div
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              className="mt-2 flex justify-center rounded-2xl border-2 border-dashed border-slate-300 px-6 py-12 hover:bg-slate-50 transition-colors bg-white relative"
            >
              <div className="text-center">
                <UploadCloud className="mx-auto h-12 w-12 text-slate-400" aria-hidden="true" />
                <div className="mt-4 flex text-sm leading-6 text-slate-600 justify-center">
                  <label
                    htmlFor="file-upload"
                    className="relative cursor-pointer rounded-md bg-transparent font-semibold text-blue-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-blue-600 focus-within:ring-offset-2 hover:text-blue-500"
                  >
                    <span>Upload a file</span>
                    <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleFileChange} accept="image/*" multiple />
                  </label>
                  <p className="pl-1">or drag and drop</p>
                </div>
                <p className="text-xs leading-5 text-slate-500 mt-2">PNG, JPG, GIF up to 10MB</p>
              </div>
            </div>

            {/* Image Preview Grid */}
            {images.length > 0 && (
              <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 gap-4">
                {images.map((img, idx) => (
                  <div key={idx} className="relative aspect-square rounded-xl overflow-hidden border border-slate-200 group">
                    <Image src={img} alt={`Preview ${idx}`} fill className="object-cover" />
                    <button
                      type="button"
                      onClick={() => removeImage(idx)}
                      className="absolute top-2 right-2 bg-white/80 backdrop-blur opacity-0 group-hover:opacity-100 transition-opacity w-8 h-8 rounded-full flex items-center justify-center shadow-md hover:bg-rose-50 text-rose-500"
                    >
                      <X className="w-4 h-4" />
                    </button>
                    {idx === 0 && <div className="absolute bottom-2 left-2 bg-slate-900/80 backdrop-blur text-white text-[10px] font-bold px-2 py-1 rounded-md">Cover Image</div>}
                  </div>
                ))}
              </div>
            )}

            {images.length > 0 && (
              <div className="mt-4 bg-blue-50 border border-blue-100 rounded-xl p-4 flex gap-3 text-sm text-blue-700">
                <span className="text-xl shrink-0">✨</span>
                <p>
                  VisionEstate AI is ready to analyze your {images.length} uploaded {images.length === 1 ? 'image' : 'images'} to automatically generate tags, room details, and natural language
                  embeddings.
                </p>
              </div>
            )}
          </div>

          {/* Section 2: Details */}
          <div className="p-6 sm:p-8 space-y-6">
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <span className="w-8 h-8 rounded-full bg-slate-100 text-slate-600 flex items-center justify-center">
                <Home className="w-4 h-4" />
              </span>
              Listing Information
            </h2>

            <div className="grid grid-cols-1 gap-x-6 gap-y-6 sm:grid-cols-6">
              <div className="sm:col-span-6">
                <label htmlFor="title" className="block text-sm font-semibold leading-6 text-slate-900">
                  Property Title
                </label>
                <div className="mt-2">
                  <input
                    type="text"
                    name="title"
                    id="title"
                    placeholder="e.g. Modern Beachfront Villa"
                    className="block w-full rounded-xl border-0 py-3 px-4 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-200 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 bg-slate-50"
                  />
                </div>
              </div>

              <div className="sm:col-span-6">
                <label htmlFor="location" className="block text-sm font-semibold leading-6 text-slate-900">
                  Location
                </label>
                <div className="mt-2 relative">
                  <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
                    <MapPin className="h-5 w-5 text-slate-400" aria-hidden="true" />
                  </div>
                  <input
                    type="text"
                    name="location"
                    id="location"
                    placeholder="City, Neighborhood or Address"
                    className="block w-full rounded-xl border-0 py-3 pl-11 pr-4 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-200 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 bg-slate-50"
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label htmlFor="price" className="block text-sm font-semibold leading-6 text-slate-900">
                  Price (INR)
                </label>
                <div className="mt-2 relative">
                  <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
                    <IndianRupee className="h-5 w-5 text-slate-400" aria-hidden="true" />
                  </div>
                  <input
                    type="number"
                    name="price"
                    id="price"
                    className="block w-full rounded-xl border-0 py-3 pl-11 pr-4 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-200 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 bg-slate-50"
                    placeholder="0.00"
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label htmlFor="category" className="block text-sm font-semibold leading-6 text-slate-900">
                  Property Type
                </label>
                <div className="mt-2">
                  <select
                    id="category"
                    name="category"
                    className="block w-full rounded-xl border-0 py-3.5 px-4 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-200 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 bg-slate-50"
                  >
                    <option>Villa</option>
                    <option>House</option>
                    <option>Apartment</option>
                    <option>Hotel Suite</option>
                  </select>
                </div>
              </div>

              <div className="sm:col-span-3">
                <label htmlFor="bedrooms" className="block text-sm font-semibold leading-6 text-slate-900">
                  Bedrooms
                </label>
                <div className="mt-2 relative">
                  <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
                    <Bed className="h-5 w-5 text-slate-400" aria-hidden="true" />
                  </div>
                  <input
                    type="number"
                    name="bedrooms"
                    id="bedrooms"
                    className="block w-full rounded-xl border-0 py-3 pl-11 pr-4 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-200 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 bg-slate-50"
                    placeholder="e.g. 3"
                  />
                </div>
              </div>

              <div className="sm:col-span-3">
                <label htmlFor="guests" className="block text-sm font-semibold leading-6 text-slate-900">
                  Max Guests
                </label>
                <div className="mt-2 relative">
                  <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
                    <Users className="h-5 w-5 text-slate-400" aria-hidden="true" />
                  </div>
                  <input
                    type="number"
                    name="guests"
                    id="guests"
                    className="block w-full rounded-xl border-0 py-3 pl-11 pr-4 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-200 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6 bg-slate-50"
                    placeholder="e.g. 6"
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="p-6 sm:p-8 border-t border-slate-100 bg-slate-50 flex items-center justify-end gap-x-6">
            <button type="button" className="text-sm font-semibold leading-6 text-slate-900 hover:text-slate-700 transition">
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className={`rounded-full px-8 py-3 text-sm font-semibold text-white shadow-sm transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 w-full sm:w-auto text-center ${isLoading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-500'}`}
            >
              {isLoading ? 'Analyzing Media...' : 'Analyze & Publish Listing'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
