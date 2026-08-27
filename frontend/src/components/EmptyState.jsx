import { Network } from "lucide-react";

function EmptyState({
  title = "No analysis loaded",
  message = "Upload and analyze a file to see results.",
}) {
  return (
    <div className="table-empty">

      <div className="empty-icon">
        <Network size={28} />
      </div>

      <strong>
        {title}
      </strong>

      <span>
        {message}
      </span>

    </div>
  );
}

export default EmptyState;