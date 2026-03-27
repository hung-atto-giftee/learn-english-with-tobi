export default function Word({ text, onClick }) {
  return (
    <button className="word-chip" type="button" onClick={() => onClick(text)}>
      {text}
    </button>
  );
}
