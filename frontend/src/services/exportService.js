import * as XLSX from "xlsx";

function downloadBlob(
  blob,
  filename
) {
  const url =
    URL.createObjectURL(blob);

  const link =
    document.createElement("a");

  link.href = url;
  link.download = filename;

  document.body.appendChild(link);

  link.click();

  link.remove();

  URL.revokeObjectURL(url);
}

function downloadText(
  content,
  filename,
  mimeType
) {
  const blob = new Blob(
    [content],
    {
      type: mimeType,
    }
  );

  downloadBlob(
    blob,
    filename
  );
}

// --------------------------------------------------
// JSON
// --------------------------------------------------

export function exportJSON(
  data,
  filename = "cyberintel-report.json"
) {
  const content =
    JSON.stringify(
      data,
      null,
      2
    );

  downloadText(
    content,
    filename,
    "application/json"
  );
}

// --------------------------------------------------
// CSV
// --------------------------------------------------

export function exportCSV(
  rows,
  filename = "cyberintel-results.csv"
) {
  const worksheet =
    XLSX.utils.json_to_sheet(
      rows
    );

  const csv =
    XLSX.utils.sheet_to_csv(
      worksheet
    );

  downloadText(
    csv,
    filename,
    "text/csv;charset=utf-8"
  );
}

// --------------------------------------------------
// XLSX
// --------------------------------------------------

export function exportXLSX(
  rows,
  filename = "cyberintel-results.xlsx"
) {
  const worksheet =
    XLSX.utils.json_to_sheet(
      rows
    );

  const workbook =
    XLSX.utils.book_new();

  XLSX.utils.book_append_sheet(
    workbook,
    worksheet,
    "Results"
  );

  XLSX.writeFile(
    workbook,
    filename
  );
}

// --------------------------------------------------
// TXT
// --------------------------------------------------

export function exportTXT(
  data,
  filename = "cyberintel-report.txt"
) {
  const content =
    typeof data === "string"
      ? data
      : JSON.stringify(
          data,
          null,
          2
        );

  downloadText(
    content,
    filename,
    "text/plain;charset=utf-8"
  );
}

// --------------------------------------------------
// Generic exporter
// --------------------------------------------------

export function exportReport(
  result,
  format
) {
  if (!result) {
    throw new Error(
      "No analysis result available."
    );
  }

  const rows =
    result.results || [];

  switch (
    format.toLowerCase()
  ) {
    case "json":
      exportJSON(result);
      break;

    case "csv":
      exportCSV(rows);
      break;

    case "xlsx":
      exportXLSX(rows);
      break;

    case "txt":
      exportTXT(result);
      break;

    default:
      throw new Error(
        `Unsupported export format: ${format}`
      );
  }
}