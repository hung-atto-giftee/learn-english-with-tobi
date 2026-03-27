import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";
import { apiRequest } from "../lib/api";

function formatDate(value) {
  return new Date(value).toLocaleString();
}

function getAccuracyClass(accuracy) {
  if (accuracy >= 80) {
    return "history-badge-high";
  }

  if (accuracy >= 50) {
    return "history-badge-medium";
  }

  return "history-badge-low";
}

export default function HistoryPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function loadHistoryData() {
      setIsLoading(true);
      setErrorMessage("");

      try {
        const [historyResponse, statsResponse] = await Promise.all([
          apiRequest("/history", { method: "GET" }),
          apiRequest("/history/stats", { method: "GET" }),
        ]);

        if (historyResponse.status === 401 || statsResponse.status === 401) {
          logout();
          navigate("/login", { replace: true });
          return;
        }

        const historyData = await historyResponse.json().catch(() => ({}));
        const statsData = await statsResponse.json().catch(() => ({}));

        if (!historyResponse.ok) {
          throw new Error(historyData.detail || "Could not load learning history.");
        }

        if (!statsResponse.ok) {
          throw new Error(statsData.detail || "Could not load learning stats.");
        }

        setHistory(historyData.history || []);
        setStats(statsData);
      } catch (error) {
        setErrorMessage(error.message);
      } finally {
        setIsLoading(false);
      }
    }

    loadHistoryData();
  }, [logout, navigate]);

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="page-shell">
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      <main className="app-card">
        <section className="hero hero-row">
          <div>
            <p className="eyebrow">Study English With Tobi</p>
            <h1>Your learning history and progress.</h1>
            <p className="hero-copy">
              Review past dictation attempts, accuracy trends, and your recent
              learning activity.
            </p>
          </div>

          <div className="user-box">
            <p className="user-label">Logged in as</p>
            <p className="user-email">{user?.email || "Unknown user"}</p>
            <div className="action-row compact-row">
              <button
                className="secondary-button"
                type="button"
                onClick={() => navigate("/")}
              >
                Back To Practice
              </button>
              <button className="ghost-button" type="button" onClick={handleLogout}>
                Logout
              </button>
            </div>
          </div>
        </section>

        <section className="panel">
          <div className="section-heading">
            <h2>Stats</h2>
            <span>{stats ? "Updated" : "Waiting"}</span>
          </div>

          {isLoading ? (
            <div className="empty-state">Loading your stats...</div>
          ) : stats ? (
            <div className="history-stats-grid">
              <div className="metric-card">
                <p className="metric-label">Average Accuracy</p>
                <p className="metric-value">{stats.average_accuracy}%</p>
              </div>

              <div className="metric-card metric-card-cool">
                <p className="metric-label">Total Sentences</p>
                <p className="metric-value">{stats.total_sentences_practiced}</p>
              </div>

              <div className="feedback-card">
                <p className="feedback-title">Accuracy Trend</p>
                {stats.accuracy_trend?.length ? (
                  <div className="trend-chart">
                    {stats.accuracy_trend.map((item, index) => (
                      <div key={`${item.created_at}-${index}`} className="trend-bar-wrap">
                        <div
                          className="trend-bar"
                          style={{ height: `${Math.max(item.accuracy, 6)}%` }}
                          title={`${item.accuracy}% on ${formatDate(item.created_at)}`}
                        />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="empty-state compact-empty">No trend data yet.</div>
                )}
              </div>
            </div>
          ) : (
            <div className="empty-state">No stats available yet.</div>
          )}
        </section>

        <section className="panel">
          <div className="section-heading">
            <h2>Learning History</h2>
            <span>{history.length} recent records</span>
          </div>

          {isLoading ? (
            <div className="empty-state">Loading your history...</div>
          ) : history.length === 0 ? (
            <div className="empty-state">
              No learning history yet. Finish a dictation exercise to see your
              results here.
            </div>
          ) : (
            <div className="history-list">
              {history.map((item) => (
                <article key={item.id} className="history-card">
                  <div className="history-card-header">
                    <p className="history-date">{formatDate(item.created_at)}</p>
                    <span className={`history-badge ${getAccuracyClass(item.accuracy)}`}>
                      {item.accuracy}%
                    </span>
                  </div>

                  <div className="history-row">
                    <p className="history-label">Sentence</p>
                    <p className="history-text">{item.sentence}</p>
                  </div>

                  <div className="history-row">
                    <p className="history-label">Your Input</p>
                    <p className="history-text">{item.user_input || "No input recorded"}</p>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {errorMessage ? <div className="error-banner">{errorMessage}</div> : null}
      </main>
    </div>
  );
}
