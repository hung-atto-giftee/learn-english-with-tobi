import { useEffect, useRef, useState } from "react";

import { API_BASE_URL, apiRequest } from "../lib/api";

export default function DictionaryModal({
  isOpen,
  word,
  data,
  isLoading,
  errorMessage,
  onClose,
}) {
  const [isAudioLoading, setIsAudioLoading] = useState(false);
  const [audioError, setAudioError] = useState("");
  const audioRef = useRef(null);

  useEffect(() => {
    if (!isOpen && audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
  }, [isOpen]);

  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  if (!isOpen) {
    return null;
  }

  async function handlePlayWordAudio() {
    const targetWord = data?.word || word;
    if (!targetWord) {
      return;
    }

    setIsAudioLoading(true);
    setAudioError("");

    try {
      const response = await apiRequest(
        `/tts/word?word=${encodeURIComponent(targetWord)}`,
        { method: "GET" }
      );
      const payload = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(payload.detail || "Could not generate word audio.");
      }

      const audioUrl = payload.absolute_audio_url
        || (payload.audio_url?.startsWith("http")
          ? payload.audio_url
          : `${API_BASE_URL}${payload.audio_url}`);

      if (!audioUrl) {
        throw new Error("Word audio URL is missing.");
      }

      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }

      const audio = new Audio(audioUrl);
      audioRef.current = audio;
      await audio.play();
    } catch (error) {
      setAudioError(error.message || "Could not play word audio.");
    } finally {
      setIsAudioLoading(false);
    }
  }

  return (
    <div className="modal-overlay" role="presentation" onClick={onClose}>
      <div
        className="modal-card"
        role="dialog"
        aria-modal="true"
        aria-label="Dictionary result"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="modal-header">
          <div className="modal-heading-group">
            <p className="eyebrow modal-eyebrow">Dictionary</p>
            <div className="modal-title-row">
              <h2 className="modal-title">{data?.word || word}</h2>
              <button
                className="secondary-button modal-audio-button"
                type="button"
                onClick={handlePlayWordAudio}
                disabled={isAudioLoading || isLoading}
                aria-label={`Play pronunciation for ${data?.word || word}`}
              >
                {isAudioLoading ? "Loading..." : "🔊"}
              </button>
            </div>
            <p className="modal-phonetic">{data?.phonetic || "No IPA available"}</p>
          </div>

          <button className="ghost-button" type="button" onClick={onClose}>
            Close
          </button>
        </div>

        {isLoading ? (
          <div className="empty-state">Looking up this word...</div>
        ) : errorMessage ? (
          <div className="error-banner">{errorMessage}</div>
        ) : (
          <div className="dictionary-meanings">
            {data?.meanings?.map((item, index) => (
              <article key={`${item.part_of_speech}-${index}`} className="dictionary-meaning-card">
                <p className="history-label">{item.part_of_speech}</p>
                <p className="history-text">{item.vi || item.definition}</p>
                {item.en && item.vi ? (
                  <p className="dictionary-english-text">{item.en}</p>
                ) : null}
              </article>
            ))}
          </div>
        )}

        {audioError ? <div className="error-banner">{audioError}</div> : null}
      </div>
    </div>
  );
}
