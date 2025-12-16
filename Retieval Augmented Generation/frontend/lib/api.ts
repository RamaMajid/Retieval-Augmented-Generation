/**
 * API client for communicating with the backend.
 */
import axios, { AxiosInstance, AxiosProgressEvent } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error);
        return Promise.reject(error);
    }
);

// API methods
export const api = {
    /**
     * Health check
     */
    healthCheck: async () => {
        const response = await apiClient.get('/api/health');
        return response.data;
    },

    /**
     * Search by text query
     */
    searchByText: async (
        query: string,
        k: number = 10,
        generateCaptions: boolean = true,
        generateNarrative: boolean = true
    ) => {
        const response = await apiClient.post('/api/search-by-text', {
            query,
            k,
            generate_captions: generateCaptions,
            generate_narrative: generateNarrative,
        });
        return response.data;
    },

    /**
     * Search by image upload
     */
    searchByImage: async (
        imageFile: File,
        k: number = 10,
        generateCaptions: boolean = true,
        generateNarrative: boolean = true,
        onUploadProgress?: (progressEvent: AxiosProgressEvent) => void
    ) => {
        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('k', k.toString());
        formData.append('generate_captions', generateCaptions.toString());
        formData.append('generate_narrative', generateNarrative.toString());

        const response = await apiClient.post('/api/search-by-image', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            onUploadProgress,
        });
        return response.data;
    },

    /**
     * Generate image from prompt
     */
    generateImage: async (
        prompt: string,
        negativePrompt: string = 'blurry, bad quality, distorted',
        numImages: number = 1,
        style: string = 'photorealistic'
    ) => {
        const response = await apiClient.post('/api/generate-image', {
            prompt,
            negative_prompt: negativePrompt,
            num_images: numImages,
            style,
        });
        return response.data;
    },

    /**
     * Generate images from captions
     */
    generateFromCaptions: async (
        captions: string[],
        style: string = 'photorealistic',
        numImages: number = 1
    ) => {
        const response = await apiClient.post('/api/generate-from-captions', {
            captions,
            style,
            num_images: numImages,
        });
        return response.data;
    },

    /**
     * Load dataset
     */
    loadDataset: async (
        datasetName: string,
        split: string = 'train',
        customPath?: string
    ) => {
        const response = await apiClient.post('/api/load-dataset', {
            dataset_name: datasetName,
            split,
            custom_path: customPath,
        });
        return response.data;
    },

    /**
     * Get dataset info
     */
    getDatasetInfo: async () => {
        const response = await apiClient.get('/api/dataset-info');
        return response.data;
    },

    /**
     * Get image URL
     */
    getImageUrl: (imagePath: string) => {
        // Ensure forward slashes for URL
        const normalizedPath = imagePath.replace(/\\/g, '/');
        return `${API_URL}/api/image/${normalizedPath}`;
    },

    // ========================================================================
    // Search History Methods
    // ========================================================================

    /**
     * Get search history list
     */
    getHistory: async (
        limit: number = 50,
        offset: number = 0,
        favoritesOnly: boolean = false
    ) => {
        const response = await apiClient.get('/api/history/list', {
            params: { limit, offset, favorites_only: favoritesOnly }
        });
        return response.data;
    },

    /**
     * Get specific search from history
     */
    getHistoryItem: async (searchId: string) => {
        const response = await apiClient.get(`/api/history/${searchId}`);
        return response.data;
    },

    /**
     * Delete search from history
     */
    deleteHistoryItem: async (searchId: string) => {
        const response = await apiClient.delete(`/api/history/${searchId}`);
        return response.data;
    },

    /**
     * Clear all search history
     */
    clearHistory: async () => {
        const response = await apiClient.delete('/api/history/clear/all');
        return response.data;
    },

    /**
     * Toggle favorite status
     */
    toggleFavorite: async (searchId: string) => {
        const response = await apiClient.post(`/api/history/${searchId}/favorite`);
        return response.data;
    },

    /**
     * Export all history
     */
    exportHistory: async () => {
        const response = await apiClient.get('/api/history/export/all');
        return response.data;
    },

    /**
     * Get history statistics
     */
    getHistoryStats: async () => {
        const response = await apiClient.get('/api/history/stats');
        return response.data;
    },
};

export default api;
