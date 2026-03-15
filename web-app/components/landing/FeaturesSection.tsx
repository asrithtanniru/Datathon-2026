"use client";

import { motion } from "framer-motion";
import { Sparkles, Image as ImageIcon, SearchCode, ShieldCheck, UploadCloud } from "lucide-react";

const features = [
  {
    name: "AI Intelligent Search",
    description: "Search naturally. Unstructured data is transformed into searchable tags. Try 'modern apartment with balcony'.",
    icon: SearchCode,
    color: "bg-blue-100 text-blue-600",
  },
  {
    name: "Automated Categorization",
    description: "Our multimodal AI analyzes property photos and instantly identifies room types, architecture, and condition.",
    icon: ImageIcon,
    color: "bg-indigo-100 text-indigo-600",
  },
  {
    name: "Seamless Broker Upload",
    description: "Brokers just drag, drop, and publish. VisionEstate AI takes care of tags, embeds, and organization.",
    icon: UploadCloud,
    color: "bg-emerald-100 text-emerald-600",
  },
  {
    name: "Verified & Secure",
    description: "We use advanced algorithms to flag falsified listings and verify property dimensions for total buyer trust.",
    icon: ShieldCheck,
    color: "bg-rose-100 text-rose-600",
  },
];

const stats = [
  { id: 1, name: "Properties Analyzed securely by AI", value: "2M+" },
  { id: 2, name: "Broker & Agent Partners across India", value: "10k+" },
  { id: 3, name: "Value matched successfully last year", value: "₹2,000Cr+" },
  { id: 4, name: "Average time saved per buyer search", value: "14 hrs" },
];

export default function FeaturesSection() {
  return (
    <div className="bg-white py-24 sm:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        {/* Intro */}
        <div className="mx-auto max-w-2xl lg:text-center mb-16 sm:mb-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-base font-semibold leading-7 text-blue-600 flex items-center justify-center gap-2">
              <Sparkles className="w-5 h-5" /> Why VisionEstate
            </h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Real Estate Intelligence, Unlocked.
            </p>
            <p className="mt-6 text-lg leading-8 text-slate-600">
              We&apos;ve replaced the frustration of rigid filters and messy listings with a fluid, intelligent marketplace driven by visual data.
            </p>
          </motion.div>
        </div>

        {/* Feature Grid */}
        <div className="mx-auto max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none mb-32">
          <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-4">
            {features.map((feature, index) => (
              <motion.div 
                key={feature.name} 
                className="flex flex-col"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-slate-900">
                  <div className={`h-10 w-10 flex items-center justify-center rounded-lg ${feature.color}`}>
                    <feature.icon className="h-6 w-6" aria-hidden="true" />
                  </div>
                  {feature.name}
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-slate-600">
                  <p className="flex-auto">{feature.description}</p>
                </dd>
              </motion.div>
            ))}
          </dl>
        </div>

        {/* Statistics Banner */}
        <motion.div 
          className="mx-auto max-w-7xl px-6 lg:px-8 bg-slate-900 rounded-[32px] py-16 sm:py-24 relative overflow-hidden"
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.7 }}
        >
          {/* Background pattern */}
          <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)', backgroundSize: '24px 24px' }}></div>
          
          <div className="relative z-10">
            <div className="mx-auto max-w-2xl lg:max-w-none">
              <div className="text-center">
                <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                  Trusted by thousands worldwide
                </h2>
                <p className="mt-4 text-lg leading-8 text-slate-300">
                  We&apos;re building the foundation for the next generation of property transactions.
                </p>
              </div>
              <dl className="mt-16 grid grid-cols-1 gap-0.5 overflow-hidden rounded-2xl text-center sm:grid-cols-2 lg:grid-cols-4 border border-slate-800 bg-slate-800/50">
                {stats.map((stat) => (
                  <div key={stat.id} className="flex flex-col bg-slate-900 p-8">
                    <dt className="text-sm font-semibold leading-6 text-slate-400">{stat.name}</dt>
                    <dd className="order-first text-3xl font-semibold tracking-tight text-white mb-2">{stat.value}</dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </motion.div>
        
      </div>
    </div>
  );
}
