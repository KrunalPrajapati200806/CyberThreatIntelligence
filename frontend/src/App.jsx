import {
  useEffect,
  useRef,
  useState,
} from "react";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import TrafficAnalysis from "./pages/TrafficAnalysis";
import ThreatDetection from "./pages/ThreatDetection";
import Reports from "./pages/Reports";
import Analytics from "./pages/Analytics";
import History from "./pages/History";

import { checkHealth } from "./services/api";

import {
  saveAnalysis,
  getAllAnalyses,
  getAnalysis,
  deleteAnalysis,
  clearAnalyses,
} from "./services/historyDb";

import "./App.css";


function createHistoryEntry(
  result,
  file
) {
  return {
    id:
      `${Date.now()}-${Math.random()
        .toString(36)
        .slice(2)}`,

    fileName:
      file?.name ||
      result?.file_name ||
      "Unknown file",

    timestamp:
      new Date().toISOString(),

    total_flows:
      Number(result?.total_flows) || 0,

    attacks:
      Number(result?.attacks) || 0,

    benign:
      Number(result?.benign) || 0,

    attack_rate:
      Number(result?.attack_rate) || 0,

    attack_types:
      result?.attack_types || {},

    model:
      result?.model ||
      "random_forest_multiclass",

    features:
      result?.features ||
      36,

    classes:
      result?.classes ||
      15,

    /*
     * IMPORTANT:
     * The complete prediction result is stored
     * in IndexedDB, NOT localStorage.
     */
    result,
  };
}


