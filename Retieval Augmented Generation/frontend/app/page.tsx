'use client';

import { motion } from 'framer-motion';
import { Search, Sparkles, Zap, Image as ImageIcon, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 animated-gradient opacity-20"></div>

      {/* Floating orbs */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-primary-500/30 rounded-full blur-3xl floating"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-accent-500/30 rounded-full blur-3xl floating" style={{ animationDelay: '1s' }}></div>

      <div className="relative z-10">
        {/* Navigation */}
        <nav className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-2"
            >
              <div className="p-2 rounded-lg bg-gradient-to-br from-primary-500 to-accent-500">
                <ImageIcon className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold gradient-text">ImageRAG</span>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <Link
                href="/search"
                className="px-6 py-2 rounded-lg glass-dark text-white hover:bg-white/10 transition-all duration-300"
              >
                Get Started
              </Link>
            </motion.div>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="container mx-auto px-6 py-20">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="mb-6"
            >
              <span className="px-4 py-2 rounded-full glass-dark text-primary-400 text-sm font-semibold">
                ✨ Powered by AI
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-6xl md:text-7xl font-bold text-white mb-6 leading-tight"
            >
              Find Images with
              <br />
              <span className="gradient-text">AI-Powered Search</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-xl text-gray-400 mb-12 max-w-2xl mx-auto"
            >
              Advanced Retrieval Augmented Generation system that combines image search
              with intelligent captions and narratives powered by CLIP, BLIP-2, and Stable Diffusion.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <Link
                href="/search"
                className="group px-8 py-4 rounded-xl font-bold text-lg text-white bg-gradient-to-r from-primary-500 to-accent-500 hover:shadow-glow transition-all duration-300 flex items-center justify-center gap-2"
              >
                Start Searching
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/search"
                className="px-8 py-4 rounded-xl font-bold text-lg text-white glass-dark hover:bg-white/10 transition-all duration-300"
              >
                View Demo
              </Link>
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto"
          >
            {[
              {
                icon: Search,
                title: 'Smart Search',
                description: 'Search by text description or upload similar images using CLIP embeddings',
                gradient: 'from-blue-500 to-cyan-500',
              },
              {
                icon: Sparkles,
                title: 'AI Captions',
                description: 'Automatic image captioning with BLIP-2 for better understanding',
                gradient: 'from-purple-500 to-pink-500',
              },
              {
                icon: Zap,
                title: 'Generate Images',
                description: 'Create new images from text with Stable Diffusion integration',
                gradient: 'from-orange-500 to-red-500',
              },
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                className="card-glass p-8 text-center group cursor-pointer"
              >
                <div className={`inline-flex p-4 rounded-2xl bg-gradient-to-br ${feature.gradient} mb-4 group-hover:scale-110 transition-transform`}>
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-400">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </motion.div>
        </section>

        {/* CTA Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto text-center glass-dark rounded-3xl p-12 border border-gray-700"
          >
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to explore?
            </h2>
            <p className="text-xl text-gray-400 mb-8">
              Start searching through thousands of images with AI-powered intelligence
            </p>
            <Link
              href="/search"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-xl font-bold text-lg text-white bg-gradient-to-r from-primary-500 to-accent-500 hover:shadow-glow transition-all duration-300"
            >
              Launch App
              <ArrowRight className="w-5 h-5" />
            </Link>
          </motion.div>
        </section>

        {/* Footer */}
        <footer className="container mx-auto px-6 py-8 border-t border-gray-800">
          <div className="text-center text-gray-500">
            <p>Built with CLIP, BLIP-2, Flan-T5, and Stable Diffusion</p>
          </div>
        </footer>
      </div>
    </div>
  );
}
