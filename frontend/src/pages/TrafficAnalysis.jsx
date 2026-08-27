import {
  BarChart3,
  Activity,
  ArrowRight,
} from "lucide-react";

import UploadPanel from "../components/UploadPanel";
import ThreatDistribution from "../components/ThreatDistribution";
import Topbar from "../components/Topbar";


export default function TrafficAnalysis({
  result,
  apiOnline,
  file,
  setFile,
  setResult,
}) {

  return (
    <>
      <Topbar
        eyebrow="OPERATIONS"
        title="Traffic Analysis"
        description="Upload network traffic and run multiclass threat detection."
        apiOnline={apiOnline}
      />


      <section className="traffic-layout">

        {/* UPLOAD */}

        <UploadPanel
          file={file}
          setFile={setFile}
          setResult={setResult}
          apiOnline={apiOnline}
        />


        {/* INFORMATION */}

        <div className="panel analysis-guide">

          <div className="panel-heading">

            <div>

              <div className="section-kicker">
                ANALYSIS PIPELINE
              </div>

              <h3>
                How analysis works
              </h3>

            </div>

            <Activity size={22} />

          </div>


          <div className="pipeline-list">

            <div className="pipeline-item">

              <span className="pipeline-number">
                01
              </span>

              <div>
                <strong>
                  Upload traffic
                </strong>

                <p>
                  Select a CSV, TSV, Excel,
                  or JSON network traffic file.
                </p>
              </div>

            </div>


            <div className="pipeline-item">

              <span className="pipeline-number">
                02
              </span>

              <div>
                <strong>
                  Feature processing
                </strong>

                <p>
                  The backend normalizes the
                  network-flow features.
                </p>
              </div>

            </div>


            <div className="pipeline-item">

              <span className="pipeline-number">
                03
              </span>

              <div>
                <strong>
                  ML detection
                </strong>

                <p>
                  Random Forest classifies the
                  traffic into 15 threat classes.
                </p>
              </div>

            </div>


            <div className="pipeline-item">

              <span className="pipeline-number">
                04
              </span>

              <div>
                <strong>
                  Intelligence
                </strong>

                <p>
                  View attack statistics,
                  analytics and detailed results.
                </p>
              </div>

            </div>

          </div>

        </div>

      </section>


      {/* RESULTS */}

      {result && (

        <section className="panel">

          <div className="panel-heading">

            <div>

              <div className="section-kicker">
                ANALYSIS RESULT
              </div>

              <h3>
                Threat Distribution
              </h3>

            </div>

            <BarChart3 size={22} />

          </div>


          <ThreatDistribution
            attackTypes={
              result.attack_types
            }

            total={
              result.total_flows || 0
            }
          />

        </section>

      )}


      {/* NEXT STEPS */}

      {result && (

        <div className="analysis-next-actions">

          <button
            className="quick-action"
            onClick={() =>
              window.dispatchEvent(
                new CustomEvent(
                  "cyberintel:navigate",
                  {
                    detail:
                      "detection",
                  }
                )
              )
            }
          >

            <Activity size={18} />

            <span>
              View Detection Results
            </span>

            <ArrowRight size={17} />

          </button>


          <button
            className="quick-action"
            onClick={() =>
              window.dispatchEvent(
                new CustomEvent(
                  "cyberintel:navigate",
                  {
                    detail:
                      "analytics",
                  }
                )
              )
            }
          >

            <BarChart3 size={18} />

            <span>
              Open Analytics
            </span>

            <ArrowRight size={17} />

          </button>

        </div>

      )}

    </>
  );
}