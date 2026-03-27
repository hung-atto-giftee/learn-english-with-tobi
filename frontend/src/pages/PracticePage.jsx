import { useMemo, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";
import DictionaryModal from "../components/DictionaryModal";
import Word from "../components/Word";
import { apiRequest } from "../lib/api";

function splitIntoSentences(paragraph) {
  return paragraph
    .split(/(?<=[.!?])\s+/)
    .map((sentence) => sentence.trim())
    .filter(Boolean);
}

function normalizeParagraphInput(value) {
  return value.replace(/\s*\n+\s*/g, " ").replace(/\s{2,}/g, " ").trimStart();
}

function renderDiff(diff) {
  if (!diff?.length) {
    return <span className="diff-chip diff-chip-equal">Perfect match</span>;
  }

  return diff.map((item, index) => {
    const key = `${item.type}-${index}`;

    if (item.type === "equal") {
      return (
        <span key={key} className="diff-chip diff-chip-equal">
          {item.expected}
        </span>
      );
    }

    if (item.type === "missing") {
      return (
        <span key={key} className="diff-chip diff-chip-missing">
          Missing: {item.expected}
        </span>
      );
    }

    if (item.type === "incorrect") {
      return (
        <span key={key} className="diff-chip diff-chip-incorrect">
          {item.actual || "Empty"} → {item.expected}
        </span>
      );
    }

    return (
      <span key={key} className="diff-chip diff-chip-extra">
        Extra: {item.actual}
      </span>
    );
  });
}

export default function PracticePage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [paragraph, setParagraph] = useState("");
  const [sentences, setSentences] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [practiceData, setPracticeData] = useState(null);
  const [userInput, setUserInput] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [isLoadingPractice, setIsLoadingPractice] = useState(false);
  const [isLoadingEvaluation, setIsLoadingEvaluation] = useState(false);
  const [isDictionaryLoading, setIsDictionaryLoading] = useState(false);
  const [selectedWord, setSelectedWord] = useState("");
  const [dictionaryData, setDictionaryData] = useState(null);
  const [dictionaryError, setDictionaryError] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const audioRef = useRef(null);
  const dictionaryCacheRef = useRef(new Map());

  const currentSentence = useMemo(
    () => sentences[currentIndex] ?? "",
    [sentences, currentIndex]
  );
  const currentWords = useMemo(
    () => currentSentence.match(/[A-Za-z']+/g) ?? [],
    [currentSentence]
  );

  async function requestPractice(sentence) {
    setIsLoadingPractice(true);
    setErrorMessage("");
    setEvaluation(null);
    setUserInput("");

    try {
      const response = await apiRequest("/practice", {
        method: "POST",
        body: JSON.stringify({ sentence }),
      });

      if (response.status === 401) {
        logout();
        navigate("/login", { replace: true });
        return;
      }

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || "Could not generate practice audio.");
      }

      setPracticeData(data);
    } catch (error) {
      setPracticeData(null);
      setErrorMessage(error.message);
    } finally {
      setIsLoadingPractice(false);
    }
  }

  async function startPractice() {
    const nextSentences = splitIntoSentences(paragraph);

    if (!nextSentences.length) {
      setErrorMessage("Please enter a paragraph with at least one sentence.");
      return;
    }

    setSentences(nextSentences);
    setCurrentIndex(0);
    await requestPractice(nextSentences[0]);
  }

  async function handleEvaluate() {
    if (!currentSentence) {
      return;
    }

    setIsLoadingEvaluation(true);
    setErrorMessage("");

    try {
      const response = await apiRequest("/evaluate", {
        method: "POST",
        body: JSON.stringify({
          sentence: currentSentence,
          user_input: userInput,
        }),
      });

      if (response.status === 401) {
        logout();
        navigate("/login", { replace: true });
        return;
      }

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || "Could not evaluate your answer.");
      }

      setEvaluation(data);
    } catch (error) {
      setEvaluation(null);
      setErrorMessage(error.message);
    } finally {
      setIsLoadingEvaluation(false);
    }
  }

  async function goToNextSentence() {
    const nextIndex = currentIndex + 1;
    if (nextIndex >= sentences.length) {
      return;
    }

    setCurrentIndex(nextIndex);
    await requestPractice(sentences[nextIndex]);
  }

  function playAudio(speed, rate = 1) {
    if (!practiceData) {
      return;
    }

    const url =
      speed === "slow"
        ? practiceData.audio_slow_url
        : practiceData.audio_normal_url;

    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }

    const audio = new Audio(url);
    audio.playbackRate = rate;
    audioRef.current = audio;
    audio.play().catch(() => {
      setErrorMessage("Audio playback was blocked. Try clicking again.");
    });
  }

  function handleLogout() {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }

    logout();
    navigate("/login", { replace: true });
  }

  async function handleWordClick(word) {
    setSelectedWord(word);
    setDictionaryError("");
    setDictionaryData(null);

    const cacheKey = word.toLowerCase();
    if (dictionaryCacheRef.current.has(cacheKey)) {
      setDictionaryData(dictionaryCacheRef.current.get(cacheKey));
      return;
    }

    setIsDictionaryLoading(true);

    try {
      const response = await apiRequest(
        `/dictionary?word=${encodeURIComponent(word)}`,
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

      dictionaryCacheRef.current.set(cacheKey, data);
      setDictionaryData(data);
    } catch (error) {
      setDictionaryError(error.message);
    } finally {
      setIsDictionaryLoading(false);
    }
  }

  function closeDictionaryModal() {
    setSelectedWord("");
    setDictionaryData(null);
    setDictionaryError("");
    setIsDictionaryLoading(false);
  }

  const hasStarted = sentences.length > 0;
  const isLastSentence = currentIndex >= sentences.length - 1;

  return (
    <div className="page-shell">
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      <main className="app-card">
        <section className="hero hero-row">
          <div>
            <p className="eyebrow">Study English With Tobi</p>
            <h1>Practice one sentence at a time with instant feedback.</h1>
            <p className="hero-copy">
              Paste a paragraph, generate listening audio, type what you hear,
              and review mistakes clearly.
            </p>
          </div>

          <div className="user-box">
            <p className="user-label">Logged in as</p>
            <p className="user-email">{user?.email || "Unknown user"}</p>
            <div className="action-row compact-row">
              <button
                className="secondary-button"
                type="button"
                onClick={() => navigate("/history")}
              >
                View Learning History
              </button>
              <button
                className="secondary-button"
                type="button"
                onClick={() => navigate("/vocabulary")}
              >
                My Vocabulary
              </button>
              <button className="ghost-button" type="button" onClick={handleLogout}>
                Logout
              </button>
            </div>
          </div>
        </section>

        <section className="panel">
          <div className="section-heading">
            <h2>Input Paragraph</h2>
            <span>{sentences.length ? `${sentences.length} sentences` : "Ready"}</span>
          </div>

          <textarea
            className="paragraph-input"
            placeholder="Paste your English paragraph here..."
            value={paragraph}
            onChange={(event) => setParagraph(normalizeParagraphInput(event.target.value))}
            rows={7}
          />

          <button
            className="primary-button"
            type="button"
            onClick={startPractice}
            disabled={isLoadingPractice}
          >
            {isLoadingPractice ? "Preparing..." : "Start Practice"}
          </button>
        </section>

        <section className="panel">
          <div className="section-heading">
            <h2>Sentence Flow</h2>
            <span>
              {hasStarted ? `Sentence ${currentIndex + 1}/${sentences.length}` : "Waiting"}
            </span>
          </div>

          <div className="sentence-stage">
            {hasStarted
              ? "Audio is ready. Listen carefully, then type what you hear."
              : "Your current sentence will appear here after you start."}
          </div>

          <div className="word-explorer">
            <p className="feedback-title">Word Explorer</p>
            {currentWords.length ? (
              <div className="word-list">
                {currentWords.map((word, index) => (
                  <Word key={`${word}-${index}`} text={word} onClick={handleWordClick} />
                ))}
              </div>
            ) : (
              <div className="empty-state compact-empty">
                Start practice to click and explore word meanings.
              </div>
            )}
          </div>

          <div className="audio-actions">
            <button
              className="secondary-button"
              type="button"
              onClick={() => playAudio("normal")}
              disabled={!practiceData}
            >
              Play Normal
            </button>
            <button
              className="secondary-button"
              type="button"
              onClick={() => playAudio("normal", 1.25)}
              disabled={!practiceData}
            >
              Play 1.25x
            </button>
            <button
              className="secondary-button"
              type="button"
              onClick={() => playAudio("slow")}
              disabled={!practiceData}
            >
              Play Slow
            </button>
            <button
              className="ghost-button"
              type="button"
              onClick={() => playAudio("normal")}
              disabled={!practiceData}
            >
              Replay Audio
            </button>
          </div>
        </section>

        <section className="panel">
          <div className="section-heading">
            <h2>Dictation</h2>
            <span>Type what you hear</span>
          </div>

          <input
            className="dictation-input"
            type="text"
            placeholder="Type the sentence here..."
            value={userInput}
            onChange={(event) => setUserInput(event.target.value)}
            disabled={!currentSentence}
          />

          <div className="action-row">
            <button
              className="primary-button"
              type="button"
              onClick={handleEvaluate}
              disabled={!currentSentence || isLoadingEvaluation}
            >
              {isLoadingEvaluation ? "Evaluating..." : "Check Answer"}
            </button>

            <button
              className="secondary-button"
              type="button"
              onClick={goToNextSentence}
              disabled={!hasStarted || isLastSentence}
            >
              Next Sentence
            </button>
          </div>
        </section>

        <section className="panel">
          <div className="section-heading">
            <h2>Evaluation</h2>
            <span>{evaluation ? `${evaluation.accuracy}% accuracy` : "No result yet"}</span>
          </div>

          {evaluation ? (
            <div className="evaluation-grid">
              <div className="metric-card">
                <p className="metric-label">Accuracy</p>
                <p className="metric-value">{evaluation.accuracy}%</p>
              </div>

              <div className="feedback-card">
                <p className="feedback-title">Highlighted Differences</p>
                <div className="diff-list">{renderDiff(evaluation.diff)}</div>
              </div>

              <div className="feedback-card">
                <p className="feedback-title">Correct Sentence</p>
                <p className="correct-sentence">{evaluation.correct_sentence}</p>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              Submit your dictation to see accuracy and detailed word-level
              feedback.
            </div>
          )}
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
