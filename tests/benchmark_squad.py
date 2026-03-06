#!/usr/bin/env python3
"""
SQuAD Benchmark for Glyphobetic Compression
Tests: compression ratio, embedding similarity, retrieval accuracy
"""

import json
import numpy as np
from typing import List, Dict, Tuple
import os

# Import glyphobetic encoder (will be built)
import sys
sys.path.insert(0, '/root/.openclaw/workspace')

try:
    from app.js.syllable_mapper import encode_word
except ImportError:
    # Fallback encoder until full system ready
    def encode_word(word: str) -> str:
        """Simple bigram encoder for testing"""
        LETTER_MAP = {
            'A': ('a', 'curve'), 'B': ('f', 'line'), 'C': ('g', 'point'),
            'D': ('e', 'curve'), 'E': ('d', 'line'), 'F': ('f', 'line'),
            'G': ('a', 'curve'), 'H': ('d', 'curve'), 'I': ('b', 'point'),
            'J': ('a', 'curve'), 'K': ('a', 'line'), 'L': ('e', 'line'),
            'M': ('f', 'curve'), 'N': ('c', 'line'), 'O': ('e', 'curve'),
            'P': ('f', 'point'), 'Q': ('g', 'curve'), 'R': ('g', 'line'),
            'S': ('a', 'point'), 'T': ('f', 'line'), 'U': ('c', 'curve'),
            'V': ('f', 'curve'), 'W': ('f', 'line'), 'X': ('g', 'line'),
            'Y': ('g', 'curve'), 'Z': ('e', 'point')
        }
        
        word = word.upper()
        segments = {}
        
        for letter in word:
            if letter in LETTER_MAP:
                seg, atom = LETTER_MAP[letter]
                if seg not in segments:
                    segments[seg] = []
                segments[seg].append(atom)
        
        # Merge atoms per segment
        ATOM_PRIORITY = {'curve': 3, 'line': 2, 'point': 1}
        ATOM_SYMBOLS = {'curve': '￿', 'line': '—', 'point': '·'}
        
        glyph_parts = []
        for seg in ['f', 'e', 'a', 'd', 'b', 'c', 'g']:
            if seg in segments:
                atoms = segments[seg]
                merged = max(atoms, key=lambda a: ATOM_PRIORITY.get(a, 0))
                glyph_parts.append(ATOM_SYMBOLS.get(merged, '∅'))
            else:
                glyph_parts.append('∅')
        
        return ''.join(glyph_parts)


class MockEmbedding:
    """Mock embedding for testing without API"""
    
    def __init__(self, dim: int = 1536):
        self.dim = dim
        self.cache = {}
    
    def embed(self, text: str) -> np.ndarray:
        """Deterministic mock embedding based on text hash"""
        if text in self.cache:
            return self.cache[text]
        
        # Deterministic pseudo-random embedding
        np.random.seed(hash(text) % 2**32)
        vec = np.random.randn(self.dim)
        vec = vec / np.linalg.norm(vec)  # Normalize
        self.cache[text] = vec
        return vec


