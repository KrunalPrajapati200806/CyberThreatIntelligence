// const API_BASE = "http://127.0.0.1:8000";

// export async function checkHealth() {
//   const response = await fetch(`${API_BASE}/health`, {
//     method: "GET",
//     cache: "no-store",
//   });

//   if (!response.ok) {
//     throw new Error("API health check failed.");
//   }

//   return response.json();
// }

// export async function analyzeFile(file) {
//   if (!file) {
//     throw new Error("No file selected.");
//   }

//   const formData = new FormData();
//   formData.append("file", file);

//   const response = await fetch(`${API_BASE}/predict-csv`, {
//     method: "POST",
//     body: formData,
//   });

//   let data;

//   try {
//     data = await response.json();
//   } catch {
//     throw new Error(
//       `Backend returned HTTP ${response.status}.`
//     );
//   }

//   if (!response.ok) {
//     throw new Error(
//       data?.detail || "Traffic analysis failed."
//     );
//   }

//   return data;
// }

// export { API_BASE };




const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

export async function checkHealth() {
  const response = await fetch(`${API_BASE}/health`, {
    method: "GET",
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("API health check failed.");
  }

  return response.json();
}

export async function analyzeFile(file, modelType = "multiclass") {
  if (!file) {
    throw new Error("No file selected.");
  }

  if (!["binary", "multiclass"].includes(modelType)) {
    throw new Error(
      "Invalid model type. Use 'binary' or 'multiclass'."
    );
  }

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(
    `${API_BASE}/predict-csv?model_type=${encodeURIComponent(modelType)}`,
    {
      method: "POST",
      body: formData,
    }
  );

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error(
      `Backend returned HTTP ${response.status}.`
    );
  }

  if (!response.ok) {
    throw new Error(
      data?.detail || "Traffic analysis failed."
    );
  }

  return data;
}

export { API_BASE };
