// import { useRef, useState } from "react";

// import {
//   AlertTriangle,
//   FileUp,
//   Loader2,
//   Search,
//   UploadCloud,
//   X,
// } from "lucide-react";

// import { analyzeFile } from "../services/api";


// function UploadPanel({
//   file,
//   setFile,
//   setResult,
//   onAnalysis,
//   apiOnline,
// }) {

//   const inputRef = useRef(null);

//   const [dragging, setDragging] =
//     useState(false);

//   const [loading, setLoading] =
//     useState(false);

//   const [error, setError] =
//     useState("");


//   // --------------------------------------------------
//   // SELECT FILE
//   // --------------------------------------------------

//   const chooseFile = (selectedFiles) => {

//     const selected =
//       selectedFiles?.[0];

//     if (!selected) {
//       return;
//     }

//     const allowedExtensions = [
//       ".csv",
//       ".tsv",
//       ".xlsx",
//       ".xls",
//       ".json",
//     ];

//     const lowerName =
//       selected.name.toLowerCase();

//     const supported =
//       allowedExtensions.some(
//         (extension) =>
//           lowerName.endsWith(extension)
//       );

//     if (!supported) {

//       setError(
//         "Unsupported file. Please upload CSV, TSV, Excel, or JSON."
//       );

//       setFile(null);

//       return;
//     }

//     setError("");

//     setResult(null);

//     setFile(selected);
//   };


//   // --------------------------------------------------
//   // DROP
//   // --------------------------------------------------

//   const onDrop = (event) => {

//     event.preventDefault();

//     setDragging(false);

//     chooseFile(
//       event.dataTransfer.files
//     );
//   };


//   // --------------------------------------------------
//   // ANALYZE
//   // --------------------------------------------------

//   const analyze = async () => {

//     if (!file) {

//       setError(
//         "Please select a network traffic file first."
//       );

//       return;
//     }

//     if (!apiOnline) {

//       setError(
//         "FastAPI backend is offline."
//       );

//       return;
//     }

//     setLoading(true);

//     setError("");

//     try {

//       const data =
//         await analyzeFile(file);

//       setResult(data);
//       if (onAnalysis) {
//         onAnalysis(data, file);
//       }

//     } catch (err) {

//       setError(
//         err.message ||
//         "Traffic analysis failed."
//       );

//     } finally {

//       setLoading(false);

//     }
//   };


//   // --------------------------------------------------
//   // CLEAR
//   // --------------------------------------------------

//   const clearFile = () => {

//     setFile(null);

//     setResult(null);

//     setError("");

//     if (inputRef.current) {
//       inputRef.current.value = "";
//     }
//   };


//   return (

//     <div className="panel upload-panel">

//       <div className="panel-heading">

//         <div>

//           <div className="section-kicker">
//             TRAFFIC ANALYSIS
//           </div>

//           <h3>
//             Upload Network Traffic
//           </h3>

//         </div>

//         <UploadCloud size={22} />

//       </div>


//       {/* DROPZONE */}

//       <div
//         className={`dropzone ${
//           dragging
//             ? "dragging"
//             : ""
//         } ${
//           file
//             ? "has-file"
//             : ""
//         }`}

//         onDragOver={(event) => {

//           event.preventDefault();

//           setDragging(true);

//         }}

//         onDragLeave={() =>
//           setDragging(false)
//         }

//         onDrop={onDrop}

//         onClick={() =>
//           inputRef.current?.click()
//         }
//       >

//         <input
//           ref={inputRef}
//           type="file"
//           hidden
//           accept=".csv,.tsv,.xlsx,.xls,.json,text/csv,application/json"
//           onChange={(event) =>
//             chooseFile(
//               event.target.files
//             )
//           }
//         />


//         {file ? (

//           <>

//             <div className="file-icon">

//               <FileUp size={28} />

//             </div>


//             <strong>
//               {file.name}
//             </strong>


//             <span>

//               {(
//                 file.size /
//                 1024 /
//                 1024
//               ).toFixed(2)}

//               {" MB · Ready for analysis"}

//             </span>


//             <button
//               className="remove-file"

//               onClick={(event) => {

//                 event.stopPropagation();

//                 clearFile();

//               }}
//             >

//               <X size={14} />

//               Remove

//             </button>

//           </>

//         ) : (

//           <>

//             <div className="upload-icon">

//               <UploadCloud size={30} />

//             </div>


//             <strong>
//               Drop your network file here
//             </strong>


//             <span>
//               or click to browse
//             </span>


//             <button
//               className="browse-button"

//               onClick={(event) => {

//                 event.stopPropagation();

//                 inputRef.current?.click();

//               }}
//             >

//               Choose File

//             </button>


//             <small>

//               CSV · TSV · XLSX · XLS · JSON

//             </small>

//           </>

