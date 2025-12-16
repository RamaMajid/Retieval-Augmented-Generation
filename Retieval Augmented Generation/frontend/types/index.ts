/**
 * TypeScript type definitions for the application.
 */

export interface SearchResult {
    rank: number;
    index: number;
    similarity: number;
    image_path: string;
    filename: string;
    caption?: string;
}

export interface SearchResponse {
    results: SearchResult[];
    query_type: 'text' | 'image';
    captions?: string[];
    narrative?: string;
}

export interface GeneratedImage {
    index: number;
    image_base64: string;
}

export interface GenerateImageResponse {
    prompt: string;
    num_images: number;
    images: GeneratedImage[];
    style?: string;
}

export interface DatasetInfo {
    indexed: boolean;
    num_images: number;
    embedding_dim?: number;
    clip_model?: string;
    has_generation?: boolean;
}

export interface LoadDatasetResponse {
    status: string;
    dataset: string;
    num_images: number;
    indexed: number;
}

export interface HealthCheckResponse {
    status: string;
    models_loaded: boolean;
    diffusion_loaded: boolean;
}

export type SearchMode = 'text' | 'image';

export interface UploadProgress {
    loaded: number;
    total: number;
    percentage: number;
}

// Search History Types
export interface SearchHistory {
    id: string;
    timestamp: string;
    query: string;
    query_type: 'text' | 'image';
    results: SearchResult[];
    narrative?: string;
    is_favorite: boolean;
    num_results: number;
}

export interface HistoryListResponse {
    searches: SearchHistory[];
    count: number;
    offset: number;
    limit: number;
}

export interface HistoryStats {
    total_searches: number;
    favorites: number;
    text_searches: number;
    image_searches: number;
    oldest_search: string | null;
    newest_search: string | null;
}
