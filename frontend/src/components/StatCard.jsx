function StatCard({
  icon: Icon,
  label,
  value,
  hint,
  tone = "cyan",
}) {
  return (
    <div
      className={`stat-card ${tone}`}
    >

      <div className="stat-icon">
        <Icon size={20} />
      </div>

      <div className="stat-content">

        <span>
          {label}
        </span>

        <strong>
          {value}
        </strong>

        <small>
          {hint}
        </small>

      </div>

    </div>
  );
}

export default StatCard;