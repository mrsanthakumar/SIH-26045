import React, {useState} from "react";
import {createRoot} from "react-dom/client";
import {ShieldCheck, Search, Scale, Leaf, Globe2, FileCheck2, AlertTriangle, ArrowRight} from "lucide-react";
import "./styles.css";

const API="http://localhost:8000/api";

function App(){
  const [jurisdiction,setJurisdiction]=useState("India");
  const [question,setQuestion]=useState("");
  const [chat,setChat]=useState(null);
  const [loading,setLoading]=useState(false);
  const [searchMode,setSearchMode]=useState(true);
  const [tab,setTab]=useState("assistant");
  const [form,setForm]=useState({product_name:"",intended_use:"",classical_text:"unknown",modification:"unknown",ingredients:[],biological_source:"unknown",market:"India",question:"",ip_types:[]});
  const [classification,setClassification]=useState(null);

  async function ask(){
    if(!question.trim()) return;
    setLoading(true);
    try{
      const r=await fetch(`${API}/chat`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question,jurisdiction,language:"English"})});
      setChat(await r.json());
    }catch(e){setChat({answer:"Backend unavailable. Start the FastAPI server on port 8000.",confidence:0,sources:[]})}
    setLoading(false);
  }

  async function classify(){
    setLoading(true);
    try{
      const payload={...form,market:jurisdiction};
      const r=await fetch(`${API}/classify`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
      setClassification(await r.json());
    }catch(e){setClassification({category:"Backend unavailable",reason:"Start FastAPI on port 8000.",confidence:0})}
    setLoading(false);
  }

  async function runAssessment(){
    setLoading(true);
    try{
      const payload={...form,market:jurisdiction,question:form.question||"Can this Ayurvedic product be protected by intellectual property?"};
      const r=await fetch(`${API}/assess`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
      setChat(await r.json());
      setTab("assistant");
    }catch(e){setChat({findings:["Backend unavailable."],confidence:0,sources:[]})}
    setLoading(false);
  }

  return <div className="app">
    <header>
      <div className="brand"><div className="logo"><Leaf size={24}/></div><div><b>AyurIPR</b><span>Ayurveda IPR & Regulatory Intelligence</span></div></div>
      <div className="jurisdiction"><Globe2 size={17}/><button className={jurisdiction==="India"?"active":""} onClick={()=>setJurisdiction("India")}>🇮🇳 India</button><button className={jurisdiction==="International"?"active":""} onClick={()=>setJurisdiction("International")}>🌍 International</button></div>
    </header>

    <main>
      <section className="hero">
        <div className="eyebrow">SOURCE-GROUNDED DECISION SUPPORT</div>
        <h1>Protect Ayurvedic innovation.<br/><em>Respect traditional knowledge.</em></h1>
        <p>Classify your product, map the relevant IP and regulatory regimes, and move from a question to authoritative sources.</p>
      </section>

      <nav className="tabs">
        <button className={tab==="assistant"?"selected":""} onClick={()=>setTab("assistant")}><Search size={17}/> AI Assistant</button>
        <button className={tab==="classify"?"selected":""} onClick={()=>setTab("classify")}><FileCheck2 size={17}/> Product Classification</button>
        <button className={tab==="assessment"?"selected":""} onClick={()=>setTab("assessment")}><Scale size={17}/> IP Assessment</button>
        <button className={tab==="sources"?"selected":""} onClick={()=>setTab("sources")}><ShieldCheck size={17}/> Source Explorer</button>
      </nav>

      {tab==="assistant" && <section className="grid">
        <div className="card chat-card">
          <div className="card-title"><div><h2>Ask AyurIPR</h2><span>Jurisdiction: {jurisdiction}</span></div><div className="pill">Information, not legal advice</div></div>
          <textarea value={question} onChange={e=>setQuestion(e.target.value)} placeholder="Ask any Ayurveda IPR or regulatory question. AyurIPR checks the indexed corpus and the live public web."/>
          <div className="live-search-note"><span className="live-dot"></span> Live internet sources are checked for every question</div>
          <div className="chips">{["Can I patent my formulation?","Do I need ABS compliance?","Could this be traditional knowledge?","Which IP protects my brand?"].map(x=><button onClick={()=>setQuestion(x)}>{x}</button>)}</div>
          <button className="primary" onClick={ask} disabled={loading}>{loading?"Checking…":"Analyze question"} <ArrowRight size={18}/></button>
        </div>
        <div className="card side-card">
          <h3>How AyurIPR works</h3>
          {[
            ["01","Classify","Determine the likely product/regulatory category."],
            ["02","Route","Map patent, trademark, GI, design, ABS and TK issues."],
            ["03","Retrieve","Use indexed authoritative sources for the selected jurisdiction."],
            ["04","Verify","Show citations, confidence and human-review escalation."]
          ].map(x=><div className="step"><b>{x[0]}</b><div><strong>{x[1]}</strong><p>{x[2]}</p></div></div>)}
        </div>
      </section>}

      {tab==="classify" && <section className="card form-card">
        <div className="card-title"><div><h2>Formulation Classification</h2><span>Answer the minimum questions first.</span></div><span className="juripill">{jurisdiction}</span></div>
        <div className="formgrid">
          <label>Product name<input value={form.product_name} onChange={e=>setForm({...form,product_name:e.target.value})}/></label>
          <label>Intended use<input value={form.intended_use} onChange={e=>setForm({...form,intended_use:e.target.value})} placeholder="medicine, food, cosmetic..."/></label>
          <label>Classical authoritative text?<select value={form.classical_text} onChange={e=>setForm({...form,classical_text:e.target.value})}><option>unknown</option><option>yes</option><option>no</option></select></label>
          <label>Modified formulation/process?<select value={form.modification} onChange={e=>setForm({...form,modification:e.target.value})}><option>unknown</option><option>no</option><option>yes</option></select></label>
          <label>Biological resource source<select value={form.biological_source} onChange={e=>setForm({...form,biological_source:e.target.value})}><option>unknown</option><option>India</option><option>outside India</option><option>cultivated</option><option>wild collected</option></select></label>
        </div>
        <button className="primary" onClick={classify}>Classify product <ArrowRight size={18}/></button>
        {classification && <div className="result"><div className="result-head"><span>PRELIMINARY CLASSIFICATION</span><strong>{Math.round(classification.confidence*100)}% confidence</strong></div><h2>{classification.category}</h2><p>{classification.reason}</p></div>}
      </section>}

      {tab==="assessment" && <section className="card form-card">
        <div className="card-title"><div><h2>IP & ABS Assessment</h2><span>Preliminary routing across overlapping regimes.</span></div></div>
        <label>Question<textarea value={form.question} onChange={e=>setForm({...form,question:e.target.value})} placeholder="What do you want to protect or commercialise?"/></label>
        <div className="checkgrid">{["Patent","Trademark","GI","Design","Copyright","ABS / Biodiversity","Traditional Knowledge"].map(x=><label className="check"><input type="checkbox" onChange={e=>setForm({...form,ip_types:e.target.checked?[...form.ip_types,x]:form.ip_types.filter(y=>y!==x)})}/>{x}</label>)}</div>
        <button className="primary" onClick={runAssessment}>Run assessment <ArrowRight size={18}/></button>
      </section>}

      {tab==="sources" && <Sources jurisdiction={jurisdiction}/>}
      {chat && tab==="assistant" && <Response data={chat}/>}
    </main>

    <footer><AlertTriangle size={15}/> AyurIPR provides information and decision support, not legal advice. Always verify current law, rules and registry records before acting.</footer>
  </div>
}

function Response({data}){
 return <section className="response">
   <div className="response-main card">
    <div className="result-head"><span>AI ASSESSMENT</span><strong>{data.confidence?Math.round(data.confidence*100):0}% confidence</strong></div>
    {data.internet_checked && <div className="web-status"><span className="live-dot"></span><b>Internet checked</b> · {data.search_results||0} live results · {data.official_results||0} official-priority results{data.checked_at && <> · {new Date(data.checked_at).toLocaleString()}</>}</div>}
    {data.findings ? <>{data.findings.map((x,i)=><p className="finding" key={i}>• {x}</p>)}</> : <div className="answer-text">{String(data.answer||'').split('\n').map((x,i)=><p key={i}>{x}</p>)}</div>}
    {data.human_review && <div className="warning">Human review recommended for this assessment.</div>}
    <small>{data.disclaimer}</small>
   </div>
   <div className="card sources"><h3>Sources checked</h3>{(data.sources||[]).map((s,i)=><a href={s.url} target="_blank" rel="noreferrer" key={i}><strong>{s.title}</strong><span>{s.authority} {s.section&&"· "+s.section}</span>{s.snippet&&<em>{s.snippet}</em>}</a>)}</div>
 </section>
}

function Sources({jurisdiction}){
 const [rows,setRows]=useState([]);
 React.useEffect(()=>{fetch(`${API}/sources?jurisdiction=${jurisdiction}`).then(r=>r.json()).then(setRows).catch(()=>setRows([]))},[jurisdiction]);
 return <section className="card form-card"><div className="card-title"><div><h2>Source Explorer</h2><span>Indexed sources for {jurisdiction}</span></div></div>{rows.map(s=><a className="source-row" href={s.url} target="_blank"><div><strong>{s.title}</strong><p>{s.authority} · {s.section||"Official source"}</p></div><span>Open ↗</span></a>)}</section>
}

createRoot(document.getElementById("root")).render(<App/>);
