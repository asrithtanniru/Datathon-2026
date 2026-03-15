"use client";

import Image from "next/image";
import { Search } from "lucide-react";
import { motion, Variants } from "framer-motion";

export default function AnimatedHero() {
  const containerVars: Variants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  };

  const itemVars: Variants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
  };

  const badgeVars: Variants = {
    hidden: { opacity: 0, scale: 0.8 },
    show: { opacity: 1, scale: 1, transition: { type: "spring", stiffness: 100, delay: 0.8 } }
  };

  return (
    <section className="relative w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 lg:pt-20 pb-16">
      <div className="grid lg:grid-cols-2 gap-12 lg:gap-8 items-center">
        
        {/* Left Content */}
        <motion.div 
          className="max-w-2xl"
          variants={containerVars}
          initial="hidden"
          animate="show"
        >
          <motion.h1 
            variants={itemVars}
            className="text-5xl lg:text-7xl font-bold tracking-tight text-slate-900 leading-[1.1] mb-6 font-heading"
          >
            The leading AI-powered Real Estate marketplace
          </motion.h1>
          <motion.p 
            variants={itemVars}
            className="text-lg lg:text-xl text-slate-600 mb-10 leading-relaxed"
          >
            Find and sell your home without the hassle. Experience unmatched discovery through visual intelligence in home transactions.
          </motion.p>

          {/* AI Search Bar */}
          <motion.div 
            variants={itemVars}
            className="relative flex items-center w-full max-w-lg bg-slate-50 border border-slate-200 rounded-full p-2 pl-6 shadow-sm mb-4 transition-transform focus-within:ring-2 focus-within:ring-blue-600/20 focus-within:border-blue-300"
          >
            <Search className="w-5 h-5 text-slate-400 mr-3 shrink-0" />
            <input
              type="text"
              placeholder="Try 'modern kitchen with island'..."
              className="w-full bg-transparent border-none outline-none text-slate-900 placeholder:text-slate-400 font-medium"
            />
            <button className="ml-2 whitespace-nowrap bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-full font-medium transition-colors shadow-sm">
              Find Homes
            </button>
          </motion.div>
          
          <motion.p variants={itemVars} className="text-xs text-slate-400 ml-4 font-medium flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></span>
            Powered by multimodal AI without the hassle of unorganized listings
          </motion.p>
        </motion.div>

        {/* Right Content - Visual Arch Layout */}
        <div className="relative w-full h-[600px] lg:h-[700px] flex justify-center lg:justify-end pr-0 lg:pr-8 mt-10 lg:mt-0">
          {/* The Arch Shape */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, ease: "easeInOut" }}
            className="relative w-full max-w-[500px] h-full rounded-t-full overflow-hidden shadow-2xl z-10"
          >
            <div className="absolute inset-0 bg-slate-200 animate-pulse" />
            <Image
              src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=2075&auto=format&fit=crop"
              alt="Beautiful home exterior"
              fill
              className="object-cover"
              priority
            />
          </motion.div>

          {/* Floating Cards */}
          <motion.div 
            variants={badgeVars}
            initial="hidden"
            animate="show"
            className="absolute left-0 lg:-left-12 top-1/2 -translate-y-1/2 glass flex items-center gap-4 p-4 rounded-2xl z-20 w-48"
          >
            <div className="w-12 h-12 rounded-full overflow-hidden relative shrink-0 border-2 border-white shadow-sm">
              <Image src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=200&auto=format&fit=crop" fill className="object-cover" alt="home" />
            </div>
            <div>
              <p className="text-xs text-slate-500 font-medium font-heading">Sell</p>
              <p className="text-lg font-bold text-slate-900">₹12.5Cr</p>
            </div>
          </motion.div>

          <motion.div 
            variants={badgeVars}
            initial="hidden"
            animate="show"
            className="absolute right-0 lg:-right-8 bottom-32 glass flex items-center gap-4 p-4 rounded-2xl z-20 w-48 shadow-lg"
          >
            <div className="w-12 h-12 rounded-full overflow-hidden relative shrink-0 border-2 border-white shadow-sm">
              <Image src="https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?q=80&w=200&auto=format&fit=crop" fill className="object-cover" alt="interior" />
            </div>
            <div>
              <p className="text-xs text-slate-500 font-medium font-heading">Buy</p>
              <p className="text-lg font-bold text-slate-900">₹1.13Cr</p>
            </div>
          </motion.div>
          
          {/* Press Banner / Featured In floating bar */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2, duration: 0.5 }}
            className="absolute bottom-8 lg:bottom-12 left-1/2 -translate-x-1/2 lg:-translate-x-10 glass px-8 py-5 rounded-full z-20 whitespace-nowrap flex items-center gap-8 shadow-xl"
          >
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Featured in:</span>
            <div className="flex items-center gap-6 opacity-70 grayscale">
              <span className="font-serif font-bold text-lg text-slate-800">FORTUNE</span>
              <span className="font-serif font-bold text-lg text-slate-800">WSJ</span>
              <span className="font-serif font-bold text-lg text-slate-800">Forbes</span>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
