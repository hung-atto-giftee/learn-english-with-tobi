import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";
import DictionaryModal from "../components/DictionaryModal";
import { apiRequest } from "../lib/api";

const PAGE_SIZE = 10;

function getTodayDateValue() {
  return new Date().toISOString().slice(0, 10);
}

function formatDate(value) {
  return new Date(value).toLocaleString();
}

function getEntryDate(item) {
  return item.updated_at || item.created_at || "";
}

function highlightText(text, keyword) {
  if (!keyword) {
    return text;
  }

  const normalizedKeyword = keyword.trim();
  if (!normalizedKeyword) {
    return text;
  }

  const regex = new RegExp(`(${normalizedKeyword})`, "ig");
  const parts = String(text).split(regex);

  return parts.map((part, index) =>
    part.toLowerCase() === normalizedKeyword.toLowerCase() ? (
      <mark key={`${part}-${index}`} className="search-highlight">
        {part}
      </mark>
    ) : (
      <span key={`${part}-${index}`}>{part}</span>
    )
  );
}

export default function VocabularyPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [items, setItems] = useState([]);
  const [searchInput, setSearchInput] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [startDate, setStartDate] = useState(() => getTodayDateValue());
  const [endDate, setEndDate] = useState(() => getTodayDateValue());
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState({
    page: 1,
    limit: PAGE_SIZE,
    total: 0,
    total_pages: 1,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [selectedWord, setSelectedWord] = useState("");
  const [dictionaryData, setDictionaryData] = useState(null);
  const [isDictionaryLoading, setIsDictionaryLoading] = useState(false);
  const [dictionaryError, setDictionaryError] = useState("");

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      setDebouncedSearch(searchInput.trim());
      setPage(1);
    }, 300);

    return () => window.clearTimeout(timeoutId);
  }, [searchInput]);

  useEffect(() => {
    async function loadVocabulary() {
      setIsLoading(true);
      setErrorMessage("");

      try {
        const params = new URLSearchParams({
          page: String(page),
          limit: String(PAGE_SIZE),
          search: debouncedSearch,
          start_date: startDate,
          end_date: endDate,
        });

        const response = await apiRequest(`/dictionary/list?${params.toString()}`, {
          method: "GET",
        });

        if (response.status === 401) {
          logout();
          navigate("/login", { replace: true });
          return;
        }

        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
          throw new Error(data.detail || "Could not load dictionary list.");
        }

        setItems(data.items || []);
        setPagination({
          page: data.page || 1,
          limit: data.limit || PAGE_SIZE,
          total: data.total || 0,
          total_pages: data.total_pages || 1,
        });
      } catch (error) {
        setErrorMessage(error.message);
      } finally {
        setIsLoading(false);
      }
    }

    loadVocabulary();
  }, [debouncedSearch, endDate, logout, navigate, page, startDate]);

  const totalLabel = useMemo(() => pagination.total || 0, [pagination.total]);

  function handleStartDateChange(event) {
    setStartDate(event.target.value);
    setPage(1);
  }

  function handleEndDateChange(event) {
    setEndDate(event.target.value);
    setPage(1);
  }

  function clearDateFilters() {
    setStartDate("");
    setEndDate("");
    setPage(1);
  }

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  function closeDictionaryModal() {
    setSelectedWord("");
    setDictionaryData(null);
    setDictionaryError("");
    setIsDictionaryLoading(false);
  }

  async function handleOpenWord(item) {
    setSelectedWord(item.word);
    setDictionaryError("");
    setDictionaryData({
      word: item.word,
      phonetic: item.phonetic,
      meanings: item.meanings,
    });

    if (item.meanings?.length) {
      return;
    }

    setIsDictionaryLoading(true);

    try {
      const response = await apiRequest(
        `/dictionary?word=${encodeURIComponent(item.word)}`,
        { method: "GET" }
      );

      if (response.status === 401) {
        logout();
        navigate("/login", { replace: true });
        return;
      }

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || "Could not load dictionary result.");
      }

      setDictionaryData(data);
    } catch (error) {
      setDictionaryError(error.message);
    } finally {
      setIsDictionaryLoading(false);
    }
  }

  return (
    <div className="page-shell">
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      <main className="app-card">
        <section className="hero hero-row">
          <div>
            <p className="eyebrow">Study English With Tobi</p>
            <h1>Browse your dictionary results.</h1>
            <p className="hero-copy">
              Search words, browse cached dictionary entries, and reopen details
              anytime.
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
          <div className="section-heading" style={{ marginBottom: "1rem" }}>
            <h2>Dictionary Search</h2>
            <span>{totalLabel} results</span>
          </div>

          <input
            className="auth-input"
            type="text"
            placeholder="Search a word..."
            value={searchInput}
            onChange={(event) => setSearchInput(event.target.value)}
          />

          <div className="filter-row">
            <div className="filter-field">
              <label className="field-label" htmlFor="start-date">
                From date
              </label>
              <input
                id="start-date"
                className="auth-input"
                type="date"
                value={startDate}
                onChange={handleStartDateChange}
              />
            </div>

            <div className="filter-field">
              <label className="field-label" htmlFor="end-date">
                To date
              </label>
              <input
                id="end-date"
                className="auth-input"
                type="date"
                value={endDate}
                onChange={handleEndDateChange}
              />
            </div>

            <button
              className="ghost-button filter-clear-button"
              type="button"
              onClick={clearDateFilters}
              disabled={!startDate && !endDate}
            >
              Clear filters
            </button>
          </div>

          {isLoading ? (
            <div className="empty-state">Loading dictionary entries...</div>
          ) : items.length === 0 ? (
            <div className="empty-state" style={{marginTop: "2rem"}}>
              No results found. Try a different keyword.
            </div>
          ) : (
            <div className="vocabulary-list" style={{marginTop: "2rem"}}>
              {items.map((item) => (
                <button
                  key={item.id}
                  className="vocabulary-card"
                  type="button"
                  onClick={() => handleOpenWord(item)}
                >
                  <div className="history-card-header">
                    <div>
                      <p className="history-label">Word</p>
                      <p className="vocabulary-word">
                        {highlightText(item.word, debouncedSearch)}
                      </p>
                    </div>
                    <p className="history-date">{formatDate(getEntryDate(item))}</p>
                  </div>

                  <div className="vocabulary-grid">
                    <div className="history-row">
                      <p className="history-label">Phonetic</p>
                      <p className="history-text">{item.phonetic || "No IPA available"}</p>
                    </div>

                    <div className="history-row">
                      <p className="history-label">Meaning</p>
                      <p className="history-text">
                        {item.meanings?.[0]?.vi
                          ? highlightText(item.meanings[0].vi, debouncedSearch)
                          : item.meanings?.[0]?.definition || "Tap to load meaning"}
                      </p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          )}

          <div className="pagination-row">
            <button
              className="secondary-button"
              type="button"
              onClick={() => setPage((currentPage) => Math.max(1, currentPage - 1))}
              disabled={pagination.page <= 1 || isLoading}
            >
              Previous
            </button>
            <span className="pagination-label">
              Page {pagination.page} / {pagination.total_pages}
            </span>
            <button
              className="secondary-button"
              type="button"
              onClick={() =>
                setPage((currentPage) =>
                  Math.min(pagination.total_pages, currentPage + 1)
                )
              }
              disabled={pagination.page >= pagination.total_pages || isLoading}
            >
              Next
            </button>
          </div>
        </section>

        {errorMessage ? <div className="error-banner">{errorMessage}</div> : null}
      </main>

      <DictionaryModal
        isOpen={Boolean(selectedWord)}
        word={selectedWord}
        data={dictionaryData}
        isLoading={isDictionaryLoading}
        errorMessage={dictionaryError}
        onClose={closeDictionaryModal}
      />
    </div>
  );
}
