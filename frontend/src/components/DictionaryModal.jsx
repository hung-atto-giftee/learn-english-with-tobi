export default function DictionaryModal({
  isOpen,
  word,
  data,
  isLoading,
  errorMessage,
  onClose,
}) {
  if (!isOpen) {
    return null;
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
          <div>
            <p className="eyebrow modal-eyebrow">Dictionary</p>
            <h2 className="modal-title">{data?.word || word}</h2>
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
                <p className="history-text">{item.definition}</p>
              </article>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
