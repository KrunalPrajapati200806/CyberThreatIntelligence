const HISTORY_KEY = "cyberintel_analysis_history_v1";

export function getHistory() {
  try {
    const stored = localStorage.getItem(HISTORY_KEY);

    if (!stored) {
      return [];
    }

    const parsed = JSON.parse(stored);

    return Array.isArray(parsed)
      ? parsed
      : [];
  } catch (error) {
    console.error("Failed to load analysis history:", error);
    return [];
  }
}


export function saveAnalysisHistory(file, result) {
  try {
    const history = getHistory();

    const entry = {
      id:
        typeof crypto !== "undefined" &&
        crypto.randomUUID
          ? crypto.randomUUID()
          : `${Date.now()}-${Math.random()}`,

      fileName: file?.name || "Unknown file",

      fileSize: file?.size || 0,

      analyzedAt:
        new Date().toISOString(),

      totalFlows:
        result?.total_flows || 0,

      attacks:
        result?.attacks || 0,

      benign:
        result?.benign || 0,

      attackRate:
        result?.attack_rate || 0,

      attackTypes:
        result?.attack_types || {},

      results:
        result?.results || [],

      fullResult:
        result,
    };

    const updated = [
      entry,
      ...history,
    ].slice(0, 50);

    localStorage.setItem(
      HISTORY_KEY,
      JSON.stringify(updated)
    );

    return updated;
  } catch (error) {
    console.error(
      "Failed to save analysis history:",
      error
    );

    return getHistory();
  }
}


export function deleteHistoryItem(id) {
  const history = getHistory();

  const updated =
    history.filter(
      (item) => item.id !== id
    );

  localStorage.setItem(
    HISTORY_KEY,
    JSON.stringify(updated)
  );

  return updated;
}


export function clearHistory() {
  localStorage.removeItem(
    HISTORY_KEY
  );

  return [];
}