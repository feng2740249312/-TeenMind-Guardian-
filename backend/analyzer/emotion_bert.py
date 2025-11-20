"""
BERT情感分析模块（核心AI模块⭐⭐⭐⭐⭐）
"""

import torch
import torch.nn as nn
from transformers import BertTokenizer, BertForSequenceClassification
from typing import List, Dict
import numpy as np
import json
import os
from datetime import datetime

class EmotionAnalyzer:
    def __init__(self, model_path: str = None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model_name = model_path or 'hfl/chinese-bert-wwm-ext'
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.emotion_model = BertForSequenceClassification.from_pretrained(model_name, num_labels=6).to(self.device)
        self.slang_dict = self._load_slang_dict()
        self.emotion_labels = {0: 'positive',1: 'negative',2: 'neutral',3: 'depression',4: 'anxiety',5: 'suicidal'}
        self.risk_weights = {'positive': -10,'negative': 10,'neutral': 0,'depression': 30,'anxiety': 25,'suicidal': 50}

    def analyze(self, text: str) -> Dict:
        processed_text = self._preprocess_text(text)
        inputs = self.tokenizer(processed_text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.emotion_model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)[0]
        emotions = {label: float(probs[idx]) for idx, label in self.emotion_labels.items()}
        primary_emotion_idx = torch.argmax(probs).item()
        primary_emotion = self.emotion_labels[primary_emotion_idx]
        confidence = float(probs[primary_emotion_idx])
        risk_score = self._calculate_risk_score(emotions)
        keywords = self._extract_keywords(text)
        suggestion = self._generate_suggestion(primary_emotion, risk_score)
        return {
            'text': text,
            'processed_text': processed_text,
            'primary_emotion': primary_emotion,
            'confidence': confidence,
            'emotions': emotions,
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'keywords': keywords,
            'suggestion': suggestion,
            'timestamp': datetime.now().isoformat()
        }

    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        return [self.analyze(t) for t in texts]

    def _preprocess_text(self, text: str) -> str:
        processed = text
        for slang, standard in self.slang_dict.items():
            processed = processed.replace(slang, standard)
        import re
        processed = re.sub(r'[!！]{2,}', '！', processed)
        processed = re.sub(r'[?？]{2,}', '？', processed)
        processed = re.sub(r'[.。]{2,}', '。', processed)
        return processed

    def _calculate_risk_score(self, emotions: Dict[str, float]) -> float:
        score = 0.0
        for emotion, prob in emotions.items():
            score += prob * self.risk_weights.get(emotion, 0)
        score = max(0, min(100, score))
        return round(score, 2)

    def _get_risk_level(self, risk_score: float) -> str:
        if risk_score < 30:
            return '🟢 低风险'
        elif risk_score < 70:
            return '🟡 中风险'
        else:
            return '🔴 高风险'

    def _extract_keywords(self, text: str) -> List[str]:
        high_risk_keywords = ['自杀','想死','不想活','结束生命','解脱','抑郁','焦虑','崩溃','绝望','痛苦','失眠','孤独']
        return [k for k in high_risk_keywords if k in text]

    def _generate_suggestion(self, emotion: str, risk_score: float) -> str:
        if risk_score < 30:
            return '状态稳定，继续保持积极心态。'
        elif risk_score < 70:
            return '出现一些负面情绪，建议与信任的人沟通并保持规律作息。'
        else:
            return '高风险警示：建议立即寻求家人、朋友陪伴并联系专业心理咨询师。'

    def _load_slang_dict(self) -> Dict[str, str]:
        slang_file = 'data/teen_slang.json'
        if os.path.exists(slang_file):
            try:
                with open(slang_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    mapping = {}
                    for section in data.values():
                        if isinstance(section, dict):
                            for k,v in section.get('standard_mapping', {}).items():
                                mapping[k] = v
                    return mapping
            except Exception:
                pass
        return {'emo了': '情绪低落','破防了': '心理防线崩溃','麻了': '麻木','摆烂': '自暴自弃','躺平': '放弃努力'}
