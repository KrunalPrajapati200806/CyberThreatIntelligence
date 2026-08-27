import {
  Activity,
  CalendarClock,
  Database,
  FileText,
  Search,
  ShieldAlert,
  ShieldCheck,
  Trash2,
  Eye,
  BarChart3,
} from "lucide-react";

import { useMemo, useState } from "react";

import Topbar from "../components/Topbar";


function formatDate(timestamp) {

  if (!timestamp) {
    return "Unknown date";
  }

  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return "Unknown date";
  }

  return date.toLocaleString(
    "en-IN",
    {
      dateStyle: "medium",
      timeStyle: "short",
    }
  );

}


function getSeverity(rate) {

  const value = Number(rate) || 0;

  if (value >= 50) {
    return {
      label: "CRITICAL",
      className: "critical",
    };
  }

  if (value >= 20) {
    return {
      label: "HIGH",
      className: "high",
    };
  }

  if (value >= 5) {
    return {
      label: "MEDIUM",
      className: "medium",
    };
  }

  return {
    label: "LOW",
    className: "low",
  };

}


export default function History({
  history,
  onSelect,
  onClear,
}) {

  const [search, setSearch] =
    useState("");


  const filteredHistory = useMemo(() => {

    const query =
      search.trim().toLowerCase();

    if (!query) {
      return history || [];
    }

    return (history || []).filter(
      (item) => {

        const filename =
          String(
            item.fileName || ""
          ).toLowerCase();

        const model =
          String(
            item.model || ""
          ).toLowerCase();

        const classes =
          Object.keys(
            item.attack_types || {}
          )
            .join(" ")
            .toLowerCase();

        return (
          filename.includes(query) ||
          model.includes(query) ||
          classes.includes(query)
        );

      }
    );

  }, [history, search]);


  const totalAnalyses =
    history?.length || 0;


  const totalFlows =
    (history || []).reduce(
      (sum, item) =>
        sum +
        (Number(
          item.total_flows
        ) || 0),
      0
    );


  const totalThreats =
    (history || []).reduce(
      (sum, item) =>
        sum +
        (Number(
          item.attacks
        ) || 0),
      0
    );


  return (

    <div className="history-page">

      <Topbar
        eyebrow="ANALYSIS ARCHIVE"
        title="Analysis History"
        description="Search, review and reopen previously analyzed network traffic."
        actions={
          <>
            <div
              className="history-counter"
            >
              <Database size={15} />

              <span>
                {totalAnalyses}{" "}
                {totalAnalyses === 1
                  ? "analysis"
                  : "analyses"}
              </span>

            </div>

            <button
              className="history-clear-button"
              onClick={onClear}
              disabled={
                totalAnalyses === 0
              }
            >
              <Trash2 size={15} />
              Clear History
            </button>
          </>
        }
      />


      <section className="history-overview">

        <div className="history-overview-card">

          <div className="history-overview-icon cyan">
            <Database size={20} />
          </div>

          <div>
            <span>
              ANALYSES
            </span>

            <strong>
              {totalAnalyses}
            </strong>
          </div>

        </div>


        <div className="history-overview-card">

          <div className="history-overview-icon purple">
            <Activity size={20} />
          </div>

          <div>
            <span>
              FLOWS PROCESSED
            </span>

            <strong>
              {totalFlows.toLocaleString()}
            </strong>
          </div>

        </div>


        <div className="history-overview-card">

          <div className="history-overview-icon red">
            <ShieldAlert size={20} />
          </div>

          <div>
            <span>
              THREATS DETECTED
            </span>

            <strong>
              {totalThreats.toLocaleString()}
            </strong>
          </div>

        </div>

      </section>


      <section className="history-toolbar">

        <div className="history-search">

          <Search size={18} />

          <input
            value={search}
            onChange={(event) =>
              setSearch(
                event.target.value
              )
            }
            placeholder="Search by file name, attack class or model..."
          />

          {search && (

            <button
              className="history-search-clear"
              onClick={() =>
                setSearch("")
              }
            >
              ×
            </button>

          )}

        </div>


        <div className="history-result-count">

          {filteredHistory.length}{" "}
          result
          {filteredHistory.length !== 1
            ? "s"
            : ""}

        </div>

      </section>


      {!history?.length ? (

        <section className="history-empty">

          <div className="history-empty-icon">
            <FileText size={32} />
          </div>

          <h3>
            No analysis history
          </h3>

          <p>
            Once you analyze a network
            traffic CSV, the analysis
            summary will appear here.
          </p>

          <button
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
            Analyze Traffic
          </button>

        </section>

      ) : filteredHistory.length === 0 ? (

        <section className="history-empty">

          <div className="history-empty-icon">
            <Search size={32} />
          </div>

          <h3>
            No matching analyses
          </h3>

          <p>
            Try another filename,
            attack class or model name.
          </p>

          <button
            onClick={() =>
              setSearch("")
            }
          >
            Clear Search
          </button>

        </section>

      ) : (

        <section className="history-list">

          {filteredHistory.map(
            (item, index) => {

              const severity =
                getSeverity(
                  item.attack_rate
                );


              const attackTypes =
                Object.entries(
                  item.attack_types ||
                  {}
                )
                  .map(
                    ([name, count]) => ({
                      name,
                      count:
                        Number(count) ||
                        0,
                    })
                  )
                  .sort(
                    (a, b) =>
                      b.count -
                      a.count
                  );


              const topClasses =
                attackTypes.slice(
                  0,
                  5
                );


              return (

                <article
                  className={`history-card ${severity.className}`}
                  key={
                    item.id ||
                    `${item.fileName}-${index}`
                  }
                >

                  <div className="history-card-accent" />


                  <div className="history-card-header">

                    <div className="history-file-icon">
                      <FileText size={22} />
                    </div>


                    <div className="history-file-info">

                      <div className="history-file-top">

                        <span className="history-number">
                          #{index + 1}
                        </span>

                        <span
                          className={`severity-badge ${severity.className}`}
                        >
                          {severity.label}
                        </span>

                      </div>


                      <h3
                        title={
                          item.fileName
                        }
                      >
                        {item.fileName ||
                          "Unknown file"}
                      </h3>


                      <div className="history-meta">

                        <span>
                          <CalendarClock
                            size={13}
                          />

                          {formatDate(
                            item.timestamp
                          )}
                        </span>

                        <span>
                          <BarChart3
                            size={13}
                          />

                          Random Forest
                        </span>

                      </div>

                    </div>

                  </div>


                  <div className="history-metrics">

                    <div className="history-metric">

                      <span>
                        TOTAL FLOWS
                      </span>

                      <strong>
                        {Number(
                          item.total_flows ||
                          0
                        ).toLocaleString()}
                      </strong>

                    </div>


                    <div className="history-metric danger">

                      <span>
                        THREATS
                      </span>

                      <strong>
                        {Number(
                          item.attacks ||
                          0
                        ).toLocaleString()}
                      </strong>

                    </div>


                    <div className="history-metric safe">

                      <span>
                        BENIGN
                      </span>

                      <strong>
                        {Number(
                          item.benign ||
                          0
                        ).toLocaleString()}
                      </strong>

                    </div>


                    <div className="history-metric rate">

                      <span>
                        ATTACK RATE
                      </span>

                      <strong>
                        {Number(
                          item.attack_rate ||
                          0
                        ).toFixed(4)}
                        %
                      </strong>

                    </div>

                  </div>


                  <div className="history-classes">

                    <div className="history-classes-header">

                      <span>
                        DETECTED CLASSES
                      </span>

                      <strong>
                        {attackTypes.length}
                      </strong>

                    </div>


                    <div className="history-class-chips">

                      {topClasses.map(
                        (type) => (

                          <span
                            className="history-class-chip"
                            key={type.name}
                          >
                            {type.name}

                            <b>
                              {type.count.toLocaleString()}
                            </b>
                          </span>

                        )
                      )}


                      {attackTypes.length >
                        5 && (

                        <span className="history-class-chip more">
                          +
                          {attackTypes.length -
                            5}{" "}
                          more
                        </span>

                      )}

                    </div>

                  </div>


                  <div className="history-card-footer">

                    <span className="history-model">

                      <ShieldCheck
                        size={14}
                      />

                      random_forest_multiclass

                    </span>


                    <div className="history-actions">

                      <button
                        className="history-view-button"
                        onClick={() =>
                          onSelect(item)
                        }
                      >

                        <Eye size={16} />

                        View Analysis

                      </button>


                      <button
                        className="history-delete-button"
                        onClick={() => {

                          if (
                            window.confirm(
                              "Delete this analysis from history?"
                            )
                          ) {

                            const remaining =
                              (history || []).filter(
                                (entry) =>
                                  entry.id !==
                                  item.id
                              );

                            /*
                             * The parent owns the
                             * history state, so use
                             * the same clear handler
                             * only when deleting all.
                             *
                             * Individual deletion is
                             * handled below by dispatch.
                             */

                            window.dispatchEvent(
                              new CustomEvent(
                                "cyberintel:delete-history",
                                {
                                  detail:
                                    item.id,
                                }
                              )
                            );

                          }

                        }}
                        title="Delete analysis"
                      >
                        <Trash2 size={16} />
                      </button>

                    </div>

                  </div>

                </article>

              );

            }
          )}

        </section>

      )}

    </div>

  );

}