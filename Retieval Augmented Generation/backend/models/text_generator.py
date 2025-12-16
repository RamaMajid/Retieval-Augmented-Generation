"""
Text Generator using Flan-T5 for narrative generation.
"""
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List, Dict

from config import settings


class TextGenerator:
    """
    Text generation model for creating narratives based on retrieved images.
    """
    
    def __init__(self, model_name: str = None, device: str = None):
        """
        Initialize text generator.
        
        Args:
            model_name: HuggingFace model name (default from settings)
            device: Device to run model on (default from settings)
        """
        self.model_name = model_name or settings.TEXT_GEN_MODEL
        self.device = device or settings.DEVICE
        
        print(f"Loading Text Generation model: {self.model_name}")
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            cache_dir=settings.MODEL_CACHE_DIR
        )
        
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name,
            cache_dir=settings.MODEL_CACHE_DIR,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)
        
        self.model.eval()
        print("Text generation model loaded successfully!")
    
    def generate_narrative(
        self,
        captions: List[str],
        query: str = None,
        max_length: int = None,
        temperature: float = 0.8,
        top_p: float = 0.9
    ) -> str:
        """
        Generate a narrative based on image captions and query.
        
        Args:
            captions: List of captions from retrieved images
            query: Original search query (optional)
            max_length: Maximum narrative length (default from settings)
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated narrative as string
        """
        max_length = max_length or settings.MAX_NARRATIVE_LENGTH
        
        # Build prompt for RAG
        prompt = self._build_rag_prompt(captions, query)
        
        # Tokenize input
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(self.device)
        
        # Generate text
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                num_beams=4,
                early_stopping=True
            )
        
        # Decode output
        narrative = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).strip()
        
        return narrative
    
    def _build_rag_prompt(self, captions: List[str], query: str = None) -> str:
        """
        Build a prompt for RAG-based generation.
        
        Args:
            captions: List of image captions
            query: Original search query
            
        Returns:
            Formatted prompt string
        """
        # Combine captions
        context = " ".join(captions[:5])  # Use top 5 captions
        
        if query:
            prompt = f"""Based on the search query "{query}", here are descriptions of relevant images: {context}
            
Write a coherent narrative that connects these images and relates to the query."""
        else:
            prompt = f"""Here are descriptions of similar images: {context}
            
Write a coherent narrative that describes what these images have in common."""
        
        return prompt
    
    def generate_summary(
        self,
        text: str,
        max_length: int = 100
    ) -> str:
        """
        Generate a summary of given text.
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            
        Returns:
            Summary as string
        """
        prompt = f"Summarize: {text}"
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=4,
                early_stopping=True
            )
        
        summary = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).strip()
        
        return summary
    
    def answer_question(
        self,
        question: str,
        context: str,
        max_length: int = 100
    ) -> str:
        """
        Answer a question based on context.
        
        Args:
            question: Question to answer
            context: Context to use for answering
            max_length: Maximum answer length
            
        Returns:
            Answer as string
        """
        prompt = f"Question: {question}\nContext: {context}\nAnswer:"
        
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_beams=4,
                early_stopping=True
            )
        
        answer = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).strip()
        
        return answer
