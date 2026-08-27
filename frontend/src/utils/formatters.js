export function formatNumber(value) {
  if (value === null || value === undefined) {
    return "0";
  }

  return Number(value).toLocaleString();
}

export function formatPercentage(value) {
  if (value === null || value === undefined) {
    return "0.00%";
  }

  return `${Number(value).toFixed(2)}%`;
}

export function formatFileSize(bytes) {
  if (!bytes) {
    return "0 B";
  }

  const units = ["B", "KB", "MB", "GB", "TB"];

  const index = Math.floor(
    Math.log(bytes) / Math.log(1024)
  );

  return `${(
    bytes / Math.pow(1024, index)
  ).toFixed(index === 0 ? 0 : 2)} ${units[index]}`;
}

export function getConfidenceLevel(value) {
  const percentage = Number(value) * 100;

  if (percentage >= 90) {
    return "VERY HIGH";
  }

  if (percentage >= 75) {
    return "HIGH";
  }

  if (percentage >= 50) {
    return "MEDIUM";
  }

  return "LOW";
}

export function getFileExtension(filename = "") {
  const parts = filename.split(".");

  if (parts.length < 2) {
    return "";
  }

  return `.${parts.pop().toLowerCase()}`;
}