class GlyphobeticBenchmark:
    """Benchmark suite for glyphobetic compression"""
    
    def __init__(self, embedding_dim: int = 1536):
        self.embedder = MockEmbedding(embedding_dim)
        self.results = []
    
    def create_minimal_squad(self, n: int = 100) -> List[Dict]:
        """Create minimal SQuAD-like dataset for testing"""
        
        # Simplified QA pairs for testing
        qa_pairs = [
            {
                "question": "What is the capital of France?",
                "context": "Paris is the capital and most populous city of France.",
                "answer": "Paris"
            },
            {
                "question": "Who wrote Romeo and Juliet?",
                "context": "William Shakespeare wrote the play Romeo and Juliet.",
                "answer": "William Shakespeare"
            },
            {
                "question": "What is the largest planet?",
                "context": "Jupiter is the largest planet in the solar system.",
                "answer": "Jupiter"
            },
            {
                "question": "When did World War II end?",
                "context": "World War II ended in 1945.",
                "answer": "1945"
            },
            {
                "question": "What is the speed of light?",
                "context": "The speed of light is approximately 299,792 kilometers per second.",
                "answer": "299,792 kilometers per second"
            },
            {
                "question": "Who painted the Mona Lisa?",
                "context": "Leonardo da Vinci painted the Mona Lisa.",
                "answer": "Leonardo da Vinci"
            },
            {
                "question": "What is the chemical formula for water?",
                "context": "Water has the chemical formula H2O.",
                "answer": "H2O"
            },
            {
                "question": "What is the tallest mountain?",
                "context": "Mount Everest is the tallest mountain above sea level.",
                "answer": "Mount Everest"
            },
            {
                "question": "Who invented the telephone?",
                "context": "Alexander Graham Bell invented the telephone.",
                "answer": "Alexander Graham Bell"
            },
            {
                "question": "What is the smallest prime number?",
                "context": "Two is the smallest prime number.",
                "answer": "Two"
            }
        ]
        
        # Repeat to reach n samples
        dataset = []
        for i in range(n):
            base = qa_pairs[i % len(qa_pairs)]
            dataset.append({
                "id": f"test_{i}",
                **base
            })
        
        return dataset
    
    def compress_text(self, text: str) -> Tuple[str, Dict]:
        """Compress text and return glyph + metrics"""
        words = text.split()
        compressed_words = []
        
        for word in words:
            # Remove punctuation for encoding
            clean_word = ''.join(c for c in word if c.isalpha())
            if clean_word:
                glyph = encode_word(clean_word)
                compressed_words.append(glyph)
        
        compressed = ' '.join(compressed_words)
        
        # Metrics
        raw_bytes = len(text.encode('utf-8'))
        compressed_bytes = len(compressed.encode('utf-8'))
        ratio = raw_bytes / compressed_bytes if compressed_bytes > 0 else 0
        
        return compressed, {
            'raw_bytes': raw_bytes,
            'compressed_bytes': compressed_bytes,
            'ratio': ratio,
            'raw_words': len(words),
            'compressed_words': len(compressed_words)
        }
    
    def measure_similarity(self, text1: str, text2: str) -> float:
        """Measure cosine similarity between embeddings"""
        emb1 = self.embedder.embed(text1)
        emb2 = self.embedder.embed(text2)
        
        similarity = np.dot(emb1, emb2)
        return float(similarity)
    
    def test_retrieval(self, dataset: List[Dict], k: int = 5) -> Dict:
        """Test retrieval accuracy with compressed queries"""
        
        correct = 0
        total = 0
        similarities = []
        
        for item in dataset[:k]:
            question = item['question']
            context = item['context']
            
            # Compress question
            compressed_q, metrics = self.compress_text(question)
            
            # Measure similarity between compressed and original context
            sim = self.measure_similarity(compressed_q, context)
            similarities.append(sim)
            
            # Simple retrieval: does compression maintain semantic signal?
            # (In real test, would retrieve from corpus)
            if sim > 0.1:  # Threshold for mock embeddings
                correct += 1
            total += 1
        
        return {
            'accuracy': correct / total if total > 0 else 0,
            'avg_similarity': np.mean(similarities) if similarities else 0,
            'min_similarity': np.min(similarities) if similarities else 0,
            'max_similarity': np.max(similarities) if similarities else 0
        }
    
    def run_full_benchmark(self, n_samples: int = 100) -> Dict:
        """Run complete benchmark suite"""
        
        print("=" * 60)
        print("GLYPHOBETIC COMPRESSION BENCHMARK")
        print("=" * 60)
        
        # Create dataset
        print(f"\n1. Creating dataset ({n_samples} samples)...")
        dataset = self.create_minimal_squad(n_samples)
        
        # Compression test
        print("\n2. Testing compression...")
        all_metrics = []
        for item in dataset[:10]:  # Test on subset
            text = item['context']
            compressed, metrics = self.compress_text(text)
            all_metrics.append(metrics)
            
            print(f"  Raw: {text[:40]}...")
            print(f"  Compressed: {compressed[:40]}...")
            print(f"  Ratio: {metrics['ratio']:.2f}:1")
        
        avg_ratio = np.mean([m['ratio'] for m in all_metrics])
        print(f"\n  Average compression ratio: {avg_ratio:.2f}:1")
        
        # Similarity test
        print("\n3. Testing embedding similarity...")
        similarities = []
        for item in dataset[:10]:
            original = item['question']
            compressed, _ = self.compress_text(original)
            sim = self.measure_similarity(original, compressed)
            similarities.append(sim)
        
        avg_sim = np.mean(similarities)
        print(f"  Average cosine similarity: {avg_sim:.4f}")
        print(f"  (1.0 = identical, 0.0 = orthogonal)")
        
        # Retrieval test
        print("\n4. Testing retrieval accuracy...")
        retrieval = self.test_retrieval(dataset, k=20)
        print(f"  Recall@{20}: {retrieval['accuracy']:.2%}")
        print(f"  Avg similarity: {retrieval['avg_similarity']:.4f}")
        
        # Summary
        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)
        
        results = {
            'compression_ratio': avg_ratio,
            'embedding_similarity': avg_sim,
            'retrieval_accuracy': retrieval['accuracy'],
            'retrieval_similarity': retrieval['avg_similarity'],
            'samples_tested': n_samples,
            'pass_threshold': {
                'compression': avg_ratio >= 2.0,
                'similarity': avg_sim >= 0.7,
                'retrieval': retrieval['accuracy'] >= 0.8
            }
        }
        
        print(f"\nCompression Ratio: {avg_ratio:.2f}:1 " + 
              ("✓ PASS" if results['pass_threshold']['compression'] else "✗ FAIL"))
        print(f"Embedding Similarity: {avg_sim:.4f} " +
              ("✓ PASS" if results['pass_threshold']['similarity'] else "✗ FAIL"))
        print(f"Retrieval Accuracy: {retrieval['accuracy']:.2%} " +
              ("✓ PASS" if results['pass_threshold']['retrieval'] else "✗ FAIL"))
        
        return results


def main():
    """Run benchmark from command line"""
    benchmark = GlyphobeticBenchmark()
    results = benchmark.run_full_benchmark(n_samples=100)
    
    # Save results (convert numpy bools to Python bools)
    output_path = '/root/.openclaw/workspace/tests/benchmark_results.json'
    json_safe_results = {
        k: bool(v) if isinstance(v, (np.bool_, bool)) else v 
        for k, v in results.items()
    }
    # Handle nested dict
    if 'pass_threshold' in json_safe_results:
        json_safe_results['pass_threshold'] = {
            k: bool(v) for k, v in json_safe_results['pass_threshold'].items()
        }
    with open(output_path, 'w') as f:
        json.dump(json_safe_results, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    
    # Exit code based on pass/fail
    all_pass = all(results['pass_threshold'].values())
    return 0 if all_pass else 1


if __name__ == '__main__':
    exit(main())
