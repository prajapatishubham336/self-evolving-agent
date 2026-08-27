class Selector:
    def select_best_path(self, paths, scores):
        best_idx = max(range(len(scores)), key=lambda i: scores[i])
        return paths[best_idx]