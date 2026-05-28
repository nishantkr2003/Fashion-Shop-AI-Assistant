"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import {
  Sparkles,
  Search,
  Package,
  MessageCircle,
  ArrowRight,
  Star,
  ShoppingBag,
  Zap,
  Shield,
  ChevronRight,
  TrendingUp,
} from "lucide-react";

const FLOATING_TAGS = [
  "Nike Air Max",
  "Under ₹1,000",
  "Summer Sale",
  "Red Sneakers",
  "Return Policy",
  "Size Guide",
  "New Arrivals",
  "Track Order",
];

const STATS = [
  { value: "5K+", label: "Products Indexed" },
  { value: "2s", label: "Avg Response Time" },
  { value: "98%", label: "Query Accuracy" },
  { value: "24/7", label: "Always Available" },
];

const FEATURES = [
  {
    icon: Search,
    title: "Natural Product Search",
    desc: "Ask in plain English. Find red Nike shoes under ₹3,000 with next-day delivery — no filters needed.",
    color: "from-violet-500/10 to-violet-500/5",
    accent: "bg-violet-500",
    tag: "Search",
  },
  {
    icon: Package,
    title: "Live Inventory Queries",
    desc: "Check real-time stock, sizes, and variants. Get notified when your item is back.",
    color: "from-emerald-500/10 to-emerald-500/5",
    accent: "bg-emerald-500",
    tag: "Inventory",
  },
  {
    icon: MessageCircle,
    title: "Policy & Support AI",
    desc: "Returns, shipping, exchange rules — instant answers drawn from the latest store policies.",
    color: "from-amber-500/10 to-amber-500/5",
    accent: "bg-amber-500",
    tag: "Support",
  },
  {
    icon: TrendingUp,
    title: "Style Recommendations",
    desc: "Tell us your vibe and budget. Get curated outfits styled by AI, not algorithms.",
    color: "from-rose-500/10 to-rose-500/5",
    accent: "bg-rose-500",
    tag: "Style",
  },
];

const TESTIMONIALS = [
  {
    name: "Priya S.",
    handle: "@priya_shops",
    text: "Found the exact white sneakers I wanted in 10 seconds. No scrolling through 500 items.",
    rating: 5,
    avatar: "PS",
    color: "bg-violet-100 text-violet-700",
  },
  {
    name: "Rahul M.",
    handle: "@rahul_m",
    text: "Asked about return policy for international orders. Got a perfect answer instantly.",
    rating: 5,
    avatar: "RM",
    color: "bg-emerald-100 text-emerald-700",
  },
  {
    name: "Ananya K.",
    handle: "@ananya.k",
    text: "It styled a whole wedding guest outfit within my budget. Absolutely love it.",
    rating: 5,
    avatar: "AK",
    color: "bg-rose-100 text-rose-700",
  },
];

const EXAMPLE_QUERIES = [
  "Show me products under ₹1,000",
  "What's your return policy?",
  "Find red Nike shoes in size 8",
  "How long does shipping take?",
  "Style me for a beach wedding under ₹5,000",
  "Is the black puffer jacket back in stock?",
];

