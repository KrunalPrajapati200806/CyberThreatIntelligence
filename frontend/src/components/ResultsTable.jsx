function ResultsTable({ result }) {

  if (!result) {

    return (
      <div className="table-empty">

        <strong>
          No analysis available
        </strong>

        <span>
          Upload and analyze a traffic file first.
        </span>

      </div>
    );
  }


  const rows =
    result.results || [];


  if (rows.length === 0) {

    return (
      <div className="table-empty">

        <strong>
          No individual predictions returned
        </strong>

        <span>
          The analysis completed but did not return flow-level results.
        </span>

      </div>
    );
  }


  const visible =
    rows.slice(0, 100);


  return (

    <div className="results-table-wrapper">

      <table className="results-table">

        <thead>

          <tr>

            <th>
              #
            </th>

            <th>
              Prediction
            </th>

            <th>
              Confidence
            </th>

            <th>
              Status
            </th>

          </tr>

        </thead>


        <tbody>

          {visible.map(
            (row, index) => {

              const prediction =
                row.prediction ??
                row.label ??
                row.attack_type ??
                row.class ??
                "Unknown";


              const confidence =
                row.confidence ??
                row.probability ??
                row.score;


              const text =
                String(prediction);


              const attack =
                text.toLowerCase() !==
                "benign";


              return (

                <tr
                  key={index}
                >

                  <td>
                    {index + 1}
                  </td>


                  <td>
                    {text}
                  </td>


                  <td>

                    {confidence !== undefined
                      ? `${(
                          Number(confidence) *
                          100
                        ).toFixed(2)}%`
                      : "—"}

                  </td>


                  <td>

                    <span
                      className={
                        attack
                          ? "status-threat"
                          : "status-safe"
                      }
                    >

                      {attack
                        ? "THREAT"
                        : "BENIGN"}

                    </span>

                  </td>

                </tr>

              );

            }
          )}

        </tbody>

      </table>

    </div>
  );
}


export default ResultsTable;