import { useEffect, useRef, useState } from "react";
import {
  Download,
  FileJson,
  FileSpreadsheet,
  FileText,
  ChevronDown,
} from "lucide-react";

function ExportMenu({
  onExportJSON,
  onExportCSV,
  onExportXLSX,
  onExportTXT,
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handleClick = (event) => {
      if (
        ref.current &&
        !ref.current.contains(event.target)
      ) {
        setOpen(false);
      }
    };

    document.addEventListener(
      "mousedown",
      handleClick
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClick
      );
    };
  }, []);

  const exportFile = (handler) => {
    setOpen(false);

    if (handler) {
      handler();
    }
  };

  return (
    <div
      className="export-menu"
      ref={ref}
    >
      <button
        className="export-button"
        onClick={() =>
          setOpen((value) => !value)
        }
      >
        <Download size={16} />

        <span>Export</span>

        <ChevronDown
          size={15}
          className={
            open
              ? "export-chevron-open"
              : ""
          }
        />
      </button>

      {open && (
        <div className="export-dropdown">

          <button
            onClick={() =>
              exportFile(onExportJSON)
            }
          >
            <FileJson size={16} />
            JSON
          </button>

          <button
            onClick={() =>
              exportFile(onExportCSV)
            }
          >
            <FileText size={16} />
            CSV
          </button>

          <button
            onClick={() =>
              exportFile(onExportXLSX)
            }
          >
            <FileSpreadsheet size={16} />
            XLSX
          </button>

          <button
            onClick={() =>
              exportFile(onExportTXT)
            }
          >
            <FileText size={16} />
            TXT
          </button>

        </div>
      )}
    </div>
  );
}

export default ExportMenu;