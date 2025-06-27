import pandas as pd
from datetime import datetime
import os

class TutorMatcher:
    def __init__(self, model, peer_list, settings):
        self.model = model
        self.peers = peer_list
        self.cfg = settings

        # Create log file if not exists
        self.feature_log_path = "features_log.csv"
        if not os.path.exists(self.feature_log_path):
            pd.DataFrame(columns=[
                "karma_in_topic",
                "same_college",
                "days_since_last_help",
                "same_branch",
                "peer_year_match",
                "peer_id",
                "student_id",
                "timestamp"
            ]).to_csv(self.feature_log_path, index=False)

    def _build_features(self, student, peer, topic):
        today = datetime.today().date()
        topic_info = peer.get("topics", {}).get(topic, {})

        if not topic_info:
            return None

        try:
            karma_points = topic_info["karma"]
            last_help_date = datetime.strptime(topic_info["last_helped_on"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            return None

        inactive_days = (today - last_help_date).days

        feature_values = [
            float(karma_points),
            float(student.college == peer.get("college")),
            float(inactive_days),
            float(student.branch == peer.get("branch")),
            float(student.year == peer.get("year"))
        ]

        feature_df = pd.DataFrame([feature_values], columns=[
            "karma_in_topic",
            "same_college",
            "days_since_last_help",
            "same_branch",
            "peer_year_match"
        ])

        # Append to CSV for logging
        feature_df["peer_id"] = peer.get("peer_id")
        feature_df["student_id"] = student.user_id
        feature_df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        feature_df.to_csv(self.feature_log_path, mode='a', index=False, header=False)

        return feature_values, karma_points, inactive_days

    def recommend(self, student_request):
        topic = student_request.topic
        max_days = self.cfg.get("max_inactive_days", 14)
        karma_threshold = self.cfg.get("karma_threshold", 0)
        score_threshold = self.cfg.get("model_threshold", 0.7)
        limit = self.cfg.get("max_results", 3)

        suitable_peers = []

        for peer in self.peers:
            topic_data = peer.get("topics", {}).get(topic)
            if not topic_data or topic_data.get("karma", 0) < karma_threshold:
                continue

            features_pack = self._build_features(student_request, peer, topic)
            if features_pack is None:
                continue

            feature_values, karma_value, days_inactive = features_pack

            if days_inactive > max_days:
                continue

            prediction = (
                self.model.predict_proba([feature_values])[0][1]
                if hasattr(self.model, "predict_proba")
                else self.model.predict([feature_values])[0]
            )

            if prediction >= score_threshold:
                suitable_peers.append({
                    "peer_id": peer.get("peer_id"),
                    "name": peer.get("name"),
                    "college": peer.get("college"),
                    "karma_in_topic": karma_value,
                    "match_score": round(prediction, 2),
                    "predicted_help_probability": round(prediction, 2),
                    "last_helped_on": topic_data["last_helped_on"]
                })

        sorted_peers = sorted(suitable_peers, key=lambda p: p["match_score"], reverse=True)[:limit]

        return {
            "user_id": student_request.user_id,
            "matched_peers": sorted_peers,
            "status": "success" if sorted_peers else "no_match"
        }