export default function HomePage() {
  const [queryIdx, setQueryIdx] = useState(0);
  const [displayText, setDisplayText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);
  const [charIdx, setCharIdx] = useState(0);
  const heroRef = useRef<HTMLDivElement>(null);

  // Typewriter effect
  useEffect(() => {
    const current = EXAMPLE_QUERIES[queryIdx];
    let timeout: NodeJS.Timeout;

    if (!isDeleting && charIdx <= current.length) {
      setDisplayText(current.slice(0, charIdx));
      timeout = setTimeout(() => setCharIdx((c) => c + 1), 45);
    } else if (!isDeleting && charIdx > current.length) {
      timeout = setTimeout(() => setIsDeleting(true), 2000);
    } else if (isDeleting && charIdx >= 0) {
      setDisplayText(current.slice(0, charIdx));
      timeout = setTimeout(() => setCharIdx((c) => c - 1), 22);
    } else {
      setIsDeleting(false);
      setQueryIdx((i) => (i + 1) % EXAMPLE_QUERIES.length);
    }

    return () => clearTimeout(timeout);
  }, [charIdx, isDeleting, queryIdx]);

  // Parallax on hero
  useEffect(() => {
    const el = heroRef.current;
    if (!el) return;
    const onScroll = () => {
      el.style.transform = `translateY(${window.scrollY * 0.25}px)`;
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <div className="min-h-screen bg-[#FAFAF8] text-[#0D0D0C] font-sans overflow-x-hidden">
      {/* ─── NAV ─── */}
      <nav className="fixed top-0 inset-x-0 z-50 flex items-center justify-between px-6 md:px-12 h-16 border-b border-black/[0.06] bg-[#FAFAF8]/90 backdrop-blur-md">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-[#0D0D0C] text-white flex items-center justify-center text-sm font-bold tracking-tight">
            ✦
          </div>
          <span className="font-semibold text-sm tracking-tight">
            Fashion Shop AI
          </span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm text-[#6B6B68]">
          <a href="#features" className="hover:text-[#0D0D0C] transition">
            Features
          </a>
          <a href="#how-it-works" className="hover:text-[#0D0D0C] transition">
            How it works
          </a>
          <a href="#testimonials" className="hover:text-[#0D0D0C] transition">
            Reviews
          </a>
        </div>
        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="text-sm text-[#6B6B68] hover:text-[#0D0D0C] transition hidden sm:block"
          >
            Sign in
          </Link>
          <Link
            href="/signup"
            className="text-sm bg-[#0D0D0C] text-white px-4 py-2 rounded-xl hover:bg-[#2a2a27] transition font-medium"
          >
            Get started
          </Link>
        </div>
      </nav>

      {/* ─── HERO ─── */}
      <section className="relative pt-36 pb-24 px-6 md:px-12 overflow-hidden">
        {/* Soft glow bg */}
        <div
          ref={heroRef}
          className="absolute inset-0 pointer-events-none select-none"
        >
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[700px] h-[400px] rounded-full bg-gradient-to-br from-violet-200/40 via-rose-100/30 to-amber-100/30 blur-3xl" />
        </div>

        <div className="relative max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-white border border-black/[0.08] rounded-full px-4 py-1.5 text-xs font-medium text-[#6B6B68] mb-8 shadow-sm">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            AI-Powered Shopping Assistant · Live
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight leading-[1.05] mb-6 text-[#0D0D0C]">
            Shop smarter.
            <br />
            <span className="text-[#A0A09B]">Ask anything.</span>
          </h1>

          <p className="text-lg md:text-xl text-[#6B6B68] max-w-xl mx-auto mb-12 leading-relaxed">
            Skip the filters. Just describe what you're looking for — products,
            policies, style advice — and get instant, accurate answers.
          </p>

          {/* Animated search bar */}
          <div className="relative max-w-lg mx-auto mb-12">
            <div className="flex items-center gap-3 bg-white border border-black/[0.1] rounded-2xl px-5 py-4 shadow-lg shadow-black/[0.04]">
              <Search className="w-4 h-4 text-[#A0A09B] flex-shrink-0" />
              <span className="text-sm text-[#0D0D0C] flex-1 text-left min-h-[20px]">
                {displayText}
                <span className="inline-block w-0.5 h-4 bg-[#0D0D0C] ml-0.5 animate-pulse align-middle" />
              </span>
              <Link href="/chat">
                <div className="w-8 h-8 bg-[#0D0D0C] rounded-lg flex items-center justify-center hover:bg-[#2a2a27] transition">
                  <ArrowRight className="w-4 h-4 text-white" />
                </div>
              </Link>
            </div>
          </div>

          {/* Floating tags */}
          <div className="flex flex-wrap justify-center gap-2 mb-14">
            {FLOATING_TAGS.map((tag) => (
              <Link
                key={tag}
                href="/chat"
                className="text-xs px-3 py-1.5 bg-white border border-black/[0.08] rounded-full text-[#6B6B68] hover:text-[#0D0D0C] hover:border-black/20 hover:shadow-sm transition"
              >
                {tag}
              </Link>
            ))}
          </div>

          <Link
            href="/chat"
            className="inline-flex items-center gap-2.5 bg-[#0D0D0C] text-white px-8 py-4 rounded-2xl text-sm font-semibold hover:bg-[#2a2a27] transition group shadow-lg shadow-black/10"
          >
            <Sparkles className="w-4 h-4" />
            Start chatting — it's free
            <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
          </Link>
        </div>
      </section>

      {/* ─── STATS ─── */}
      <section className="border-y border-black/[0.06] py-10 bg-white">
        <div className="max-w-5xl mx-auto px-6 md:px-12 grid grid-cols-2 md:grid-cols-4 gap-8">
          {STATS.map(({ value, label }) => (
            <div key={label} className="text-center">
              <p className="text-3xl font-bold text-[#0D0D0C] mb-1 tracking-tight">
                {value}
              </p>
              <p className="text-sm text-[#A0A09B]">{label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ─── FEATURES ─── */}
      <section id="features" className="py-28 px-6 md:px-12">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-sm font-medium text-[#A0A09B] uppercase tracking-widest mb-3">
              Capabilities
            </p>
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-[#0D0D0C]">
              Everything a shopper needs
            </h2>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            {FEATURES.map(({ icon: Icon, title, desc, color, accent, tag }) => (
              <div
                key={title}
                className={`relative bg-gradient-to-br ${color} border border-black/[0.06] rounded-3xl p-8 hover:shadow-lg hover:shadow-black/[0.06] transition-all duration-300 group cursor-default`}
              >
                <div className="flex items-start justify-between mb-6">
                  <div
                    className={`w-10 h-10 ${accent} bg-opacity-10 rounded-xl flex items-center justify-center`}
                  >
                    <Icon className="w-5 h-5 text-[#0D0D0C]" />
                  </div>
                  <span className="text-xs font-medium text-[#A0A09B] bg-white/60 px-2.5 py-1 rounded-full border border-black/[0.06]">
                    {tag}
                  </span>
                </div>
                <h3 className="text-lg font-semibold mb-2 text-[#0D0D0C]">
                  {title}
                </h3>
                <p className="text-sm text-[#6B6B68] leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── HOW IT WORKS ─── */}
      <section
        id="how-it-works"
        className="py-24 px-6 md:px-12 bg-[#0D0D0C] text-white"
      >
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-sm font-medium text-white/30 uppercase tracking-widest mb-3">
              Process
            </p>
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
              Three steps to done
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: "01",
                title: "Type your question",
                desc: "No forms, no filters. Ask in plain language like you'd ask a friend.",
                icon: MessageCircle,
              },
              {
                step: "02",
                title: "AI finds the answer",
                desc: "Our agent searches products, policies, and inventory in real-time.",
                icon: Zap,
              },
              {
                step: "03",
                title: "Shop with confidence",
                desc: "Get direct links, precise answers, and follow-up support instantly.",
                icon: ShoppingBag,
              },
            ].map(({ step, title, desc, icon: Icon }) => (
              <div key={step} className="relative">
                <div className="text-6xl font-bold text-white/[0.06] mb-4 font-mono">
                  {step}
                </div>
                <div className="w-10 h-10 bg-white/[0.08] rounded-xl flex items-center justify-center mb-4 border border-white/[0.08]">
                  <Icon className="w-5 h-5 text-white/70" />
                </div>
                <h3 className="font-semibold mb-2">{title}</h3>
                <p className="text-sm text-white/50 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── TESTIMONIALS ─── */}
      <section id="testimonials" className="py-28 px-6 md:px-12">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-sm font-medium text-[#A0A09B] uppercase tracking-widest mb-3">
              Reviews
            </p>
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-[#0D0D0C]">
              Loved by shoppers
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            {TESTIMONIALS.map(
              ({ name, handle, text, rating, avatar, color }) => (
                <div
                  key={name}
                  className="bg-white border border-black/[0.06] rounded-3xl p-6 hover:shadow-lg hover:shadow-black/[0.04] transition"
                >
                  <div className="flex items-center gap-1 mb-4">
                    {Array.from({ length: rating }).map((_, i) => (
                      <Star
                        key={i}
                        className="w-3.5 h-3.5 fill-amber-400 text-amber-400"
                      />
                    ))}
                  </div>
                  <p className="text-sm text-[#0D0D0C] leading-relaxed mb-6">
                    "{text}"
                  </p>
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-full ${color} flex items-center justify-center text-xs font-semibold`}
                    >
                      {avatar}
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-[#0D0D0C]">
                        {name}
                      </p>
                      <p className="text-xs text-[#A0A09B]">{handle}</p>
                    </div>
                  </div>
                </div>
              ),
            )}
          </div>
        </div>
      </section>

      {/* ─── CTA ─── */}
      <section className="py-24 px-6 md:px-12 bg-white border-t border-black/[0.06]">
        <div className="max-w-2xl mx-auto text-center">
          <div className="w-16 h-16 rounded-3xl bg-[#0D0D0C] text-white flex items-center justify-center text-3xl mx-auto mb-8">
            ✦
          </div>
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-[#0D0D0C] mb-4">
            Ready to shop differently?
          </h2>
          <p className="text-[#6B6B68] mb-10 text-lg">
            Join thousands of shoppers finding what they need in seconds, not
            minutes.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link
              href="/signup"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-[#0D0D0C] text-white px-8 py-4 rounded-2xl text-sm font-semibold hover:bg-[#2a2a27] transition"
            >
              <Sparkles className="w-4 h-4" />
              Create free account
            </Link>
            <Link
              href="/login"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-white border border-black/[0.1] text-[#0D0D0C] px-8 py-4 rounded-2xl text-sm font-medium hover:bg-[#FAFAF8] transition"
            >
              Sign in
            </Link>
          </div>
        </div>
      </section>

      {/* ─── FOOTER ─── */}
      <footer className="border-t border-black/[0.06] py-8 px-6 md:px-12">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-lg bg-[#0D0D0C] text-white flex items-center justify-center text-xs">
              ✦
            </div>
            <span className="text-sm font-medium text-[#0D0D0C]">
              Fashion Shop AI
            </span>
          </div>
          <div className="flex items-center gap-6 text-xs text-[#A0A09B]">
            <a href="#" className="hover:text-[#0D0D0C] transition">
              Privacy
            </a>
            <a href="#" className="hover:text-[#0D0D0C] transition">
              Terms
            </a>
            <a href="#" className="hover:text-[#0D0D0C] transition">
              Support
            </a>
          </div>
          <p className="text-xs text-[#A0A09B]">© 2026 Fashion Shop AI</p>
        </div>
      </footer>
    </div>
  );
}
