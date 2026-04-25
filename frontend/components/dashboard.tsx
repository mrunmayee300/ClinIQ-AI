"use client";

import { useMemo, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { diagnose } from "@/lib/api";

type ResultShape = {
  disease_ranking: { disease: string; confidence: number; reasoning: string }[];
  summary: {
    risk_level: string;
    suggested_next_steps: string[];
    disclaimer: string;
  };
  agent_trace: { agent: string; status: string }[];
};

const defaultPayload = {
  symptoms_text: "Fever, cough, fatigue for 3 days with mild shortness of breath",
  age: 32,
  gender: "female",
  medical_history: ["hypertension"],
  medications: ["amlodipine"],
  severity: "moderate",
  lifestyle: { smoking: false, alcohol: false, activity_level: "moderate" }
};

export function Dashboard() {
  const [payload, setPayload] = useState(defaultPayload);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ResultShape | null>(null);

  const chartData = useMemo(
    () =>
      (result?.disease_ranking ?? []).map((item) => ({
        disease: item.disease,
        confidence: Number((item.confidence * 100).toFixed(1))
      })),
    [result]
  );

  const submit = async () => {
    setLoading(true);
    try {
      const response = await diagnose(payload);
      setResult(response);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 p-6">
      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-3">
        <section className="rounded-xl bg-card p-5 lg:col-span-1">
          <h2 className="mb-4 text-lg font-semibold">Patient Input</h2>
          <textarea
            className="h-40 w-full rounded-md bg-slate-900 p-3"
            value={payload.symptoms_text}
            onChange={(e) => setPayload({ ...payload, symptoms_text: e.target.value })}
          />
          <button className="mt-4 w-full rounded-md bg-cyan-500 px-3 py-2 font-semibold text-slate-900" onClick={submit}>
            {loading ? "Analyzing..." : "Run Diagnosis"}
          </button>
        </section>

        <section className="rounded-xl bg-card p-5 lg:col-span-2">
          <h2 className="mb-4 text-lg font-semibold">Disease Probability</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="disease" stroke="#cbd5e1" />
                <YAxis stroke="#cbd5e1" />
                <Tooltip />
                <Bar dataKey="confidence" fill="#22d3ee" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="mt-4 text-sm text-slate-300">{result?.summary?.disclaimer}</p>
        </section>

        <section className="rounded-xl bg-card p-5">
          <h3 className="mb-3 font-semibold">Risk & Follow-up</h3>
          <p className="mb-3 text-cyan-300">Risk: {result?.summary?.risk_level ?? "N/A"}</p>
          <ul className="space-y-2 text-sm text-slate-300">
            {(result?.summary?.suggested_next_steps ?? []).map((step) => (
              <li key={step}>- {step}</li>
            ))}
          </ul>
        </section>

        <section className="rounded-xl bg-card p-5 lg:col-span-2">
          <h3 className="mb-3 font-semibold">Agent Reasoning Trace</h3>
          <div className="space-y-2 text-sm text-slate-300">
            {(result?.agent_trace ?? []).map((node, idx) => (
              <div key={`${node.agent}-${idx}`} className="rounded-md bg-slate-900 p-2">
                {node.agent}: {node.status}
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
