import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Activity,
} from "lucide-react";


function ThreatDetection({ result }) {

  if (!result) {

    return (
      <div className="page detection-page">

        <div className="page-header">

          <div>

            <span className="eyebrow">
              THREAT DETECTION
            </span>

            <h1>
              Threat Detection
            </h1>

            <p>
              Investigate malicious network activity
              identified by the machine-learning engine.
            </p>

          </div>

        </div>


        <div className="detection-empty">

          <ShieldCheck size={44} />

          <h2>
            No active analysis
          </h2>

          <p>
            Upload network traffic from Traffic Analysis
            to begin threat investigation.
          </p>

        </div>

      </div>
    );

  }


  const total =
    Number(result.total_flows) || 0;

  const threats =
    Number(result.attacks) || 0;

  const benign =
    Number(result.benign) || 0;

  const attackRate =
    Number(result.attack_rate) || 0;


  const attacks =
    Object.entries(
      result.attack_types || {}
    )
      .map(([name, count]) => ({
        name,
        count: Number(count) || 0,
      }))
      .filter((item) => item.count > 0)
      .sort((a, b) => b.count - a.count);


  const maxCount =
    attacks.length
      ? attacks[0].count
      : 1;


  const getSeverity = (percentage) => {

    if (percentage >= 25) {
      return "CRITICAL";
    }

    if (percentage >= 10) {
      return "HIGH";
    }

    if (percentage >= 2) {
      return "MEDIUM";
    }

    return "LOW";

  };


  const formatNumber = (value) =>
    Number(value || 0).toLocaleString();


  return (

    <div className="page detection-page">


      {/* HEADER */}

      <div className="page-header">

        <div>

          <span className="eyebrow">
            THREAT DETECTION
          </span>

          <h1>
            Threat Detection
          </h1>

          <p>
            Investigate malicious activity identified
            by the Random Forest intelligence engine.
          </p>

        </div>

      </div>


      {/* SUMMARY */}

      <div className="detection-summary">


        <div className="detection-stat">

          <div className="detection-icon red">
            <ShieldAlert size={19} />
          </div>

          <div>

            <span>
              Threats detected
            </span>

            <strong>
              {formatNumber(threats)}
            </strong>

          </div>

        </div>


        <div className="detection-stat">

          <div className="detection-icon cyan">
            <Activity size={19} />
          </div>

          <div>

            <span>
              Flows inspected
            </span>

            <strong>
              {formatNumber(total)}
            </strong>

          </div>

        </div>


        <div className="detection-stat">

          <div className="detection-icon green">
            <ShieldCheck size={19} />
          </div>

          <div>

            <span>
              Benign flows
            </span>

            <strong>
              {formatNumber(benign)}
            </strong>

          </div>

        </div>


        <div className="detection-stat">

          <div className="detection-icon orange">
            <AlertTriangle size={19} />
          </div>

          <div>

            <span>
              Threat rate
            </span>

            <strong>
              {attackRate.toFixed(4)}%
            </strong>

          </div>

        </div>


      </div>



      {/* DETECTION TABLE */}

      <section className="detection-panel">

        <div className="detection-panel-header">

          <div>

            <span className="eyebrow">
              DETECTION QUEUE
            </span>

            <h2>
              Detected Threats
            </h2>

            <p>
              Ranked by observed attack volume.
            </p>

          </div>


          <div className="detection-count">
            {attacks.length} classes
          </div>

        </div>


        {attacks.length === 0 ? (

          <div className="detection-empty-small">

            <ShieldCheck size={32} />

            <strong>
              No threats detected
            </strong>

          </div>

        ) : (

          <div className="detection-list">

            {attacks.map(
              (item, index) => {

                const percentage =
                  threats > 0
                    ? (item.count / threats) * 100
                    : 0;

                const severity =
                  getSeverity(percentage);

                const width =
                  Math.max(
                    (item.count / maxCount) * 100,
                    2
                  );


                return (

                  <div
                    className="detection-row"
                    key={item.name}
                  >


                    <div className="detection-rank">
                      {index + 1}
                    </div>


                    <div className="detection-main">

                      <div className="detection-title">

                        <strong>
                          {item.name}
                        </strong>

                        <span
                          className={`severity-badge ${severity.toLowerCase()}`}
                        >
                          {severity}
                        </span>

                      </div>


                      <div className="detection-track">

                        <div
                          className="detection-fill"
                          style={{
                            width: `${width}%`,
                          }}
                        />

                      </div>

                    </div>


                    <div className="detection-number">

                      <strong>
                        {formatNumber(item.count)}
                      </strong>

                      <span>
                        {percentage.toFixed(2)}%
                      </span>

                    </div>

                  </div>

                );

              }
            )}

          </div>

        )}

      </section>


      {/* MODEL INFO */}

      <section className="detection-model-card">

        <div>

          <span className="eyebrow">
            ML ENGINE
          </span>

          <h3>
            Random Forest Multiclass
          </h3>

          <p>
            36 engineered network features ·
            15 supported attack classes
          </p>

        </div>


        <div className="model-status">
          <span />
          Model active
        </div>

      </section>

    </div>

  );

}


export default ThreatDetection;