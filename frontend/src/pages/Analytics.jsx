import React from "react";
import {
  BarChart3,
  PieChart,
  Activity,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
  Target,
} from "lucide-react";

function Analytics({ result }) {
  /*
   * ============================================================
   * NORMALIZE RESULT DATA
   * ============================================================
   */

  const data = result || {};

  const totalFlows = Number(
    data.total_flows ??
      data.totalFlows ??
      data.total ??
      0
  );

  const threats = Number(
    data.attacks ??
      data.threats ??
      data.threat_count ??
      0
  );

  const benign = Number(
    data.benign ??
      data.benign_count ??
      Math.max(totalFlows - threats, 0)
  );

  const attackRate =
    totalFlows > 0
      ? (threats / totalFlows) * 100
      : Number(data.attack_rate ?? 0);

  /*
   * ============================================================
   * ATTACK TYPES
   * ============================================================
   */

  const attackTypes =
    data.attack_types ||
    data.attackTypes ||
    data.classes ||
    {};

  const entries = Object.entries(attackTypes)
    .map(([name, value]) => ({
      name,
      count: Number(value) || 0,
    }))
    .filter((item) => item.count > 0)
    .sort((a, b) => b.count - a.count);

  /*
   * Only show useful attack classes.
   *
   * We use LOGARITHMIC VISUAL SCALING for the graph.
   * This is important because PortScan can be 99%+
   * of the attacks and would otherwise hide every
   * smaller class.
   */

  const topClasses = entries.slice(0, 8);

  const maxLog =
    topClasses.length > 0
      ? Math.max(
          ...topClasses.map((item) =>
            Math.log10(item.count + 1)
          )
        )
      : 1;

  /*
   * ============================================================
   * DONUT
   * ============================================================
   */

  const benignPercent =
    totalFlows > 0
      ? (benign / totalFlows) * 100
      : 0;

  const threatPercent =
    totalFlows > 0
      ? (threats / totalFlows) * 100
      : 0;

  /*
   * ============================================================
   * HELPERS
   * ============================================================
   */

  const formatNumber = (value) =>
    Number(value || 0).toLocaleString();

  const formatPercent = (value) =>
    Number(value || 0).toFixed(2);

  /*
   * ============================================================
   * EMPTY STATE
   * ============================================================
   */

  if (!totalFlows && !entries.length) {
    return (
      <div className="analytics-v2-page">
        <div className="analytics-v2-header">
          <div>
            <span className="analytics-v2-eyebrow">
              SECURITY ANALYTICS
            </span>

            <h1>Network Analytics</h1>

            <p>
              Visual intelligence from the latest
              network traffic analysis.
            </p>
          </div>
        </div>

        <div className="analytics-v2-empty">
          <BarChart3 size={42} />

          <h2>No analysis data available</h2>

          <p>
            Analyze a network traffic CSV to populate
            the analytics dashboard.
          </p>
        </div>
      </div>
    );
  }

  /*
   * ============================================================
   * MAIN UI
   * ============================================================
   */

  return (
    <div className="analytics-v2-page">

      {/* ======================================================
          HEADER
         ====================================================== */}

      <div className="analytics-v2-header">
        <div>
          <span className="analytics-v2-eyebrow">
            SECURITY ANALYTICS
          </span>

          <h1>Network Analytics</h1>

          <p>
            Visual intelligence from the latest
            network traffic analysis.
          </p>
        </div>

        <div className="analytics-v2-status">
          <span />
          LIVE ANALYSIS
        </div>
      </div>


      {/* ======================================================
          SUMMARY CARDS
         ====================================================== */}

      <div className="analytics-v2-stats">

        <div className="analytics-v2-stat">
          <div className="analytics-v2-stat-icon cyan">
            <Activity size={19} />
          </div>

          <div>
            <span>TOTAL FLOWS</span>
            <strong>{formatNumber(totalFlows)}</strong>
            <small>Network traffic analyzed</small>
          </div>
        </div>


        <div className="analytics-v2-stat">
          <div className="analytics-v2-stat-icon red">
            <ShieldAlert size={19} />
          </div>

          <div>
            <span>THREATS DETECTED</span>
            <strong>{formatNumber(threats)}</strong>
            <small>Malicious flows detected</small>
          </div>
        </div>


        <div className="analytics-v2-stat">
          <div className="analytics-v2-stat-icon green">
            <ShieldCheck size={19} />
          </div>

          <div>
            <span>BENIGN TRAFFIC</span>
            <strong>{formatNumber(benign)}</strong>
            <small>Normal traffic classified</small>
          </div>
        </div>


        <div className="analytics-v2-stat">
          <div className="analytics-v2-stat-icon purple">
            <TrendingUp size={19} />
          </div>

          <div>
            <span>ATTACK RATE</span>
            <strong>{formatPercent(attackRate)}%</strong>
            <small>Malicious traffic percentage</small>
          </div>
        </div>

      </div>


      {/* ======================================================
          TOP CHARTS
         ====================================================== */}

      <div className="analytics-v2-top-grid">

        {/* ====================================================
            THREAT INTENSITY PROFILE
           ==================================================== */}

        <section className="analytics-v2-card analytics-v2-intensity-card">

          <div className="analytics-v2-card-header">

            <div>
              <span>THREAT LANDSCAPE</span>

              <h2>Threat Intensity Profile</h2>

              <p>
                Relative concentration of detected attack
                categories.
              </p>
            </div>

            <div className="analytics-v2-card-icon">
              <BarChart3 size={18} />
            </div>

          </div>


          <div className="analytics-v2-chart">

            {topClasses.length === 0 ? (

              <div className="analytics-v2-no-data">
                <BarChart3 size={34} />
                <strong>No attack classes</strong>
                <span>
                  Analyze traffic to populate this chart.
                </span>
              </div>

            ) : (

              <div className="analytics-v2-bars">

                {topClasses.map((item, index) => {

                  const logValue =
                    Math.log10(item.count + 1);

                  /*
                   * Log scaling keeps small attack classes
                   * visible even when PortScan dominates.
                   */

                  const height =
                    Math.max(
                      14,
                      (logValue / maxLog) * 100
                    );

                  const share =
                    threats > 0
                      ? (item.count / threats) * 100
                      : 0;

                  return (
                    <div
                      className="analytics-v2-bar-item"
                      key={item.name}
                    >

                      <div className="analytics-v2-bar-value">
                        {formatNumber(item.count)}
                      </div>

                      <div className="analytics-v2-bar-track">

                        <div
                          className="analytics-v2-bar-fill"
                          style={{
                            height: `${height}%`,
                          }}
                        >
                          <div className="analytics-v2-bar-glow" />
                        </div>

                      </div>

                      <div className="analytics-v2-bar-label">
                        {item.name}
                      </div>

                      <div className="analytics-v2-bar-share">
                        {share >= 0.01
                          ? `${share.toFixed(2)}%`
                          : "<0.01%"}
                      </div>

                    </div>
                  );
                })}

              </div>

            )}

          </div>


          <div className="analytics-v2-chart-footer">

            <span>
              Showing top {topClasses.length} detected
              classes
            </span>

            <span>
              {entries.length} total classes
            </span>

          </div>

        </section>


        {/* ====================================================
            BENIGN VS THREAT DONUT
           ==================================================== */}

        <section className="analytics-v2-card analytics-v2-composition-card">

          <div className="analytics-v2-card-header">

            <div>
              <span>TRAFFIC COMPOSITION</span>

              <h2>Benign vs Threat</h2>

              <p>
                Overall classification of analyzed flows.
              </p>
            </div>

            <div className="analytics-v2-card-icon">
              <PieChart size={18} />
            </div>

          </div>


          <div className="analytics-v2-donut-area">

            <div
              className="analytics-v2-donut"
              style={{
                background: `conic-gradient(
                  #ff416c 0 ${threatPercent}%,
                  #172a3d ${threatPercent}% 100%
                )`,
              }}
            >

              <div className="analytics-v2-donut-inner">

                <strong>
                  {formatPercent(attackRate)}%
                </strong>

                <span>THREAT RATE</span>

              </div>

            </div>


            <div className="analytics-v2-legend">

              <div className="analytics-v2-legend-row">

                <div>
                  <i className="green-dot" />
                  <span>Benign</span>
                </div>

                <strong>
                  {formatNumber(benign)}
                </strong>

              </div>


              <div className="analytics-v2-legend-row">

                <div>
                  <i className="red-dot" />
                  <span>Threats</span>
                </div>

                <strong>
                  {formatNumber(threats)}
                </strong>

              </div>


              <div className="analytics-v2-legend-row total">

                <div>
                  <span>Total flows</span>
                </div>

                <strong>
                  {formatNumber(totalFlows)}
                </strong>

              </div>

            </div>

          </div>


          <div className="analytics-v2-composition-footer">

            <div>
              <span>NORMAL TRAFFIC</span>
              <strong className="green-text">
                {formatPercent(benignPercent)}%
              </strong>
            </div>

            <div>
              <span>MALICIOUS TRAFFIC</span>
              <strong className="red-text">
                {formatPercent(threatPercent)}%
              </strong>
            </div>

          </div>

        </section>

      </div>


      {/* ======================================================
          BOTTOM SECTION
         ====================================================== */}

      <div className="analytics-v2-bottom-grid">


        {/* ====================================================
            ATTACK CLASS RANKING
           ==================================================== */}

        <section className="analytics-v2-card analytics-v2-ranking">

          <div className="analytics-v2-card-header">

            <div>
              <span>THREAT INTELLIGENCE</span>

              <h2>Attack Class Ranking</h2>

              <p>
                Relative contribution of each detected
                attack class.
              </p>
            </div>

            <div className="analytics-v2-card-icon">
              <Target size={18} />
            </div>

          </div>


          <div className="analytics-v2-ranking-list">

            {topClasses.map((item, index) => {

              const percentage =
                threats > 0
                  ? (item.count / threats) * 100
                  : 0;

              return (
                <div
                  className="analytics-v2-ranking-row"
                  key={item.name}
                >

                  <div className="analytics-v2-rank">
                    {index + 1}
                  </div>

                  <div className="analytics-v2-ranking-main">

                    <div className="analytics-v2-ranking-title">
                      <strong>{item.name}</strong>

                      <span>
                        {formatNumber(item.count)}
                      </span>
                    </div>

                    <div className="analytics-v2-ranking-track">

                      <div
                        className="analytics-v2-ranking-fill"
                        style={{
                          width: `${Math.max(
                            percentage,
                            1
                          )}%`,
                        }}
                      />

                    </div>

                  </div>

                  <span className="analytics-v2-ranking-percent">
                    {percentage >= 0.01
                      ? `${percentage.toFixed(2)}%`
                      : "<0.01%"}
                  </span>

                </div>
              );
            })}

          </div>

        </section>


        {/* ====================================================
            ANALYSIS SUMMARY
           ==================================================== */}

        <section className="analytics-v2-card analytics-v2-summary">

          <div className="analytics-v2-card-header">

            <div>
              <span>SECURITY INSIGHTS</span>

              <h2>Analysis Summary</h2>

              <p>
                Key observations from the current dataset.
              </p>
            </div>

            <div className="analytics-v2-card-icon">
              <Activity size={18} />
            </div>

          </div>


          <div className="analytics-v2-insights">

            <div className="analytics-v2-insight">

              <div className="analytics-v2-insight-icon cyan">
                <Activity size={17} />
              </div>

              <div>
                <span>TRAFFIC ANALYZED</span>
                <strong>
                  {formatNumber(totalFlows)} flows
                </strong>
                <small>
                  Total network flows processed by
                  the intelligence engine.
                </small>
              </div>

            </div>


            <div className="analytics-v2-insight">

              <div className="analytics-v2-insight-icon red">
                <ShieldAlert size={17} />
              </div>

              <div>
                <span>THREAT EXPOSURE</span>

                <strong className="red-text">
                  {formatPercent(attackRate)}%
                </strong>

                <small>
                  Percentage of traffic classified as
                  malicious.
                </small>
              </div>

            </div>


            <div className="analytics-v2-insight">

              <div className="analytics-v2-insight-icon purple">
                <Target size={17} />
              </div>

              <div>
                <span>DOMINANT ATTACK</span>

                <strong>
                  {topClasses[0]?.name || "None"}
                </strong>

                <small>
                  {topClasses[0]
                    ? `${formatNumber(
                        topClasses[0].count
                      )} detections`
                    : "No attack detected"}
                </small>
              </div>

            </div>


            <div className="analytics-v2-insight">

              <div className="analytics-v2-insight-icon green">
                <ShieldCheck size={17} />
              </div>

              <div>
                <span>ATTACK CLASSES</span>

                <strong>
                  {entries.length}
                </strong>

                <small>
                  Distinct attack categories detected
                  in this analysis.
                </small>
              </div>

            </div>

          </div>

        </section>

      </div>

    </div>
  );
}

export default Analytics;