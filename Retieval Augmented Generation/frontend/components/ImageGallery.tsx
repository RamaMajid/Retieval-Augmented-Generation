'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Download, Maximize2 } from 'lucide-react';
import { SearchResult } from '@/types';
import api from '@/lib/api';

interface ImageGalleryProps {
    results: SearchResult[];
}

export default function ImageGallery({ results }: ImageGalleryProps) {
    const [selectedImage, setSelectedImage] = useState<SearchResult | null>(null);

    const containerVariants = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1,
            },
        },
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        show: { opacity: 1, y: 0 },
    };

    return (
        <>
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="show"
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
            >
                {results.map((result, index) => (
                    <motion.div
                        key={result.index}
                        variants={itemVariants}
                        whileHover={{ scale: 1.05 }}
                        className="group relative cursor-pointer"
                        onClick={() => setSelectedImage(result)}
                    >
                        <div className="relative aspect-square rounded-xl overflow-hidden bg-gray-900 shadow-lg group-hover:shadow-glow transition-all duration-300">
                            <img
                                src={api.getImageUrl(result.image_path)}
                                alt={result.caption || result.filename}
                                className="w-full h-full object-cover"
                            />

                            {/* Overlay */}
                            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                                <div className="absolute bottom-0 left-0 right-0 p-4">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-xs font-bold text-white bg-primary-500 px-2 py-1 rounded">
                                            #{result.rank}
                                        </span>
                                        <span className="text-xs font-semibold text-white bg-black/50 px-2 py-1 rounded">
                                            {(result.similarity * 100).toFixed(1)}% match
                                        </span>
                                    </div>
                                    {result.caption && (
                                        <p className="text-sm text-white line-clamp-2">
                                            {result.caption}
                                        </p>
                                    )}
                                </div>
                            </div>

                            {/* Expand icon */}
                            <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
                                <div className="p-2 rounded-full bg-black/50 backdrop-blur-sm">
                                    <Maximize2 className="w-4 h-4 text-white" />
                                </div>
                            </div>
                        </div>

                        {/* Similarity bar */}
                        <div className="mt-3 h-1 bg-gray-700 rounded-full overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${result.similarity * 100}%` }}
                                transition={{ duration: 0.5, delay: index * 0.05 }}
                                className="h-full bg-gradient-to-r from-primary-500 to-accent-500"
                            />
                        </div>
                    </motion.div>
                ))}
            </motion.div>

            {/* Modal */}
            <AnimatePresence>
                {selectedImage && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm"
                        onClick={() => setSelectedImage(null)}
                    >
                        <motion.div
                            initial={{ scale: 0.9, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.9, opacity: 0 }}
                            className="relative max-w-4xl w-full bg-gray-900 rounded-2xl overflow-hidden shadow-2xl"
                            onClick={(e) => e.stopPropagation()}
                        >
                            {/* Close button */}
                            <button
                                onClick={() => setSelectedImage(null)}
                                className="absolute top-4 right-4 z-10 p-2 rounded-full bg-black/50 hover:bg-black/70 text-white transition-colors"
                            >
                                <X className="w-6 h-6" />
                            </button>

                            {/* Image */}
                            <div className="relative aspect-video bg-black flex items-center justify-center">
                                <img
                                    src={api.getImageUrl(selectedImage.image_path)}
                                    alt={selectedImage.caption || selectedImage.filename}
                                    className="max-w-full max-h-full object-contain"
                                />
                            </div>

                            {/* Info */}
                            <div className="p-6 space-y-4">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <h3 className="text-xl font-bold text-white mb-1">
                                            Rank #{selectedImage.rank}
                                        </h3>
                                        <p className="text-sm text-gray-400">
                                            {selectedImage.filename}
                                        </p>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-2xl font-bold gradient-text">
                                            {(selectedImage.similarity * 100).toFixed(1)}%
                                        </p>
                                        <p className="text-xs text-gray-400">Similarity</p>
                                    </div>
                                </div>

                                {selectedImage.caption && (
                                    <div className="p-4 rounded-xl glass-dark">
                                        <p className="text-sm text-gray-400 mb-1">Caption</p>
                                        <p className="text-white">{selectedImage.caption}</p>
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
}
