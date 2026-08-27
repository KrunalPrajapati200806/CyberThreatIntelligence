import { RefreshCw } from "lucide-react";

function Topbar({
  eyebrow,
  title,
  description,
  apiOnline,
  onRefresh,
}) {
  return (
    <header className="topbar">

      <div>

        <div className="eyebrow">
          {eyebrow}
        </div>

        <h2>
          {title}
        </h2>

        <p>
          {description}
        </p>

      </div>


      <div className="topbar-actions">

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
          onClick={onRefresh}
          title="Refresh API status"
        >
          <RefreshCw size={18} />
        </button>

      </div>

    </header>
  );
}

export default Topbar;