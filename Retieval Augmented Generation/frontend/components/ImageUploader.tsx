'use client';

import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, Image as ImageIcon } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Image from 'next/image';

interface ImageUploaderProps {
    onImageSelect: (file: File) => void;
    onImageRemove: () => void;
    selectedImage: File | null;
}

export default function ImageUploader({
    onImageSelect,
    onImageRemove,
    selectedImage,
}: ImageUploaderProps) {
    const [preview, setPreview] = useState<string | null>(null);

    const onDrop = useCallback(
        (acceptedFiles: File[]) => {
            if (acceptedFiles.length > 0) {
                const file = acceptedFiles[0];
                onImageSelect(file);

                // Create preview
                const reader = new FileReader();
                reader.onload = () => {
                    setPreview(reader.result as string);
                };
                reader.readAsDataURL(file);
            }
        },
        [onImageSelect]
    );

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.png', '.jpg', '.jpeg', '.webp', '.bmp'],
        },
        maxFiles: 1,
    });

    const handleRemove = () => {
        setPreview(null);
        onImageRemove();
    };

    return (
        <div className="w-full">
            <AnimatePresence mode="wait">
                {!selectedImage ? (
                    <motion.div
                        key="dropzone"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                    >
                        <div
                            {...getRootProps()}
                            className={`
                relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer
                transition-all duration-300 glass-dark
                ${isDragActive
                                    ? 'border-primary-500 bg-primary-500/10 scale-105'
                                    : 'border-gray-600 hover:border-primary-400 hover:bg-primary-500/5'
                                }
              `}
                        >
                            <input {...getInputProps()} />
                            <motion.div
                                animate={isDragActive ? { scale: 1.1 } : { scale: 1 }}
                                transition={{ duration: 0.2 }}
                                className="flex flex-col items-center gap-4"
                            >
                                <div className="p-6 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 shadow-glow">
                                    <Upload className="w-12 h-12 text-white" />
                                </div>
                                <div>
                                    <p className="text-xl font-semibold text-white mb-2">
                                        {isDragActive ? 'Drop your image here' : 'Upload an image'}
                                    </p>
                                    <p className="text-gray-400">
                                        Drag & drop or click to browse
                                    </p>
                                    <p className="text-sm text-gray-500 mt-2">
                                        Supports: PNG, JPG, JPEG, WebP, BMP
                                    </p>
                                </div>
                            </motion.div>
                        </div>
                    </motion.div>
                ) : (
                    <motion.div
                        key="preview"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        transition={{ duration: 0.2 }}
                        className="relative"
                    >
                        <div className="relative rounded-2xl overflow-hidden glass-dark p-4">
                            <div className="relative aspect-video rounded-xl overflow-hidden bg-gray-900">
                                {preview && (
                                    <Image
                                        src={preview}
                                        alt="Preview"
                                        fill
                                        className="object-contain"
                                    />
                                )}
                            </div>
                            <button
                                onClick={handleRemove}
                                className="absolute top-6 right-6 p-2 rounded-full bg-red-500 hover:bg-red-600 text-white transition-all duration-200 hover:scale-110 shadow-lg"
                            >
                                <X className="w-5 h-5" />
                            </button>
                            <div className="mt-4 flex items-center gap-3 text-white">
                                <ImageIcon className="w-5 h-5 text-primary-400" />
                                <span className="text-sm font-medium truncate">
                                    {selectedImage.name}
                                </span>
                                <span className="text-xs text-gray-400">
                                    ({(selectedImage.size / 1024).toFixed(1)} KB)
                                </span>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
