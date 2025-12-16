'use client';

import React, { useState } from 'react';
import { Search, X } from 'lucide-react';
import { motion } from 'framer-motion';

interface TextQueryInputProps {
    onSearch: (query: string) => void;
    placeholder?: string;
}

export default function TextQueryInput({
    onSearch,
    placeholder = 'Describe the image you want to find...',
}: TextQueryInputProps) {
    const [query, setQuery] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query.trim());
        }
    };

    const handleClear = () => {
        setQuery('');
    };

    return (
        <form onSubmit={handleSubmit} className="w-full">
            <div className="relative">
                <div className="relative glass-dark rounded-2xl overflow-hidden border-2 border-gray-600 focus-within:border-primary-500 transition-all duration-300">
                    <div className="flex items-center gap-3 px-6 py-4">
                        <Search className="w-6 h-6 text-primary-400 flex-shrink-0" />
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder={placeholder}
                            className="flex-1 bg-transparent text-white placeholder-gray-400 outline-none text-lg"
                        />
                        {query && (
                            <motion.button
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                exit={{ scale: 0 }}
                                type="button"
                                onClick={handleClear}
                                className="p-2 rounded-full hover:bg-gray-700 transition-colors"
                            >
                                <X className="w-5 h-5 text-gray-400" />
                            </motion.button>
                        )}
                    </div>
                </div>

                {/* Character counter */}
                {query && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="absolute right-4 -bottom-6 text-xs text-gray-500"
                    >
                        {query.length} characters
                    </motion.div>
                )}
            </div>

            {/* Search button */}
            <motion.button
                type="submit"
                disabled={!query.trim()}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`
          mt-8 w-full py-4 rounded-xl font-bold text-lg text-white
          transition-all duration-300 shadow-lg
          ${query.trim()
                        ? 'bg-gradient-to-r from-primary-500 to-accent-500 hover:shadow-glow cursor-pointer'
                        : 'bg-gray-700 cursor-not-allowed opacity-50'
                    }
        `}
            >
                Search Images
            </motion.button>
        </form>
    );
}
