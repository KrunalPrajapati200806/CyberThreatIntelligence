import {
  Activity,
  AlertTriangle,
  BarChart3,
  Gauge,
  ShieldCheck,
  RefreshCw,
  ArrowRight,
} from "lucide-react";

import StatCard from "../components/StatCard";
import ThreatDistribution from "../components/ThreatDistribution";
import Topbar from "../components/Topbar";


function Dashboard({
  result,
  apiOnline,
  checkHealth,
  onAnalysis,
}) {

  return (
    <>
      <Topbar
        eyebrow="SECURITY OPERATIONS CENTER"
        title="Network Threat Dashboard"
        description="Monitor the latest network security analysis and threat activity."
        actions={
          <>
            <div
              className={`api-badge ${
                apiOnline
                  ? "online"
                  : "offline"
              }`}
            >
              <span className="status-dot" />

              API{" "}
              {apiOnline
                ? "ONLINE"
                : "OFFLINE"}
            </div>


            <button
              className="icon-button"
              onClick={checkHealth}
              title="Refresh API status"
            >
              <RefreshCw
                size={18}
              />
            </button>
          </>
        }
      />


      <section className="stats-grid">

        <StatCard
          icon={Activity}
          label="TOTAL FLOWS"
          value={
            result?.total_flows ?? 0
          }
          hint="Network flows analyzed"
        />


        <StatCard
          icon={AlertTriangle}
          label="THREATS DETECTED"
          value={
            result?.attacks ?? 0
          }
          hint="Malicious activity"
          tone="red"
        />


        <StatCard
          icon={ShieldCheck}
          label="BENIGN TRAFFIC"
          value={
            result?.benign ?? 0
          }
          hint="Normal traffic"
          tone="green"
        />


        <StatCard
          icon={Gauge}
          label="ATTACK RATE"
          value={`${result?.attack_rate ?? 0}%`}
          hint="Malicious flow percentage"
          tone="purple"
        />

      </section>


      <section className="dashboard-grid">

        <div className="panel">

          <div className="panel-heading">

            <div>

              <div className="section-kicker">
                THREAT INTELLIGENCE
              </div>

              <h3>
                Current Threat Distribution
              </h3>

            </div>

            <BarChart3
              size={22}
            />

          </div>


          <ThreatDistribution
            attackTypes={
              result?.attack_types
            }
            total={
              result?.total_flows || 0
            }
          />

        </div>


        <div className="panel dashboard-status-panel">

          <div className="panel-heading">

            <div>

              <div className="section-kicker">
                ANALYSIS STATUS
              </div>

              <h3>
                Latest Analysis
              </h3>

            </div>

            <Activity
              size={22}
            />

          </div>


          {!result ? (

            <div className="dashboard-empty">

              <strong>
                No analysis loaded
              </strong>

              <span>
                Go to Traffic Analysis
                to analyze a network
                traffic file.
              </span>

            </div>

          ) : (

            <div className="latest-analysis">

              <div className="latest-number">

                <strong>
                  {result.total_flows?.toLocaleString()}
                </strong>

                <span>
                  flows analyzed
                </span>

              </div>


              <div className="latest-row">

                <span>
                  Threats
                </span>

                <strong className="danger-text">
                  {result.attacks?.toLocaleString()}
                </strong>

              </div>


              <div className="latest-row">

                <span>
                  Benign
                </span>

                <strong className="success-text">
                  {result.benign?.toLocaleString()}
                </strong>

              </div>


              <div className="latest-row">

                <span>
                  Attack rate
                </span>

                <strong>
                  {result.attack_rate}%
                </strong>

              </div>

            </div>

          )}

        </div>

      </section>


      <section className="dashboard-quick-actions">

        <button
          className="quick-action"
          onClick={() =>
            window.dispatchEvent(
              new CustomEvent(
                "cyberintel:navigate",
                {
                  detail: "traffic",
                }
              )
            )
          }
        >

          <Activity size={18} />

          <span>
            Analyze Traffic
          </span>

          <ArrowRight
            size={17}
          />

        </button>


        <button
          className="quick-action"
          onClick={() =>
            window.dispatchEvent(
              new CustomEvent(
                "cyberintel:navigate",
                {
                  detail: "analytics",
                }
              )
            )
          }
        >

          <BarChart3
            size={18}
          />

          <span>
            Open Analytics
          </span>

          <ArrowRight
            size={17}
          />

        </button>


        <button
          className="quick-action"
          onClick={() =>
            window.dispatchEvent(
              new CustomEvent(
                "cyberintel:navigate",
                {
                  detail: "history",
                }
              )
            )
          }
        >

          <Activity size={18} />

          <span>
            View History
          </span>

          <ArrowRight
            size={17}
          />

        </button>

      </section>

    </>
  );
}


export default Dashboard;