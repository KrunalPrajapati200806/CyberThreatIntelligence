import * as XLSX from "xlsx";

const SUPPORTED_EXTENSIONS = [
  ".csv",
  ".tsv",
  ".xls",
  ".xlsx",
  ".txt",
  ".json",
];

export function getFileExtension(filename) {
  const name = filename.toLowerCase();

  const index = name.lastIndexOf(".");

  if (index === -1) {
    return "";
  }

  return name.slice(index);
}

export function isSupportedFile(file) {
  if (!file) {
    return false;
  }

  const extension = getFileExtension(file.name);

  return SUPPORTED_EXTENSIONS.includes(extension);
}

export function getSupportedExtensions() {
  return [...SUPPORTED_EXTENSIONS];
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

export async function readTabularFile(file) {
  if (!file) {
    throw new Error("No file selected.");
  }

  if (!isSupportedFile(file)) {
    throw new Error(
      `Unsupported file format: ${getFileExtension(file.name) || "unknown"}`
    );
  }

  const extension = getFileExtension(file.name);

  // --------------------------------------------------
  // JSON
  // --------------------------------------------------

  if (extension === ".json") {
    const text = await file.text();

    try {
      const data = JSON.parse(text);

      return {
        type: "json",
        extension,
        name: file.name,
        data,
      };
    } catch {
      throw new Error(
        "The selected JSON file is invalid."
      );
    }
  }

  // --------------------------------------------------
  // CSV / TSV / TXT / XLS / XLSX
  // --------------------------------------------------

  const buffer = await file.arrayBuffer();

  const workbook = XLSX.read(buffer, {
    type: "array",
    cellDates: true,
  });

  if (!workbook.SheetNames.length) {
    throw new Error(
      "The uploaded file contains no worksheet."
    );
  }

  const firstSheet =
    workbook.Sheets[workbook.SheetNames[0]];

  const rows = XLSX.utils.sheet_to_json(
    firstSheet,
    {
      defval: null,
    }
  );

  return {
    type: "table",
    extension,
    name: file.name,
    sheetName: workbook.SheetNames[0],
    sheets: workbook.SheetNames,
    rows,
  };
}

export async function convertFileToCsv(file) {
  const parsed = await readTabularFile(file);

  if (parsed.type === "json") {
    const data = Array.isArray(parsed.data)
      ? parsed.data
      : [parsed.data];

    if (!data.length) {
      return "";
    }

    const worksheet =
      XLSX.utils.json_to_sheet(data);

    return XLSX.utils.sheet_to_csv(worksheet);
  }

  const worksheet =
    XLSX.utils.json_to_sheet(parsed.rows);

  return XLSX.utils.sheet_to_csv(worksheet);
}