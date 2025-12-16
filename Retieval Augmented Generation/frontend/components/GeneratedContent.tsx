'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Copy, Check, RefreshCw } from 'lucide-react';

interface GeneratedContentProps {
    narrative?: string;
    onRegenerate?: () => void;
}

export default function GeneratedContent({
    narrative,
    onRegenerate,
}: GeneratedContentProps) {
    const [displayedText, setDisplayedText] = useState('');
    const [copied, setCopied] = useState(false);
    const [isTyping, setIsTyping] = useState(true);

    useEffect(() => {
        if (!narrative) return;

        setIsTyping(true);
        setDisplayedText('');
        let currentIndex = 0;

        const interval = setInterval(() => {
            if (currentIndex < narrative.length) {
                setDisplayedText(narrative.slice(0, currentIndex + 1));
                currentIndex++;
            } else {
                setIsTyping(false);
                clearInterval(interval);
            }
        }, 20);

        return () => clearInterval(interval);
    }, [narrative]);

    const handleCopy = async () => {
        if (narrative) {
            await navigator.clipboard.writeText(narrative);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

    if (!narrative) return null;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8"
        >
            <div className="glass-dark rounded-2xl p-6 border border-gray-700">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold gradient-text">
                        Generated Narrative
                    </h3>
                    <div className="flex gap-2">
                        {onRegenerate && (
                            <button
                                onClick={onRegenerate}
                                className="p-2 rounded-lg hover:bg-gray-700 transition-colors group"
                                title="Regenerate"
                            >
                                <RefreshCw className="w-5 h-5 text-gray-400 group-hover:text-primary-400 transition-colors" />
                            </button>
                        )}
                        <button
                            onClick={handleCopy}
                            className="p-2 rounded-lg hover:bg-gray-700 transition-colors group"
                            title="Copy to clipboard"
                        >
                            {copied ? (
                                <Check className="w-5 h-5 text-green-400" />
                            ) : (
                                <Copy className="w-5 h-5 text-gray-400 group-hover:text-primary-400 transition-colors" />
                            )}
                        </button>
                    </div>
                </div>

                <div className="relative">
                    <p className="text-white leading-relaxed">
                        {displayedText}
                        {isTyping && (
                            <motion.span
                                animate={{ opacity: [1, 0] }}
                                transition={{ duration: 0.5, repeat: Infinity }}
                                className="inline-block w-0.5 h-5 bg-primary-500 ml-1"
                            />
                        )}
                    </p>
                </div>
            </div>
        </motion.div>
    );
}
