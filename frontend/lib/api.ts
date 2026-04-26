export const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api/v1";

export type DiagnosePayload = {
  symptoms_text: string;
  age: number;
  gender: string;
  medical_history: string[];
  medications: string[];
  severity: string;
  lifestyle: {
    smoking: boolean;
    alcohol: boolean;
    activity_level: string;
  };
};

export async function diagnose(payload: DiagnosePayload) {
  const response = await fetch(`${API_BASE}/diagnose`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error("Diagnosis request failed");
  return response.json();
}

export async function retrieveMedicalContext(payload: DiagnosePayload) {
  const response = await fetch(`${API_BASE}/retrieve-medical-context`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error("Medical context retrieval failed");
  return response.json();
}
