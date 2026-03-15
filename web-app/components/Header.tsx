import Link from "next/link";
import { Search } from "lucide-react";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 w-full bg-white border-b border-slate-100 shadow-sm">
      <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Left section: Logo & Search */}
          <div className="flex items-center gap-12 flex-1">
            <Link href="/" className="flex items-center gap-2 shrink-0">
              <span className="font-bold text-2xl tracking-tight text-slate-900 flex items-center gap-1">
                <span className="text-blue-600 text-3xl">V</span> isionEstate
              </span>
            </Link>

            {/* Search Bar - Aceplace style */}
            <div className="hidden lg:flex flex-1 max-w-xl items-center bg-slate-50 border border-slate-100 rounded-full px-4 py-2.5">
              <Search className="w-5 h-5 text-slate-400 mr-3" />
              <input
                type="text"
                placeholder="Search..."
                className="bg-transparent border-none outline-none w-full text-sm placeholder:text-slate-400"
              />
            </div>
          </div>

          {/* Right section: Links & Login */}
          <div className="flex items-center gap-4 sm:gap-8 shrink-0">
            <nav className="hidden md:flex items-center gap-6 text-[15px] font-medium text-slate-600">
              <Link href="/listings" className="hover:text-slate-900 transition-colors uppercase text-xs font-bold bg-[#e3fe61] px-4 py-1.5 rounded-full text-slate-900">
                Buy
              </Link>
              <Link href="/listings" className="hover:text-slate-900 transition-colors">
                Sell
              </Link>
              <Link href="/listings" className="hover:text-slate-900 transition-colors">
                Rent
              </Link>
              <Link href="#" className="hover:text-slate-900 transition-colors ml-4 border-l border-slate-200 pl-8">
                Contact us
              </Link>
              
              <div className="flex items-center gap-2 ml-4 mr-2">
                <span className="w-5 h-5 rounded-full bg-blue-100 border border-blue-200 overflow-hidden text-[10px] flex items-center justify-center">🇮🇳</span>
                <span className="text-sm font-semibold text-slate-900">INR</span>
              </div>
            </nav>
            <div className="flex items-center gap-2 sm:gap-4">
              <Link href="/broker" className="hidden sm:inline-flex bg-white hover:bg-slate-50 border border-slate-200 text-slate-900 px-4 sm:px-6 py-2.5 rounded-full text-sm font-semibold transition-colors shadow-sm">
                Post Listing
              </Link>
              <button className="bg-[#0f172a] hover:bg-black text-white px-6 sm:px-8 py-2.5 rounded-full text-sm sm:text-[15px] font-medium transition-colors shadow-sm">
                Login
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
