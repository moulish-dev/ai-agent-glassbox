
# 🧠 **GlassMind Navigator**

### **Transparent Agents. Trustworthy Decisions. Full Explainability.**

GlassMind Navigator transforms any AI agent into a **fully observable**, **auditable**, and **explainable** system.
Every decision.
Every memory update.
Every tool call.
Fully visible. Fully traceable. Fully understandable.

Built for **Track B – Agent Glass Box** of the Great Agent Hackathon.

---

## 💡 Inspiration

Modern AI agents act, remember, reason, and take actions — but their internal process is still a black box.
Track B asks a critical question:

> **“Can you build an agent you can actually understand?”**

This challenge aligns perfectly with my ongoing work in **Artificial Human Intelligence (AHI)**, cognitive architectures, and explainable agent systems.

I wanted to build something that:

* Shows the entire reasoning flow
* Makes memory mutations fully visible
* Reveals hidden behavioral patterns
* Helps developers debug, trust, and improve agents

**GlassMind Navigator is the answer.**

---

## 🧠 What It Does

GlassMind Navigator makes agent cognition **transparent** and **auditable**.

### 🔍 **Key Features**

#### **1. Full Trajectory Visualization**

See the complete reasoning chain:

* Thoughts
* Decisions
* Tool calls
* Outputs
* Next state

#### **2. Memory Timeline Analyzer**

Inspect:

* `memory_before`
* `memory_after`
  for each node.

Watch how memory evolves step by step.

#### **3. Behavior Pattern Analyzer**

Automatically discovers:

* Tool overuse
* Reasoning loops
* Node frequency
* Unnecessary steps
* Hallucination triggers

#### **4. Error Replay Mode**

Finds failure points and reconstructs exactly where reasoning went wrong.

Perfect for debugging and safety evaluations.

#### **5. Before/After Optimization**

Change a config → Re-run → Instantly visualize improvement in:

* Tool calls
* Step count
* Stability
* Consistency

#### **6. Real-Time LangSmith Observability**

All major nodes use `@traceable`, giving:

* Clean execution traces
* Step-level audit logs
* Reproducible trajectories

---

## 🧩 How We Built It

### **Architecture Overview**

```
User  
   ↓  
LangGraph-style Agent (Plan → Research → Answer)  
   ↓  
Trajectory Recorder  
   ↓  
Streamlit Trace Visualizer  
   ↓  
Memory Timeline Analyzer  
   ↓  
Behavior Pattern Analyzer  
   ↓  
Improvement Engine
```

### **Core Components**

| File                            | Purpose                                     |
| ------------------------------- | ------------------------------------------- |
| `backend/graph.py`              | Agent logic, plan-research-answer pipeline  |
| `backend/models.py`             | Pydantic models for structured step logging |
| `analysis/traces_loader.py`     | Save/load agent trajectories                |
| `analysis/behavior_analysis.py` | Statistical pattern analysis                |
| `frontend/app.py`               | Streamlit interactive UI                    |
| `backend/llm.py`                | Gemini/Ollama Valyu search integration      |

### **Tech Stack**

* **LangSmith** (`@traceable`) — observability & auditing
* **Gemini** — reasoning
* **Valyu DeepSearch API** — research tool
* **Streamlit** — visualization dashboard
* **Pandas** — behavior analysis
* **JSON traces** — reproducibility
* **Python** — glue for agent logic

---

## 🚧 Challenges We Ran Into

* Ollama timeouts → solved by switching to Gemini
* Making every node fully serializable for LangSmith
* Streamlit import path and environment issues
* Designing memory_before / memory_after without corrupting state
* Structuring traces that remain clean, readable, and scalable
* Turning raw logs into intuitive, human-friendly visualizations

Each challenge helped refine the final solution and reinforced the importance of **robust observability** in agentic systems.

---

## 🏆 Accomplishments We’re Proud Of

* Built end-to-end explainability from scratch
* Achieved full trajectory capture without LangGraph’s built-in tools
* Created behavior analysis that reveals real agent patterns
* Integrated LangSmith successfully for complete auditability
* Built a clean, extensible foundation for any future agent
* Delivered a UI where judges can see:

  * Why a decision was made
  * What the agent remembered
  * How memory changed
  * Where a mistake happened
  * How the improvement engine enhances stability

---

## 📚 What We Learned

* Observability is a **design philosophy**, not an addon
* Memory tracking is essential for debugging AI agents
* Tool usage drastically shapes agent behavior
* Small config changes can radically alter trajectories
* Explainability requires **deliberate engineering**
* Transparency is the foundation for agent trust and safety

---

## 🚀 What’s Next for GlassMind Navigator

### 🔮 Upcoming Enhancements

* Visual DAG-based trajectory graphs
* Natural language “step explanation diffs”
* Multi-agent execution visualization
* Automated anomaly detection
* Reinforcement learning for config optimization
* Integration with AWS Bedrock Agents & Strands SDK
* Plugin system for custom tools and memory modules

### 🌍 Long-Term Vision

A **universal observability dashboard** for any agent framework —
advancing trust, safety, and transparency for real-world agent deployments.

---

## 🛠 Installation & Setup

```bash
git clone <repo>
cd glassmind-navigator

pip install -r requirements.txt
streamlit run frontend/app.py
```

Ensure:

* `.env` contains API keys (Gemini, Valyu, LangSmith)
* Gemini + Valyu APIs are active
* You have traces generated via `run_once.py`

---

## ▶️ Running the Agent

To generate a trace:

```bash
python run_once.py
```

To visualize:

```bash
streamlit run frontend/app.py
```

---

