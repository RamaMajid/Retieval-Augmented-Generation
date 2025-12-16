"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Clock, Star, Trash2, Download, Search, Image as ImageIcon, Type } from 'lucide-react';
import { api } from '@/lib/api';
import { SearchHistory } from '@/types';

interface HistorySidebarProps {
    isOpen: boolean;
    onClose: () => void;
    onReplay: (search: SearchHistory) => void;
}

export default function HistorySidebar({ isOpen, onClose, onReplay }: HistorySidebarProps) {
    const [searches, setSearches] = useState<SearchHistory[]>([]);
    const [loading, setLoading] = useState(false);
    const [searchFilter, setSearchFilter] = useState('');
    const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);

    // Load history on mount and when sidebar opens
    useEffect(() => {
        if (isOpen) {
            loadHistory();
        }
    }, [isOpen, showFavoritesOnly]);

    const loadHistory = async () => {
        setLoading(true);
        try {
            const response = await api.getHistory(50, 0, showFavoritesOnly);
            setSearches(response.searches);
        } catch (error) {
            console.error('Failed to load history:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleToggleFavorite = async (searchId: string) => {
        try {
            await api.toggleFavorite(searchId);
            // Update local state
            setSearches(searches.map(s =>
                s.id === searchId ? { ...s, is_favorite: !s.is_favorite } : s
            ));
        } catch (error) {
            console.error('Failed to toggle favorite:', error);
        }
    };

    const handleDelete = async (searchId: string) => {
        try {
            await api.deleteHistoryItem(searchId);
            setSearches(searches.filter(s => s.id !== searchId));
        } catch (error) {
            console.error('Failed to delete search:', error);
        }
    };

    const handleClearAll = async () => {
        if (!confirm('Are you sure you want to clear all history?')) return;

        try {
            await api.clearHistory();
            setSearches([]);
        } catch (error) {
            console.error('Failed to clear history:', error);
        }
    };

    const handleExport = async () => {
        try {
            const data = await api.exportHistory();
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `search-history-${new Date().toISOString()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Failed to export history:', error);
        }
    };

    const filteredSearches = searches.filter(search =>
        search.query.toLowerCase().includes(searchFilter.toLowerCase())
    );

    const formatTimestamp = (timestamp: string) => {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return 'Just now';
        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        return date.toLocaleDateString();
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
                    />

                    {/* Sidebar */}
                    <motion.div
                        initial={{ x: '100%' }}
                        animate={{ x: 0 }}
                        exit={{ x: '100%' }}
                        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                        className="fixed right-0 top-0 h-full w-full sm:w-96 bg-gradient-to-br from-gray-900/95 to-black/95 backdrop-blur-xl border-l border-white/10 shadow-2xl z-50 flex flex-col"
                    >
                        {/* Header */}
                        <div className="p-6 border-b border-white/10">
                            <div className="flex items-center justify-between mb-4">
                                <h2 className="text-2xl font-bold gradient-text">Search History</h2>
                                <button
                                    onClick={onClose}
                                    className="p-2 rounded-lg hover:bg-white/10 transition-colors"
                                >
                                    <X className="w-5 h-5" />
                                </button>
                            </div>

                            {/* Search filter */}
                            <div className="relative mb-3">
                                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                                <input
                                    type="text"
                                    placeholder="Search history..."
                                    value={searchFilter}
                                    onChange={(e) => setSearchFilter(e.target.value)}
                                    className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary/50 transition-colors"
                                />
                            </div>

                            {/* Filters */}
                            <div className="flex gap-2">
                                <button
                                    onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
                                    className={`flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-all ${showFavoritesOnly
                                            ? 'bg-primary/20 text-primary border border-primary/30'
                                            : 'bg-white/5 hover:bg-white/10 border border-white/10'
                                        }`}
                                >
                                    <Star className={`w-4 h-4 inline mr-1 ${showFavoritesOnly ? 'fill-primary' : ''}`} />
                                    Favorites
                                </button>
                                <button
                                    onClick={handleExport}
                                    className="px-3 py-2 rounded-lg text-sm font-medium bg-white/5 hover:bg-white/10 border border-white/10 transition-all"
                                >
                                    <Download className="w-4 h-4 inline mr-1" />
                                    Export
                                </button>
                                <button
                                    onClick={handleClearAll}
                                    className="px-3 py-2 rounded-lg text-sm font-medium bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-400 transition-all"
                                >
                                    <Trash2 className="w-4 h-4" />
                                </button>
                            </div>
                        </div>

                        {/* History list */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-3">
                            {loading ? (
                                <div className="text-center py-8 text-gray-400">Loading...</div>
                            ) : filteredSearches.length === 0 ? (
                                <div className="text-center py-8 text-gray-400">
                                    {searchFilter ? 'No matching searches' : 'No search history yet'}
                                </div>
                            ) : (
                                filteredSearches.map((search) => (
                                    <motion.div
                                        key={search.id}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        className="glass-dark p-4 rounded-xl border border-white/10 hover:border-primary/30 transition-all group cursor-pointer"
                                        onClick={() => onReplay(search)}
                                    >
                                        {/* Header */}
                                        <div className="flex items-start justify-between mb-2">
                                            <div className="flex items-center gap-2 flex-1">
                                                {search.query_type === 'text' ? (
                                                    <Type className="w-4 h-4 text-primary flex-shrink-0" />
                                                ) : (
                                                    <ImageIcon className="w-4 h-4 text-accent flex-shrink-0" />
                                                )}
                                                <span className="text-sm font-medium truncate">{search.query}</span>
                                            </div>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    handleToggleFavorite(search.id);
                                                }}
                                                className="p-1 hover:bg-white/10 rounded transition-colors"
                                            >
                                                <Star
                                                    className={`w-4 h-4 ${search.is_favorite ? 'fill-yellow-400 text-yellow-400' : 'text-gray-400'
                                                        }`}
                                                />
                                            </button>
                                        </div>

                                        {/* Metadata */}
                                        <div className="flex items-center gap-3 text-xs text-gray-400 mb-2">
                                            <span className="flex items-center gap-1">
                                                <Clock className="w-3 h-3" />
                                                {formatTimestamp(search.timestamp)}
                                            </span>
                                            <span>{search.num_results} results</span>
                                        </div>

                                        {/* Preview images */}
                                        {search.results.length > 0 && (
                                            <div className="flex gap-1 mb-2">
                                                {search.results.slice(0, 4).map((result, idx) => (
                                                    <div
                                                        key={idx}
                                                        className="w-12 h-12 rounded overflow-hidden bg-white/5"
                                                    >
                                                        <img
                                                            src={api.getImageUrl(result.image_path)}
                                                            alt=""
                                                            className="w-full h-full object-cover"
                                                        />
                                                    </div>
                                                ))}
                                                {search.results.length > 4 && (
                                                    <div className="w-12 h-12 rounded bg-white/5 flex items-center justify-center text-xs text-gray-400">
                                                        +{search.results.length - 4}
                                                    </div>
                                                )}
                                            </div>
                                        )}

                                        {/* Actions */}
                                        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    onReplay(search);
                                                }}
                                                className="flex-1 px-3 py-1.5 bg-primary/20 hover:bg-primary/30 text-primary text-xs font-medium rounded-lg transition-colors"
                                            >
                                                Replay
                                            </button>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    handleDelete(search.id);
                                                }}
                                                className="px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-medium rounded-lg transition-colors"
                                            >
                                                <Trash2 className="w-3 h-3" />
                                            </button>
                                        </div>
                                    </motion.div>
                                ))
                            )}
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}
