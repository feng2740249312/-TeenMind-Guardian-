"""
共鸣网络分析模块（独特创新点⭐⭐⭐⭐⭐）
"""
import numpy as np
import networkx as nx
from typing import List, Dict
from collections import defaultdict
from datetime import datetime

class ResonanceNetworkAnalyzer:
    def __init__(self):
        self.resonance_weights = {'like':1.0,'comment':2.0,'share':3.0,'collect':2.5,'long_time':1.5}

    def analyze(self, user_id: str, content_ids: List[str], interactions: List[Dict]=None) -> Dict:
        interactions = interactions or self._fetch_interactions(user_id, content_ids)
        resonance_scores = self._calculate_resonance_scores(user_id, interactions)
        high_risk_contents = self._identify_high_risk_contents(resonance_scores)
        graph = self._build_resonance_network(user_id, interactions)
        cluster_users = self._cluster_users(user_id, graph)
        centrality_score = self._calculate_centrality(user_id, graph)
        overall_resonance = self._calculate_overall_resonance(resonance_scores)
        intervention_needed = overall_resonance > 0.7 or len(high_risk_contents) > 5
        intervention_suggestion = self._generate_intervention_suggestion(overall_resonance, high_risk_contents, cluster_users)
        return {
            'user_id': user_id,
            'resonance_intensity': overall_resonance,
            'resonance_scores': resonance_scores[:10],
            'high_risk_contents': high_risk_contents,
            'high_risk_count': len(high_risk_contents),
            'cluster_ids': cluster_users,
            'centrality_score': centrality_score,
            'needs_intervention': intervention_needed,
            'intervention_suggestion': intervention_suggestion,
            'network_stats': self._get_network_stats(graph),
            'analysis_timestamp': datetime.now().isoformat()
        }

    def _calculate_resonance_scores(self, user_id: str, interactions: List[Dict]) -> List[Dict]:
        content_resonance = defaultdict(float)
        details = {}
        for it in interactions:
            cid = it['content_id']
            w = self.resonance_weights.get(it['action_type'],1.0)
            content_resonance[cid] += w
            if cid not in details:
                details[cid] = {'content_id': cid,'content_text': it.get('content_text',''),'content_type': it.get('content_type','post')}
        max_score = max(content_resonance.values()) if content_resonance else 1
        lst = []
        for cid, score in content_resonance.items():
            lst.append({'content_id': cid,'resonance_score': round(score/max_score,3),'raw_score': score, **details[cid]})
        lst.sort(key=lambda x: x['resonance_score'], reverse=True)
        return lst

    def _identify_high_risk_contents(self, resonance_scores: List[Dict]) -> List[Dict]:
        keywords = ['自杀','想死','抑郁','绝望','痛苦','孤独']
        high = []
        for c in resonance_scores:
            risk = 0
            matched = []
            for k in keywords:
                if k in c.get('content_text',''):
                    risk += 10
                    matched.append(k)
            if c['resonance_score'] > 0.5 and risk > 0:
                high.append({**c,'risk_score': risk,'matched_keywords': matched})
        return high

    def _build_resonance_network(self, user_id: str, interactions: List[Dict]) -> nx.Graph:
        G = nx.Graph()
        G.add_node(user_id, node_type='user')
        for it in interactions:
            cid = it['content_id']
            if not G.has_node(cid):
                G.add_node(cid, node_type='content', content_text=it.get('content_text',''))
            w = self.resonance_weights.get(it['action_type'],1.0)
            if G.has_edge(user_id, cid):
                G[user_id][cid]['weight'] += w
            else:
                G.add_edge(user_id, cid, weight=w)
        return G

    def _cluster_users(self, user_id: str, graph: nx.Graph) -> List[str]:
        return [user_id]  # 简化占位

    def _calculate_centrality(self, user_id: str, graph: nx.Graph) -> float:
        try:
            deg = nx.degree_centrality(graph).get(user_id,0)
            bet = nx.betweenness_centrality(graph).get(user_id,0)
            return round((deg+bet)/2,3)
        except:
            return 0.0

    def _calculate_overall_resonance(self, scores: List[Dict]) -> float:
        if not scores: return 0.0
        high_count = sum(1 for s in scores if s['resonance_score']>0.7)
        avg_res = np.mean([s['resonance_score'] for s in scores])
        overall = high_count/len(scores)*0.4 + avg_res*0.6
        return round(overall,3)

    def _generate_intervention_suggestion(self, intensity: float, high_risk: List[Dict], cluster_users: List[str]) -> str:
        if intensity < 0.5 and len(high_risk) < 3:
            return '共鸣正常，继续观察。'
        if intensity < 0.7:
            return f'中度风险：对 {len(high_risk)} 个高危内容产生共鸣，建议推送积极内容。'
        return f'高风险：高强度共鸣与 {len(high_risk)} 个高危内容，需立即干预。'

    def _get_network_stats(self, graph: nx.Graph) -> Dict:
        return {'total_nodes': graph.number_of_nodes(),'total_edges': graph.number_of_edges(),'density': round(nx.density(graph),3) if graph.number_of_nodes()>0 else 0}

    def _fetch_interactions(self, user_id: str, content_ids: List[str]) -> List[Dict]:
        return [{'user_id': user_id,'content_id': cid,'action_type': 'like','content_text': f'Content {cid}','content_type': 'post'} for cid in content_ids]
