from logger.logger import CustomLogger


class DataFinder:
    def __init__(self, data):
        self.data = data
        self.logger = CustomLogger()  # Можна не передавати, тоді логер не використовується

    def find(self, target_key: str, count: int = None, parent: bool = False):
        try:
            results = self._search(self.data, target_key, parent)
            # self.logger.error_log(f"Знайдено {len(results)} результат(ів) за ключем '{target_key}'", status='info')

            if isinstance(count, int):
                if 0 <= count < len(results):
                    value = list(results[count].values())[0]

                    return value
                else:
                    self.logger.error_log(f"Індекс {count} виходить за межі результатів для ключа '{target_key}'", status='war')
                    return None

            return results

        except Exception as e:
            self.logger.error_log(e)
            return None

    def _search(self, data, target_key: str, parent: bool, parent_key=None):
        results = []

        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    if parent:
                        results.append({parent_key or "root": data})
                    else:
                        results.append({key: value})
                results.extend(self._search(value, target_key, parent, key))

        elif isinstance(data, list):
            for item in data:
                results.extend(self._search(item, target_key, parent, parent_key))

        return results
