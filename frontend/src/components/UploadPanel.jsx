import { useRef, useState } from "react";

import {
  AlertTriangle,
  FileUp,
  Loader2,
  Search,
  UploadCloud,
  X,
} from "lucide-react";

import { analyzeFile } from "../services/api";


function UploadPanel({
  file,
  setFile,
  setResult,
  onAnalysis,
  apiOnline,
}) {

  const inputRef = useRef(null);

  const [dragging, setDragging] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  // --------------------------------------------------
  // SELECT FILE
  // --------------------------------------------------

  const chooseFile = (selectedFiles) => {

    const selected =
      selectedFiles?.[0];

    if (!selected) {
      return;
    }

    const allowedExtensions = [
      ".csv",
      ".tsv",
      ".xlsx",
      ".xls",
      ".json",
    ];

    const lowerName =
      selected.name.toLowerCase();

    const supported =
      allowedExtensions.some(
        (extension) =>
          lowerName.endsWith(extension)
      );

    if (!supported) {

      setError(
        "Unsupported file. Please upload CSV, TSV, Excel, or JSON."
      );

      setFile(null);

      return;
    }

    setError("");

    setResult(null);

    setFile(selected);
  };


  // --------------------------------------------------
  // DROP
  // --------------------------------------------------

  const onDrop = (event) => {

    event.preventDefault();

    setDragging(false);

    chooseFile(
      event.dataTransfer.files
    );
  };


  // --------------------------------------------------
  // ANALYZE
  // --------------------------------------------------

  const analyze = async () => {

    if (!file) {

      setError(
        "Please select a network traffic file first."
      );

      return;
    }

    if (!apiOnline) {

      setError(
        "FastAPI backend is offline."
      );

      return;
    }

    setLoading(true);

    setError("");

    try {

      const data =
        await analyzeFile(file);

      setResult(data);
      if (onAnalysis) {
        onAnalysis(data, file);
      }

    } catch (err) {

      setError(
        err.message ||
        "Traffic analysis failed."
      );

    } finally {

      setLoading(false);

    }
  };


  // --------------------------------------------------
  // CLEAR
  // --------------------------------------------------

  const clearFile = () => {

    setFile(null);

    setResult(null);

    setError("");

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };


  return (

    <div className="panel upload-panel">

      <div className="panel-heading">

        <div>

          <div className="section-kicker">
            TRAFFIC ANALYSIS
          </div>

          <h3>
            Upload Network Traffic
          </h3>

        </div>

        <UploadCloud size={22} />

      </div>


      {/* DROPZONE */}

      <div
        className={`dropzone ${
          dragging
            ? "dragging"
            : ""
        } ${
          file
            ? "has-file"
            : ""
        }`}

        onDragOver={(event) => {

          event.preventDefault();

          setDragging(true);

        }}

        onDragLeave={() =>
          setDragging(false)
        }

        onDrop={onDrop}

        onClick={() =>
          inputRef.current?.click()
        }
      >

        <input
          ref={inputRef}
          type="file"
          hidden
          accept=".csv,.tsv,.xlsx,.xls,.json,text/csv,application/json"
          onChange={(event) =>
            chooseFile(
              event.target.files
            )
          }
        />


        {file ? (

          <>

            <div className="file-icon">

              <FileUp size={28} />

            </div>


            <strong>
              {file.name}
            </strong>


            <span>

              {(
                file.size /
                1024 /
                1024
              ).toFixed(2)}

              {" MB · Ready for analysis"}

            </span>


            <button
              className="remove-file"

              onClick={(event) => {

                event.stopPropagation();

                clearFile();

              }}
            >

              <X size={14} />

              Remove

            </button>

          </>

        ) : (

          <>

            <div className="upload-icon">

              <UploadCloud size={30} />

            </div>


            <strong>
              Drop your network file here
            </strong>


            <span>
              or click to browse
            </span>


            <button
              className="browse-button"

              onClick={(event) => {

                event.stopPropagation();

                inputRef.current?.click();

              }}
            >

              Choose File

            </button>


            <small>

              CSV · TSV · XLSX · XLS · JSON

            </small>

          </>

        )}

      </div>


      {/* ERROR */}

      {error && (

        <div className="error-box">

          <AlertTriangle size={17} />

          <span>
            {error}
          </span>

        </div>

      )}


      {/* ACTIONS */}

      <div className="analysis-actions">

        <button
          className="primary-button"

          onClick={analyze}

          disabled={
            !file ||
            loading ||
            !apiOnline
          }
        >

          {loading ? (

            <>

              <Loader2
                size={18}
                className="spin"
              />

              Analyzing...

            </>

          ) : (

            <>

              <Search size={18} />

              Analyze Traffic

            </>

          )}

        </button>


        <button
          className="secondary-button"

          onClick={clearFile}

          disabled={loading}
        >

          Clear

        </button>

      </div>


      {!apiOnline && (

        <div className="warning-text">

          Start FastAPI on{" "}

          <code>
            127.0.0.1:8000
          </code>

        </div>

      )}

    </div>
  );
}


export default UploadPanel;