//         )}

//       </div>


//       {/* ERROR */}

//       {error && (

//         <div className="error-box">

//           <AlertTriangle size={17} />

//           <span>
//             {error}
//           </span>

//         </div>

//       )}


//       {/* ACTIONS */}

//       <div className="analysis-actions">

//         <button
//           className="primary-button"

//           onClick={analyze}

//           disabled={
//             !file ||
//             loading ||
//             !apiOnline
//           }
//         >

//           {loading ? (

//             <>

//               <Loader2
//                 size={18}
//                 className="spin"
//               />

//               Analyzing...

//             </>

//           ) : (

//             <>

//               <Search size={18} />

//               Analyze Traffic

//             </>

//           )}

//         </button>


//         <button
//           className="secondary-button"

//           onClick={clearFile}

//           disabled={loading}
//         >

//           Clear

//         </button>

//       </div>


//       {!apiOnline && (

//         <div className="warning-text">

//           Start FastAPI on{" "}

//           <code>
//             127.0.0.1:8000
//           </code>

//         </div>

//       )}

//     </div>
//   );
// }


// export default UploadPanel;

































































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

  const [modelType, setModelType] =
    useState("multiclass");


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
        await analyzeFile(
          file,
          modelType
        );

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


      {/* DETECTION MODE */}

                              {/* <div className="detection-mode">

                                <div className="mode-label">
                                  Detection Mode
                                </div>

                                <div className="mode-options">

                                  <label
                                    className={`mode-option ${
                                      modelType === "multiclass"
                                        ? "active"
                                        : ""
                                    }`}
                                  >

                                    <input
                                      type="radio"
                                      name="modelType"
                                      value="multiclass"
                                      checked={
                                        modelType === "multiclass"
                                      }
                                      onChange={() =>
                                        setModelType("multiclass")
                                      }
                                    />

                                    <div>

                                      <strong>
                                        Multiclass Classification
                                      </strong>

                                      <span>
                                        Identify the specific attack type
                                      </span>

                                    </div>

                                  </label>


                                  <label
                                    className={`mode-option ${
                                      modelType === "binary"
                                        ? "active"
                                        : ""
                                    }`}
                                  >

                                    <input
                                      type="radio"
                                      name="modelType"
                                      value="binary"
                                      checked={
                                        modelType === "binary"
                                      }
                                      onChange={() =>
                                        setModelType("binary")
                                      }
                                    />

                                    <div>

                                      <strong>
                                        Binary Detection
                                      </strong>

                                      <span>
                                        Detect benign or malicious traffic
                                      </span>

                                    </div>

                                  </label>

                                </div>

                              </div> */}

      {/* DETECTION MODE */}

      <div className="detection-mode">

        <div className="mode-header">
          <div>
            <div className="mode-label">
              Detection Mode
            </div>

            <div className="mode-description">
              Choose how the traffic intelligence engine should classify your data.
            </div>
          </div>

          <div className="mode-status">
            <span className="mode-status-dot" />
            {modelType === "multiclass"
              ? "Threat Classification"
              : "Threat Detection"}
          </div>
        </div>


        <div
          className="mode-options"
          role="radiogroup"
          aria-label="Detection Mode"
        >

          {/* MULTICLASS */}

          <label
            className={`mode-option ${
              modelType === "multiclass"
                ? "active"
                : ""
            }`}
          >

            <input
              type="radio"
              name="modelType"
              value="multiclass"
              checked={modelType === "multiclass"}
              onChange={() =>
                setModelType("multiclass")
              }
            />

            <div className="mode-icon multiclass-icon">
              <span />
              <span />
              <span />
            </div>

            <div className="mode-content">

              <div className="mode-title-row">

                <strong>
                  Multiclass Classification
                </strong>

                {modelType === "multiclass" && (
                  <span className="selected-badge">
                    ACTIVE
                  </span>
                )}

              </div>

              <span>
                Identify the specific attack type
              </span>

            </div>

            <div className="mode-radio-indicator">
              <div />
            </div>

          </label>


          {/* BINARY */}

          <label
            className={`mode-option ${
              modelType === "binary"
                ? "active"
                : ""
            }`}
          >

            <input
              type="radio"
              name="modelType"
              value="binary"
              checked={modelType === "binary"}
              onChange={() =>
                setModelType("binary")
              }
            />

            <div className="mode-icon binary-icon">
              <span />
              <span />
            </div>

            <div className="mode-content">

              <div className="mode-title-row">

                <strong>
                  Binary Detection
                </strong>

                {modelType === "binary" && (
                  <span className="selected-badge">
                    ACTIVE
                  </span>
                )}

              </div>

              <span>
                Detect benign or malicious traffic
              </span>

            </div>

            <div className="mode-radio-indicator">
              <div />
            </div>

          </label>

        </div>

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
