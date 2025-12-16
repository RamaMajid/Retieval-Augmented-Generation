'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface LoadingSpinnerProps {
    size?: 'sm' | 'md' | 'lg';
    message?: string;
}

export default function LoadingSpinner({
    size = 'md',
    message,
}: LoadingSpinnerProps) {
    const sizeClasses = {
        sm: 'w-8 h-8',
        md: 'w-16 h-16',
        lg: 'w-24 h-24',
    };

    return (
        <div className="flex flex-col items-center justify-center gap-4 p-8">
            <motion.div
                className={`${sizeClasses[size]} relative`}
                animate={{ rotate: 360 }}
                transition={{
                    duration: 1,
                    repeat: Infinity,
                    ease: 'linear',
                }}
            >
                <div className="absolute inset-0 rounded-full border-4 border-gray-700"></div>
                <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-primary-500 border-r-accent-500"></div>
            </motion.div>

            {message && (
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-gray-400 text-center"
                >
                    {message}
                </motion.p>
            )}
        </div>
    );
}

export function SkeletonLoader({ className = '' }: { className?: string }) {
    return (
        <div className={`skeleton ${className}`}>
            <div className="shimmer"></div>
        </div>
    );
}

export function ImageSkeleton() {
    return (
        <div className="space-y-3">
            <SkeletonLoader className="w-full aspect-square rounded-xl" />
            <SkeletonLoader className="w-3/4 h-4 rounded" />
            <SkeletonLoader className="w-1/2 h-3 rounded" />
        </div>
    );
}
