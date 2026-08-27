import {
  BarChart3,
  ChevronRight,
} from "lucide-react";

function ThreatDistribution({
  attackTypes,
  total,
}) {
  const entries = Object.entries(attackTypes || {})
    .map(([name, count]) => ({
      name,
      count: Number(count) || 0,
    }))
    .filter((item) => item.count > 0)
    .sort((a, b) => b.count - a.count);

  const totalThreats = entries.reduce(
    (sum, item) => sum + item.count,
    0
  );

  const topClasses = entries.slice(0, 5);

  if (!topClasses.length) {
    return (
      <div className="threat-distribution-empty">
        <BarChart3 size={28} />

        <strong>No threats detected</strong>

        <span>
          Analyze network traffic to populate
          the threat distribution.
        </span>
      </div>
    );
  }

  return (
    <div className="threat-distribution compact-threat-distribution">

      <div className="threat-distribution-summary">

        <div>
          <span className="td-label">
            DETECTED THREATS
          </span>

          <strong>
            {totalThreats.toLocaleString()}
          </strong>
        </div>

        <div>
          <span className="td-label">
            TOTAL FLOWS
          </span>

          <strong>
            {Number(total || 0).toLocaleString()}
          </strong>
        </div>

        <div>
          <span className="td-label">
            CLASSES
          </span>

          <strong>
            {entries.length}
          </strong>
        </div>

      </div>


      <div className="compact-threat-list">

        {topClasses.map((item, index) => {

          const percentage =
            totalThreats > 0
              ? (item.count / totalThreats) * 100
              : 0;

          const width =
            topClasses[0]?.count > 0
              ? (item.count / topClasses[0].count) * 100
              : 0;

          return (
            <div
              className="compact-threat-row"
              key={item.name}
            >

              <div className="compact-threat-rank">
                {index + 1}
              </div>

              <div className="compact-threat-main">

                <div className="compact-threat-header">

                  <strong>
                    {item.name}
                  </strong>

                  <span>
                    {item.count.toLocaleString()}
                  </span>

                </div>

                <div className="compact-threat-track">

                  <div
                    className="compact-threat-fill"
                    style={{
                      width: `${Math.max(width, 2)}%`,
                    }}
                  />

                </div>

                <small>
                  {percentage.toFixed(1)}% of threats
                </small>

              </div>

            </div>
          );
        })}

      </div>


      {entries.length > 5 && (
        <button
          className="threat-more-button"
          onClick={() =>
            window.dispatchEvent(
              new CustomEvent(
                "cyberintel:navigate",
                {
                  detail: "detection",
                }
              )
            )
          }
        >
          <span>
            View all {entries.length} threat classes
          </span>

          <ChevronRight size={16} />
        </button>
      )}

    </div>
  );
}

export default ThreatDistribution;