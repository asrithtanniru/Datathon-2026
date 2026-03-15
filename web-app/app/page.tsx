import AnimatedHero from "../components/landing/AnimatedHero";
import FeaturesSection from "../components/landing/FeaturesSection";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-white overflow-hidden">
      
      {/* 1. Animated Hero Section */}
      <AnimatedHero />

      {/* Background Map Graphic (Decorative) */}
      <div className="absolute bottom-0 left-0 w-full h-[400px] pointer-events-none opacity-20 bg-[url('https://images.unsplash.com/photo-1524661135-423995f22d0b?q=80&w=2074&auto=format&fit=crop')] bg-cover bg-top -z-10 [mask-image:linear-gradient(to_bottom,transparent,black)]"></div>

      {/* 2. New Animated Features Grid & Statistics */}
      <FeaturesSection />

      {/* 3. AI Platform Description Section */}
      <section className="w-full bg-slate-50 py-24 border-t border-slate-100 relative z-10">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center justify-center px-4 py-1.5 mb-8 rounded-full bg-blue-100/50 border border-blue-200 text-blue-700 text-sm font-semibold tracking-wide uppercase">
            Platform Vision
          </div>
          <h2 className="text-3xl lg:text-4xl font-bold text-slate-900 mb-8 font-heading">
            Visual Intelligence Layer
          </h2>
          <p className="text-lg lg:text-xl text-slate-600 leading-relaxed">
            &ldquo;Our platform introduces an AI-powered visual intelligence layer for real estate marketplaces. Property platforms today receive massive volumes of unorganized interior images from brokers and agents, making it difficult to categorize listings and match them with buyer intent. Our system analyzes property photos using computer vision and multimodal AI to identify room types, architectural styles, lighting conditions, and spatial layout. These images are converted into semantic embeddings, enabling users to search for homes using natural language queries such as &lsquo;bright bedroom with balcony&rsquo; or &lsquo;modern kitchen with island.&rsquo; By transforming unstructured property images into structured spatial intelligence, the platform enables smarter property discovery, cleaner listings, and a more intuitive home search experience.&rdquo;
          </p>
        </div>
      </section>
      
    </div>
  );
}
