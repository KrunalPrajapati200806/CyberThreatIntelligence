import { useMemo, useState } from "react";
import {
  Download,
  FileJson,
  FileSpreadsheet,
  FileText,
  ChevronDown,
  ShieldAlert,
  Activity,
  CheckCircle2,
} from "lucide-react";


function Reports({ result }) {
  const [exportOpen, setExportOpen] = useState(false);

  const attackTypes = useMemo(() => {
    return Object.entries(result?.attack_types || {})
      .map(([name, count]) => ({
        name,
        count: Number(count) || 0,
      }))
      .filter((item) => item.count > 0)
      .sort((a, b) => b.count - a.count);
  }, [result]);

  const totalFlows = Number(result?.total_flows || 0);
  const attacks = Number(result?.attacks || 0);
  const benign = Number(result?.benign || 0);

  const attackRate =
    Number(
      result?.attack_rate ??
        (totalFlows > 0 ? (attacks / totalFlows) * 100 : 0)
    ) || 0;

  const exportData = {
    report: "CyberIntel Network Attack Analysis",
    generated_at: new Date().toISOString(),
    model: "random_forest_multiclass",
    features: 36,
    classes: 15,
    total_flows: totalFlows,
    threats_detected: attacks,
    benign_flows: benign,
    attack_rate: attackRate,
    attack_types: Object.fromEntries(
      attackTypes.map((item) => [item.name, item.count])
    ),
  };

  const downloadFile = (content, filename, mimeType) => {
    const blob = new Blob([content], {
      type: mimeType,
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = filename;

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);

    setExportOpen(false);
  };

  const exportJSON = () => {
    downloadFile(
      JSON.stringify(exportData, null, 2),
      "cyberintel-analysis.json",
      "application/json"
    );
  };

  const exportCSV = () => {
    const rows = [
      [
        "Attack Class",
        "Detected",
        "Share (%)",
      ],
      ...attackTypes.map((item) => [
        item.name,
        item.count,
        attacks > 0
          ? ((item.count / attacks) * 100).toFixed(2)
          : "0.00",
      ]),
    ];

    const summary = [
      ["CyberIntel Analysis Report"],
      [],
      ["Metric", "Value"],
      ["Total Flows", totalFlows],
      ["Threats Detected", attacks],
      ["Benign Traffic", benign],
      ["Attack Rate (%)", attackRate.toFixed(4)],
      [],
      ...rows,
    ];

    const csv = summary
      .map((row) =>
        row
          .map((value) => {
            const text = String(value ?? "");
            return `"${text.replace(/"/g, '""')}"`;
          })
          .join(",")
      )
      .join("\n");

    downloadFile(
      csv,
      "cyberintel-analysis.csv",
      "text/csv;charset=utf-8"
    );
  };

  const exportTXT = () => {
    const lines = [
      "CYBERINTEL NETWORK ATTACK ANALYSIS",
      "===================================",
      "",
      `Generated: ${new Date().toLocaleString()}`,
      `Model: Random Forest Multiclass`,
      `Features: 36`,
      `Supported Classes: 15`,
      "",
      "ANALYSIS SUMMARY",
      "----------------",
      `Total Flows: ${totalFlows.toLocaleString()}`,
      `Threats Detected: ${attacks.toLocaleString()}`,
      `Benign Traffic: ${benign.toLocaleString()}`,
      `Attack Rate: ${attackRate.toFixed(4)}%`,
      "",
      "DETECTED ATTACK CLASSES",
      "------------------------",
      ...attackTypes.map(
        (item, index) =>
          `${index + 1}. ${item.name}: ${item.count.toLocaleString()}`
      ),
      "",
      "===================================",
      "CyberIntel - Network Attack Intelligence Platform",
    ];

    downloadFile(
      lines.join("\n"),
      "cyberintel-analysis.txt",
      "text/plain;charset=utf-8"
    );
  };

  if (!result) {
    return (
      <div className="reports-page">
        <div className="reports-header">
          <div>
            <span className="section-kicker">
              SECURITY REPORTING
            </span>

            <h1>Analysis Report</h1>

            <p>
              Executive summary of the latest network
              threat analysis.
            </p>
          </div>
        </div>

        <div className="report-empty">
          <Activity size={42} />

          <h2>No analysis available</h2>

          <p>
            Upload and analyze a network traffic CSV to
            generate a security report.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="reports-page">
      {/* HEADER */}

      <div className="reports-header">
        <div>
          <span className="section-kicker">
            SECURITY REPORTING
          </span>

          <h1>Analysis Report</h1>

          <p>
            Executive summary of the latest network
            threat analysis.
          </p>
        </div>

        {/* EXPORT */}

        <div className="export-wrapper">
          <button
            className="export-main-button"
            onClick={() =>
              setExportOpen((value) => !value)
            }
          >
            <Download size={17} />

            <span>Export</span>

            <ChevronDown
              size={16}
              className={
                exportOpen
                  ? "export-chevron-open"
                  : ""
              }
            />
          </button>

          {exportOpen && (
            <div className="export-menu">
              <button onClick={exportJSON}>
                <FileJson size={17} />

                <div>
                  <strong>JSON</strong>
                  <span>Machine-readable report</span>
                </div>
              </button>

              <button onClick={exportCSV}>
                <FileSpreadsheet size={17} />

                <div>
                  <strong>CSV</strong>
                  <span>Spreadsheet-compatible data</span>
                </div>
              </button>

              <button onClick={exportTXT}>
                <FileText size={17} />

                <div>
                  <strong>TXT</strong>
                  <span>Readable text report</span>
                </div>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* SUMMARY */}

      <div className="report-summary-grid">
        <div className="report-summary-card">
          <div className="report-card-icon cyan">
            <Activity size={20} />
          </div>

          <div>
            <span>FLOWS ANALYZED</span>

            <strong>
              {totalFlows.toLocaleString()}
            </strong>
          </div>
        </div>

        <div className="report-summary-card">
          <div className="report-card-icon red">
            <ShieldAlert size={20} />
          </div>

          <div>
            <span>THREATS DETECTED</span>

            <strong>
              {attacks.toLocaleString()}
            </strong>
          </div>
        </div>

        <div className="report-summary-card">
          <div className="report-card-icon green">
            <CheckCircle2 size={20} />
          </div>

          <div>
            <span>BENIGN TRAFFIC</span>

            <strong>
              {benign.toLocaleString()}
            </strong>
          </div>
        </div>

        <div className="report-summary-card">
          <div className="report-card-icon purple">
            <Activity size={20} />
          </div>

          <div>
            <span>ATTACK RATE</span>

            <strong>
              {attackRate.toFixed(4)}%
            </strong>
          </div>
        </div>
      </div>

      {/* ATTACK CLASSES */}

      <section className="report-section">
        <div className="report-section-header">
          <div>
            <span className="section-kicker">
              THREAT INTELLIGENCE
            </span>

            <h2>Detected Attack Classes</h2>

            <p>
              Ranked attack categories identified by the
              ML engine.
            </p>
          </div>

          <div className="report-model-badge">
            Random Forest · 36 Features · 15 Classes
          </div>
        </div>

        {attackTypes.length === 0 ? (
          <div className="report-no-threats">
            No malicious traffic detected.
          </div>
        ) : (
          <div className="attack-table">
            <div className="attack-table-header">
              <span>#</span>
              <span>ATTACK CLASS</span>
              <span>DETECTED</span>
              <span>SHARE</span>
            </div>

            {attackTypes.map((item, index) => {
              const share =
                attacks > 0
                  ? (item.count / attacks) * 100
                  : 0;

              return (
                <div
                  className="attack-table-row"
                  key={item.name}
                >
                  <span className="attack-rank">
                    {index + 1}
                  </span>

                  <strong>{item.name}</strong>

                  <span className="attack-count">
                    {item.count.toLocaleString()}
                  </span>

                  <div className="attack-share">
                    <div className="share-track">
                      <div
                        className="share-fill"
                        style={{
                          width: `${Math.max(
                            share,
                            1
                          )}%`,
                        }}
                      />
                    </div>

                    <span>
                      {share.toFixed(2)}%
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* REPORT FOOTER */}

      <div className="report-footer">
        <span>
          CyberIntel · Network Attack Intelligence
          Platform
        </span>

        <span>
          Generated automatically from the latest
          analysis
        </span>
      </div>
    </div>
  );
}

export default Reports;