function App() {

  const [activeNav, setActiveNav] =
    useState("dashboard");

  const [apiOnline, setApiOnline] =
    useState(false);

  const [result, setResult] =
    useState(null);

  const [file, setFile] =
    useState(null);

  const [history, setHistory] =
    useState([]);

  const [collapsed, setCollapsed] =
    useState(false);


  /*
   * Ref gives us the latest file immediately.
   * React state is intentionally asynchronous.
   */
  const fileRef =
    useRef(null);


  // --------------------------------------------------
  // FILE
  // --------------------------------------------------

  const updateFile = (nextFile) => {
    fileRef.current =
      nextFile;

    setFile(nextFile);
  };


  // --------------------------------------------------
  // LOAD HISTORY
  // --------------------------------------------------

  const loadHistory = async () => {

    try {

      const records =
        await getAllAnalyses();

      setHistory(records);

    } catch (error) {

      console.error(
        "Could not load analysis history:",
        error
      );

      setHistory([]);

    }

  };


  useEffect(() => {

    loadHistory();

  }, []);


  // --------------------------------------------------
  // API HEALTH
  // --------------------------------------------------

  const checkAPI = async () => {

    try {

      const response =
        await checkHealth();

      setApiOnline(
        response?.status ===
        "healthy"
      );

    } catch {

      setApiOnline(false);

    }

  };


  useEffect(() => {

    checkAPI();

    const timer =
      setInterval(
        checkAPI,
        10000
      );

    return () =>
      clearInterval(timer);

  }, []);


  // --------------------------------------------------
  // ANALYSIS RESULT
  // --------------------------------------------------

  const handleResult = async (
    nextResult
  ) => {

    if (!nextResult) {

      setResult(null);

      return;

    }


    setResult(nextResult);


    const entry =
      createHistoryEntry(
        nextResult,
        fileRef.current
      );


    try {

      await saveAnalysis(
        entry
      );

      await loadHistory();

    } catch (error) {

      console.error(
        "Could not save analysis:",
        error
      );

    }

  };


  // --------------------------------------------------
  // NAVIGATION
  // --------------------------------------------------

  useEffect(() => {

    const handleNavigation =
      (event) => {

        if (event.detail) {

          setActiveNav(
            event.detail
          );

        }

      };


    window.addEventListener(
      "cyberintel:navigate",
      handleNavigation
    );


    return () => {

      window.removeEventListener(
        "cyberintel:navigate",
        handleNavigation
      );

    };

  }, []);


  // --------------------------------------------------
  // OPEN HISTORY
  // --------------------------------------------------

  const openHistoryItem =
    async (item) => {

      try {

        const record =
          await getAnalysis(
            item.id
          );


        if (!record) {

          console.warn(
            "Analysis not found:",
            item.id
          );

          return;

        }


        /*
         * Restore the COMPLETE analysis.
         */
        setResult(
          record.result
        );


        setFile({
          name:
            record.fileName,

          size:
            0,
        });


        fileRef.current = {
          name:
            record.fileName,

          size:
            0,
        };


        setActiveNav(
          "detection"
        );

      } catch (error) {

        console.error(
          "Could not open analysis:",
          error
        );

      }

    };


  // --------------------------------------------------
  // DELETE ONE HISTORY ITEM
  // --------------------------------------------------

  const removeHistoryItem =
    async (id) => {

      try {

        await deleteAnalysis(
          id
        );

        await loadHistory();

      } catch (error) {

        console.error(
          "Could not delete analysis:",
          error
        );

      }

    };


  // --------------------------------------------------
  // CLEAR HISTORY
  // --------------------------------------------------

  const handleClearHistory =
    async () => {

      try {

        await clearAnalyses();

        setHistory([]);

      } catch (error) {

        console.error(
          "Could not clear history:",
          error
        );

      }

    };


  // --------------------------------------------------
  // EXPORT
  // --------------------------------------------------

  const handleExport = () => {

    if (!result) {

      return;

    }


    const blob =
      new Blob(
        [
          JSON.stringify(
            result,
            null,
            2
          ),
        ],
        {
          type:
            "application/json",
        }
      );


    const url =
      URL.createObjectURL(
        blob
      );


    const link =
      document.createElement(
        "a"
      );


    link.href =
      url;

    link.download =
      "cyberintel-analysis.json";

    link.click();


    URL.revokeObjectURL(
      url
    );

  };


  // --------------------------------------------------
  // PAGE
  // --------------------------------------------------

  const renderPage = () => {

    switch (
      activeNav
    ) {

      case "dashboard":

        return (
          <Dashboard
            result={result}
            apiOnline={apiOnline}
            checkHealth={checkAPI}
            onAnalysis={() =>
              setActiveNav(
                "traffic"
              )
            }
          />
        );


      case "traffic":

        return (
          <TrafficAnalysis
            result={result}
            apiOnline={apiOnline}
            file={file}
            setFile={updateFile}
            setResult={handleResult}
          />
        );


      case "detection":

        return (
          <ThreatDetection
            result={result}
            onExport={
              handleExport
            }
          />
        );


      case "analytics":

        return (
          <Analytics
            result={result}
          />
        );


      case "reports":

        return (
          <Reports
            result={result}
          
          />
        );


      case "history":

        return (
          <History
            history={history}
            onSelect={
              openHistoryItem
            }
            onDelete={
              removeHistoryItem
            }
            onClear={
              handleClearHistory
            }
          />
        );


      default:

        return (
          <Dashboard
            result={result}
            apiOnline={apiOnline}
            checkHealth={checkAPI}
            onAnalysis={() =>
              setActiveNav(
                "traffic"
              )
            }
          />
        );

    }

  };


  return (

    <div
      className={`app-shell ${
        collapsed
          ? "sidebar-collapsed"
          : ""
      }`}
    >

      <Sidebar
        activeNav={
          activeNav
        }

        setActiveNav={
          setActiveNav
        }

        apiOnline={
          apiOnline
        }

        collapsed={
          collapsed
        }

        setCollapsed={
          setCollapsed
        }
      />


      <main className="main-content">

        {renderPage()}


        <footer className="footer">

          <span>
            CyberIntel · Network Attack
            Intelligence Platform
          </span>

          <span>
            Random Forest · 36 Features ·
            15 Classes
          </span>

        </footer>

      </main>

    </div>

  );

}


export default App;