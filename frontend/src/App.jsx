import React, { useState } from "react";

const API_URL = "http://localhost:8000/api/research";

export default function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setData(null);
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || "Research request failed");
      setData(body);
    } catch (err) {
      setError(err.message || "Unable to connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  const report = data?.report;

  return (
    <main className="container">
      <header>
        <p className="eyebrow">LANGGRAPH + TAVILY + GROQ</p>
        <h1>AI Research Agent</h1>
        <p className="sub">Ask a research question. The agent plans, searches, evaluates evidence, and creates a cited report.</p>
      </header>

      <form className="question-form" onSubmit={handleSubmit}>
        <label htmlFor="question">Research question</label>
        <textarea id="question" value={question} onChange={e => setQuestion(e.target.value)}
          placeholder="Example: Compare the top 3 open-source vector databases for a startup building RAG products."
          minLength={8} maxLength={1500} required />
        <button disabled={loading || question.trim().length < 8}>
          {loading ? "Researching..." : "Start research"}
        </button>
      </form>

      {loading && <section className="panel"><p>The agent is planning and gathering evidence. This may take a little time.</p></section>}
      {error && <section className="error">{error}</section>}

      {report && <>
        <section className="panel">
          <div className="row"><h2>Short answer</h2><span className={`confidence ${report.confidence}`}>{report.confidence} confidence</span></div>
          <p>{report.short_answer}</p>
          <small>Question: {report.user_question}</small>
        </section>

        <section className="panel">
          <h2>Key findings</h2>
          {report.key_findings.map((item, i) => <article className="finding" key={i}>
            <h3>{item.heading}</h3><p>{item.detail}</p>
            {item.supporting_source_ids?.length > 0 && <small>Sources: {item.supporting_source_ids.join(", ")}</small>}
          </article>)}
        </section>

        <section className="panel">
          <h2>Sources used</h2>
          {report.sources.map(source => <article className="source" key={source.source_id}>
            <strong>{source.source_id}. {source.title}</strong>
            <p>{source.snippet}</p>
            <a href={source.url} target="_blank" rel="noreferrer">{source.url}</a>
          </article>)}
          {report.sources.length === 0 && <p>No sources were successfully extracted.</p>}
        </section>

        <section className="two-col">
          <div className="panel"><h2>Confidence and limitations</h2>
            <p>{report.confidence_reason}</p>
            <ul>{report.limitations_assumptions.map((x, i) => <li key={i}>{x}</li>)}</ul>
          </div>
          <div className="panel"><h2>Suggested next steps</h2>
            <ul>{report.next_steps.map((x, i) => <li key={i}>{x}</li>)}</ul>
          </div>
        </section>

        <section className="panel">
          <h2>Agent execution trace</h2>
          <ol className="trace">{data.trace.map((step, i) => <li key={i}>{step.replaceAll("_", " ")}</li>)}</ol>
          <small>Recovery rounds used: {data.recovery_count}</small>
        </section>
      </>}
    </main>
  );
}
