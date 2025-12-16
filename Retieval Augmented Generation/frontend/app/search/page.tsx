'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Image as ImageIcon, ArrowLeft, Loader2, Sparkles, Clock } from 'lucide-react';
import Link from 'next/link';
import ImageUploader from '@/components/ImageUploader';
import TextQueryInput from '@/components/TextQueryInput';
import ImageGallery from '@/components/ImageGallery';
import GeneratedContent from '@/components/GeneratedContent';
import LoadingSpinner from '@/components/LoadingSpinner';
import HistorySidebar from '@/components/HistorySidebar';
import { SearchResponse, SearchMode, SearchHistory } from '@/types';
import api from '@/lib/api';

export default function SearchPage() {
    const [mode, setMode] = useState<SearchMode>('text');
    const [selectedImage, setSelectedImage] = useState<File | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [results, setResults] = useState<SearchResponse | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isHistoryOpen, setIsHistoryOpen] = useState(false);

    const handleTextSearch = async (query: string) => {
        setIsLoading(true);
        setError(null);
        setResults(null);

        try {
            const response = await api.searchByText(query, 12, true, true);
            setResults(response);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to search. Please make sure the backend is running and dataset is loaded.');
            console.error('Search error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleImageSearch = async () => {
        if (!selectedImage) return;

        setIsLoading(true);
        setError(null);
        setResults(null);

        try {
            const response = await api.searchByImage(selectedImage, 12, true, true);
            setResults(response);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to search. Please make sure the backend is running and dataset is loaded.');
            console.error('Search error:', err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen relative overflow-hidden bg-gray-950">
            {/* Background */}
            <div className="absolute inset-0 animated-gradient opacity-10"></div>
            <div className="absolute top-40 right-20 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl"></div>
            <div className="absolute bottom-20 left-20 w-72 h-72 bg-accent-500/20 rounded-full blur-3xl"></div>

            <div className="relative z-10">
                {/* Header */}
                <header className="border-b border-gray-800 glass-dark">
                    <div className="container mx-auto px-6 py-4">
                        <div className="flex items-center justify-between">
                            <Link href="/" className="flex items-center gap-2 group">
                                <ArrowLeft className="w-5 h-5 text-gray-400 group-hover:text-primary-400 transition-colors" />
                                <div className="flex items-center gap-2">
                                    <div className="p-2 rounded-lg bg-gradient-to-br from-primary-500 to-accent-500">
                                        <ImageIcon className="w-5 h-5 text-white" />
                                    </div>
                                    <span className="text-xl font-bold gradient-text">ImageRAG</span>
                                </div>
                            </Link>

                            <div className="flex items-center gap-4">
                                <button
                                    onClick={() => setIsHistoryOpen(true)}
                                    className="p-2 rounded-lg glass-dark hover:bg-white/10 transition-all group relative"
                                    title="Search History"
                                >
                                    <Clock className="w-5 h-5 text-gray-400 group-hover:text-primary-400 transition-colors" />
                                </button>
                                <span className="text-sm text-gray-400">
                                    {results ? `${results.results.length} results` : 'Ready to search'}
                                </span>
                            </div>
                        </div>
                    </div>
                </header>

                <div className="container mx-auto px-6 py-12">
                    {/* Search Interface */}
                    <div className="max-w-4xl mx-auto mb-12">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="text-center mb-8"
                        >
                            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
                                Search Images with AI
                            </h1>
                            <p className="text-gray-400 text-lg">
                                Upload an image or describe what you're looking for
                            </p>
                        </motion.div>

                        {/* Mode Tabs */}
                        <div className="flex gap-4 mb-8 justify-center">
                            <button
                                onClick={() => setMode('text')}
                                className={`
                  px-6 py-3 rounded-xl font-semibold transition-all duration-300 flex items-center gap-2
                  ${mode === 'text'
                                        ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-glow'
                                        : 'glass-dark text-gray-400 hover:text-white'
                                    }
                `}
                            >
                                <Search className="w-5 h-5" />
                                Text Query
                            </button>
                            <button
                                onClick={() => setMode('image')}
                                className={`
                  px-6 py-3 rounded-xl font-semibold transition-all duration-300 flex items-center gap-2
                  ${mode === 'image'
                                        ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-glow'
                                        : 'glass-dark text-gray-400 hover:text-white'
                                    }
                `}
                            >
                                <ImageIcon className="w-5 h-5" />
                                Image Upload
                            </button>
                        </div>

                        {/* Search Input */}
                        <AnimatePresence mode="wait">
                            {mode === 'text' ? (
                                <motion.div
                                    key="text"
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: 20 }}
                                >
                                    <TextQueryInput onSearch={handleTextSearch} />
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="image"
                                    initial={{ opacity: 0, x: 20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, x: -20 }}
                                >
                                    <ImageUploader
                                        onImageSelect={setSelectedImage}
                                        onImageRemove={() => setSelectedImage(null)}
                                        selectedImage={selectedImage}
                                    />
                                    {selectedImage && (
                                        <motion.button
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            onClick={handleImageSearch}
                                            disabled={isLoading}
                                            className="mt-6 w-full py-4 rounded-xl font-bold text-lg text-white bg-gradient-to-r from-primary-500 to-accent-500 hover:shadow-glow transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                                        >
                                            {isLoading ? (
                                                <>
                                                    <Loader2 className="w-5 h-5 animate-spin" />
                                                    Searching...
                                                </>
                                            ) : (
                                                <>
                                                    <Search className="w-5 h-5" />
                                                    Find Similar Images
                                                </>
                                            )}
                                        </motion.button>
                                    )}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>

                    {/* Loading State */}
                    {isLoading && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-center py-12"
                        >
                            <LoadingSpinner size="lg" message="Searching through images..." />
                        </motion.div>
                    )}

                    {/* Error State */}
                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="max-w-2xl mx-auto"
                        >
                            <div className="glass-dark rounded-xl p-6 border-2 border-red-500/50">
                                <p className="text-red-400 text-center">{error}</p>
                                <p className="text-gray-400 text-sm text-center mt-2">
                                    Make sure the backend server is running on http://localhost:8000
                                </p>
                            </div>
                        </motion.div>
                    )}

                    {/* Results */}
                    {results && !isLoading && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="space-y-8"
                        >
                            {/* Results Header */}
                            <div className="flex items-center justify-between">
                                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                                    <Sparkles className="w-6 h-6 text-primary-400" />
                                    Search Results
                                </h2>
                                <span className="text-gray-400">
                                    Found {results.results.length} similar images
                                </span>
                            </div>

                            {/* Image Gallery */}
                            <ImageGallery results={results.results} />

                            {/* Generated Narrative */}
                            {results.narrative && (
                                <GeneratedContent narrative={results.narrative} />
                            )}
                        </motion.div>
                    )}

                    {/* Empty State */}
                    {!results && !isLoading && !error && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="text-center py-20"
                        >
                            <div className="inline-flex p-6 rounded-full glass-dark mb-6">
                                <Search className="w-12 h-12 text-gray-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-400 mb-2">
                                No searches yet
                            </h3>
                            <p className="text-gray-500">
                                Start by entering a text query or uploading an image
                            </p>
                        </motion.div>
                    )}
                </div>
            </div>

            {/* History Sidebar */}
            <HistorySidebar
                isOpen={isHistoryOpen}
                onClose={() => setIsHistoryOpen(false)}
                onReplay={(search: SearchHistory) => {
                    // Close sidebar
                    setIsHistoryOpen(false);

                    // Set mode based on search type
                    setMode(search.query_type);

                    // ⚡ OPTIMIZED: Load cached results directly from history JSON
                    // No need to re-run expensive search operations!
                    setResults({
                        results: search.results,
                        query_type: search.query_type,
                        narrative: search.narrative
                    });

                    // Scroll to top to show results
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
            />
        </div>
    );
}
