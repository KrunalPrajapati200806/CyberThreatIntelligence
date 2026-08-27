import {
  LayoutDashboard,
  Network,
  ShieldAlert,
  BarChart3,
  FileBarChart,
  History,
  ChevronRight,
  ChevronLeft,
  Shield,
  Activity,
} from "lucide-react";


const operations = [

  {
    id: "dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
  },

  {
    id: "traffic",
    label: "Traffic Analysis",
    icon: Network,
  },

  {
    id: "detection",
    label: "Threat Detection",
    icon: ShieldAlert,
  },

  {
    id: "analytics",
    label: "Analytics",
    icon: BarChart3,
  },

  {
    id: "reports",
    label: "Reports",
    icon: FileBarChart,
  },

];


export default function Sidebar({
  activeNav,
  setActiveNav,
  apiOnline,
  collapsed,
  setCollapsed,
}) {

  const navigation = (id) => {
    setActiveNav(id);
  };


  return (

    <aside
      className={`sidebar ${
        collapsed
          ? "collapsed"
          : ""
      }`}
    >

      <div className="sidebar-header">

        <div className="brand-mark">
          <Shield size={21} />
        </div>


        {!collapsed && (

          <div className="brand-text">

            <strong>
              CyberIntel
            </strong>

            <span>
              Threat Intelligence
            </span>

          </div>

        )}

      </div>


      <button
        className="sidebar-toggle"
        onClick={() =>
          setCollapsed(
            !collapsed
          )
        }
        title={
          collapsed
            ? "Expand sidebar"
            : "Collapse sidebar"
        }
      >

        {collapsed ? (
          <ChevronRight
            size={17}
          />
        ) : (
          <ChevronLeft
            size={17}
          />
        )}

      </button>


      <div className="sidebar-scroll">

        <div className="sidebar-section">

          {!collapsed && (
            <div className="sidebar-label">
              OPERATIONS
            </div>
          )}


          {operations.map(
            ({
              id,
              label,
              icon: Icon,
            }) => (

              <button
                key={id}
                className={`nav-item ${
                  activeNav === id
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  navigation(id)
                }
                title={
                  collapsed
                    ? label
                    : undefined
                }
              >

                <Icon size={19} />

                {!collapsed && (
                  <>
                    <span>
                      {label}
                    </span>

                    <ChevronRight
                      size={15}
                      className="nav-arrow"
                    />
                  </>
                )}

              </button>

            )
          )}

        </div>


        <div className="sidebar-section">

          {!collapsed && (
            <div className="sidebar-label">
              HISTORY
            </div>
          )}


          <button
            className={`nav-item ${
              activeNav === "history"
                ? "active"
                : ""
            }`}
            onClick={() =>
              navigation("history")
            }
            title={
              collapsed
                ? "Analysis History"
                : undefined
            }
          >

            <History
              size={19}
            />

            {!collapsed && (
              <>
                <span>
                  Analysis History
                </span>

                <ChevronRight
                  size={15}
                  className="nav-arrow"
                />
              </>
            )}

          </button>

        </div>

      </div>


      <div className="sidebar-system">

        <div className="system-status">

          <span
            className={`status-dot ${
              apiOnline
                ? "online"
                : "offline"
            }`}
          />

          {!collapsed && (

            <div>

              <strong>
                {apiOnline
                  ? "SYSTEM ONLINE"
                  : "API OFFLINE"}
              </strong>

              <span>
                Random Forest ML Engine
              </span>

              <small>
                FastAPI · Port 8000
              </small>

            </div>

          )}

        </div>

      </div>


      <div className="sidebar-footer">

        {!collapsed && (
          <>
            <span>
              CYBERINTEL
            </span>

            <strong>
              v1.0.0
            </strong>
          </>
        )}

      </div>

    </aside>

  );
}